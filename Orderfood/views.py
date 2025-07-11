from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from functools import wraps
import re
from django.views.decorators.http import require_POST
from django.utils.timezone import localtime
from Restaurant.models import RegisterCanteen, MenuItem, OrderDetails
from Webusers.models import Users, UserProfile
from Orderfood.models import Cart


# Login required decorator for session-authenticated users
def require_login(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# Show all canteens and cart details
def canteen(request):
    canteens = RegisterCanteen.objects.all()
    user_id = request.session.get('user_id')

    cart, total_price, total_item, all_items = [], 0, 0, []

    if user_id:
        try:
            user = Users.objects.get(id=user_id)
            cart = Cart.objects.filter(cart_user=user)
            total_price = sum(item.item_price * item.item_quantity for item in cart)
            total_item = sum(item.item_quantity for item in cart)
            all_items = [item.item_title for item in cart]
        except Exception as e:
            print(f"Cart fetch error: {e}")

    return render(request, 'canteen/order.html', {
        'cart': cart,
        'all_items': all_items,
        'total_price': total_price,
        'total_item': total_item,
        'canteens': canteens,
    })


# Show menu items from a specific canteen
def menu_page(request, slug):
    user_id = request.session.get('user_id')
    canteen = get_object_or_404(RegisterCanteen, slug=slug)
    items = MenuItem.objects.filter(canteen=canteen)

    cart = []
    total_price = 0
    total_item = 0
    all_items = []
    mobile_number = None  # ✅ Set default if user not logged in

    if user_id:
        try:
            user = Users.objects.get(id=user_id)
            cart = Cart.objects.filter(cart_user=user)
            total_price = sum(item.item_price * item.item_quantity for item in cart)
            total_item = sum(item.item_quantity for item in cart)
            all_items = [item.item_title for item in cart]

            profile = UserProfile.objects.get(user=user)
            mobile_number = profile.mobile_number
        except Users.DoesNotExist:
            print("❌ User not found")
        except UserProfile.DoesNotExist:
            print("⚠️ User profile not found")
        except Exception as e:
            print(f"Cart fetch error: {e}")

    # Group items by category
    categorized_items = {}
    for item in items:
        category = item.category or "Others"
        categorized_items.setdefault(category, []).append(item)

    return render(request, 'canteen/menu.html', {
        'cart': cart,
        'all_items': all_items,
        'total_price': total_price,
        'total_item': total_item,
        'canteen': canteen,
        'categorized_items': categorized_items,
        'mobile_number': mobile_number,
    })

# Add item to cart
@require_login
def addtocart(request, slug, item_id):
    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({'error': 'You must be logged in to add to cart.'}, status=401)

    user = get_object_or_404(Users, id=user_id)
    food = get_object_or_404(MenuItem, id=item_id)

    try:
        cart_item = Cart.objects.filter(cart_user=user, item_slug=food.slug).first()
        if cart_item:
            cart_item.item_quantity += 1
            cart_item.save()
            return JsonResponse({'message': f'One more {food.name} added to your cart!'})
        else:
            Cart.objects.create(
                cart_user=user,
                item_title=food.name,
                item_price=food.price,
                item_slug=food.slug,
                item_quantity=1
            )
            return JsonResponse({'message': f'{food.name} added to your cart!'})
    except Exception as e:
        return JsonResponse({'error': f"Server error: {str(e)}"}, status=500)


# Remove item from cart
@require_login
def remove_from_cart(request, slug, item_id):
    user = get_object_or_404(Users, id=request.session.get('user_id'))
    cart_item = get_object_or_404(Cart, id=item_id, cart_user=user)
    cart_item.delete()
    return JsonResponse({'message': f"{cart_item.item_title} removed from your plate."})


# Confirm order view (from cart)
@require_login
def confirm_order(request):
    if request.method != "POST":
        return redirect("order")

    user = get_object_or_404(Users, id=request.session.get("user_id"))
    cart = Cart.objects.filter(cart_user=user)

    if not cart.exists():
        return redirect("order")

    try:
        order_type = request.POST.get("order_type")
        address = request.POST.get("address")
        mobile_number = request.POST.get("mobile")
        payment_type = request.POST.get("payment")

        total_price = sum(item.item_price * item.item_quantity for item in cart)
        quantity = sum(item.item_quantity for item in cart)

        # Save items as comma-separated string (e.g., "Pizza, Fries")
        items_string = ", ".join(item.item_title for item in cart)

        menu_items_qs = MenuItem.objects.filter(slug__in=[item.item_slug for item in cart])
        canteen = menu_items_qs.first().canteen if menu_items_qs.exists() else None

        if not canteen:
            return redirect("order")

        # Create the order
        OrderDetails.objects.create(
            user=user,
            mobile_number=mobile_number,
            items=items_string,
            total_price=total_price,
            quantity=quantity,
            address=address,
            order_type=order_type,
            payment_type=payment_type,
            order_status="Pending",
            canteen=canteen
        )

        # Estimate delivery time
        def parse_minutes(time_str):
            match = re.search(r'(\d+)', time_str)
            return int(match.group(1)) if match else 0

        delivery_times = [
            parse_minutes(item.delivery_time) for item in menu_items_qs
            if hasattr(item, 'delivery_time') and item.delivery_time
        ]
        average_minutes = sum(delivery_times) // len(delivery_times) if delivery_times else 0

        # Clear cart
        cart.delete()

        latest_order = OrderDetails.objects.filter(user=user).order_by('-ordered_at').first()

        return render(request, 'canteen/confirm_order.html', {
            'user': user,
            'total_price': total_price,
            'order_date': latest_order.ordered_at.strftime("%B %d, %Y at %I:%M %p") if latest_order else None,
            'order_number': latest_order.order_number if latest_order else "N/A",
            'average_delivery': f"{average_minutes} min" if average_minutes else "N/A"
        })

    except Exception as e:
        print(f"Error confirming order: {e}")
        return redirect("order")



@require_login
def track_order(request, order_id):
    user = get_object_or_404(Users, id=request.session.get("user_id"))

    order = get_object_or_404(OrderDetails, id=order_id, user=user)

    item_names = [name.strip() for name in order.items.split(',') if name.strip()]
    menu_items = MenuItem.objects.filter(name__in=item_names)
    item_map = {item.name: item for item in menu_items}

    def parse_minutes(time_str):
        match = re.search(r'(\d+)', time_str)
        return int(match.group(1)) if match else 0

    delivery_times = [
        parse_minutes(item_map[item].delivery_time)
        for item in item_names if item in item_map and item_map[item].delivery_time
    ]
    average_minutes = sum(delivery_times) // len(delivery_times) if delivery_times else 0

    context = {
        'user': user,
        'items': item_names,
        'menu_items': item_map,
        'total_price': order.total_price,
        'order_date': localtime(order.ordered_at).strftime("%B %d, %Y at %I:%M %p"),
        'order_number': order.order_number,
        'average_delivery': f"{average_minutes} min" if average_minutes else "N/A",
        'order_status': order.order_status,
        'address': order.address,
        'order_type': order.order_type,
        'payment_type': order.payment_type,
        'mobile_number': order.mobile_number,
        'quantity': order.quantity,
        'order': order,
    }

    return render(request, 'canteen/trackorder.html', context)

@require_login
def view_orders(request):
    user = get_object_or_404(Users, id=request.session.get("user_id"))
    orders = OrderDetails.objects.filter(user=user).order_by('-ordered_at')

    if not orders:
        messages.info(request, "You have not placed any orders yet.")

    return render(request, "canteen/view_order.html", {
        "orders": orders,
        "user": user,
    })

@require_POST
@require_login
def cancel_order(request, order_id):
    user = get_object_or_404(Users, id=request.session.get("user_id"))
    order = get_object_or_404(OrderDetails, id=order_id, user=user)

    if order.order_status not in ["Cancelled", "Delivered", "Rejected"]:
        order.order_status = "Cancelled"
        order.save()
        messages.success(request, "Order has been cancelled.")

    return redirect("view_order")

def errorpage(request,path):
    return render(request,'general/404_error.html')
def errorpage2(request,path,err):
    path=None
    err=None
    return render(request,'general/404_error.html')
def errorpage3(request,path,err,errr):
    path=None
    err=None
    return render(request,'general/404_error.html')

