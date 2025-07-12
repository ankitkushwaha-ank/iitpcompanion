from django.shortcuts import render, get_object_or_404, redirect
from Restaurant.models import RegisterOwner, RegisterCanteen, MenuItem, OrderDetails
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from .models import RegisterOwner, RegisterCanteen
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from functools import wraps


def require_login(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        owner_id = request.session.get('owner_id')
        if not owner_id:
            return redirect('login_owner')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def register_owner(request):
    if request.method == "POST":
        name = request.POST.get("ownername")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if RegisterOwner.objects.filter(ownername=name).exists():
            messages.error(request, "Username already taken.")
            return redirect("register_owner")

        owner = RegisterOwner(ownername=name, email=email)
        owner.set_password(password)
        owner.save()

        messages.success(request, "Registration successful. Please login.")
        return redirect("login_owner")

    return render(request, "Restaurant/register_owner.html")


def login_owner(request):
    owner_id = request.session.get('owner_id')
    if owner_id:
        messages.error(request, "You are already loggin")
        return redirect('owner_dashboard')
    if request.method == "POST":
        name = request.POST.get("ownername")
        password = request.POST.get("password")

        try:
            owner = RegisterOwner.objects.get(ownername=name)
        except RegisterOwner.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return redirect("login_owner")

        if owner.check_password(password):
            request.session["owner_id"] = owner.id
            return redirect("owner_dashboard")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login_owner")

    return render(request, "Restaurant/login_owner.html")


def logout_owner(request):
    request.session.flush()
    messages.success(request, "Logged out successfully.")
    return redirect("login_owner")

@require_login
def owner_dashboard(request):
    owner_id = request.session.get("owner_id")
    if not owner_id:
        return redirect("login_owner")

    owner = get_object_or_404(RegisterOwner, id=owner_id)
    canteen = RegisterCanteen.objects.filter(owner=owner).first()

    if canteen:
        orders = (
            OrderDetails.objects
            .filter(canteen=canteen)
            .order_by("-ordered_at")
        )
        menu_items = MenuItem.objects.filter(canteen=canteen)
    else:
        orders = []
        menu_items = []

    context = {
        "owner": owner,
        "canteen": canteen,
        "orders": orders,
        "menu_items": menu_items,
    }

    return render(request, "Restaurant/restaurant_admin.html", context)


@require_login
def delete_menu_item(request, slug):
    item = get_object_or_404(MenuItem, slug=slug)
    item.delete()
    messages.success(request, f"'{item.name}' has been deleted successfully.")
    return redirect("owner_dashboard")

@require_login
def update_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)

    if request.method == "POST":
        item.name = request.POST.get("name")
        item.description = request.POST.get("description")
        item.price = request.POST.get("price")
        item.category = request.POST.get("category")
        item.save()
        messages.success(request, "Menu item updated.")
        return redirect("owner_dashboard")

    return render(request, "Restaurant/restaurant_admin.html", {"item": item})


@require_login



def add_menu_item(request):
    owner_id = request.session.get("owner_id")
    owner = get_object_or_404(RegisterOwner, id=owner_id)

    # Get the first canteen linked to this owner
    canteen = RegisterCanteen.objects.filter(owner=owner).first()

    if not canteen:
        messages.error(request, "No canteen found for this owner.")
        return redirect("owner_dashboard")  # Or an error page

    if request.method == "POST":
        MenuItem.objects.create(
            canteen=canteen,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            price=request.POST.get("price"),
            category=request.POST.get("category"),
            delivery_time="20 min",
            image=request.FILES.get("image"),
        )

        messages.success(request, "Menu item added.")
        return redirect("owner_dashboard")

    return render(request, "Restaurant/restaurant_admin.html")


@require_login
def owner_profile(request):
    owner_id = request.session.get("owner_id")
    owner = get_object_or_404(RegisterOwner, id=owner_id)

    try:
        canteen = RegisterCanteen.objects.get(owner_id=owner_id)
    except RegisterCanteen.DoesNotExist:
        canteen = None

    menu_items = MenuItem.objects.filter(canteen=canteen) if canteen else []
    orders = OrderDetails.objects.filter(canteen=canteen).order_by('-id')[:10] if canteen else []

    context = {
        'owner': owner,
        'canteen': canteen,
        'menu_items': menu_items,
        'orders': orders,
    }

    return render(request, 'Restaurant/owner_profile.html', context)

@require_login
def edit_owner_profile(request):
    owner_id = request.session.get("owner_id")
    owner = get_object_or_404(RegisterOwner, id=owner_id)
    canteen = get_object_or_404(RegisterCanteen, owner_id=owner_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        owner.username = username
        owner.save()


        canteen.mobile_number = request.POST.get('mobile_number')
        canteen.save()
        if 'profile_image' in request.FILES:
            owner.profile_image = request.FILES['profile_image']
        owner.save()


        owner.email = request.POST.get('email')
        owner.save()

        return redirect('owner_profile')

    context = {
        'owner': owner,
        'canteen': canteen,
    }
    return render(request, 'Restaurant/edit_owner_profile.html', context)


@require_login
def owner_change_password(request):
    owner_id = request.session.get('owner_id')
    if not owner_id:
        messages.error(request, "You must be logged in to change your password.")
        return redirect('login')

    user = get_object_or_404(RegisterOwner, id=owner_id)

    if request.method == 'POST':
        current_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password1')
        confirm_password = request.POST.get('new_password2')


        if not check_password(current_password, user.password):
            messages.error(request, "❌ Current password is incorrect.")
            return redirect('change_password')


        if new_password != confirm_password:
            messages.error(request, "❌ New passwords do not match.")
            return redirect('change_password')

        # I add password strength check here


        user.password = make_password(new_password)
        user.save()
        messages.success(request, "Password updated successfully.")
        return redirect('owner_profile')

    return render(request, 'Restaurant/owner_change_password.html')


@require_POST
def update_order_status(request, order_id):
    owner_id = request.session.get("owner_id")
    if not owner_id:
        return redirect("login_owner")

    order = get_object_or_404(OrderDetails, id=order_id)
    new_status = request.POST.get("status")

    if new_status in dict(OrderDetails.ORDER_STATUS_CHOICES):
        order.order_status = new_status
        order.save()
        messages.success(request, f"Order #{order.order_number} updated to {new_status}.")
    else:
        messages.error(request, "Invalid order status.")

    # 🔁 Redirect back to the previous page
    return redirect(request.META.get("HTTP_REFERER", "owner_dashboard"))

# View: Order Detail
def order_detail(request, order_id):
    order = get_object_or_404(OrderDetails, id=order_id)
    return render(request, "Restaurant/order_detail.html", {"order": order})


