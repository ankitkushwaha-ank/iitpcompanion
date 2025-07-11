# for getting user live location

# <script>
# navigator.geolocation.watchPosition(function(position) {
#     const latitude = position.coords.latitude;
#     const longitude = position.coords.longitude;
#
#     // Send to backend
#     fetch('/save-location/', {
#         method: 'POST',
#         headers: {
#             'Content-Type': 'application/json',
#             'X-CSRFToken': '{{ csrf_token }}'  // include CSRF if not using API token
#         },
#         body: JSON.stringify({
#             latitude: latitude,
#             longitude: longitude
#         })
#     });
# });
# </script>


# views.py
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .models import UserLocation  # your model
#
# @csrf_exempt
# def save_location(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         latitude = data.get('latitude')
#         longitude = data.get('longitude')
#         user = request.user if request.user.is_authenticated else None  # optional
#
#         UserLocation.objects.create(
#             user=user,
#             latitude=latitude,
#             longitude=longitude
#         )
#
#         return JsonResponse({'status': 'success'})

# urls.py
# from django.urls import path
# from .views import save_location
#
# urlpatterns = [
#     path('save-location/', save_location, name='save_location'),
# ]


# models.py
# from django.db import models
# from django.contrib.auth.models import User
#
# class UserLocation(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
#     latitude = models.FloatField()
#     longitude = models.FloatField()
#     timestamp = models.DateTimeField(auto_now_add=True)


# python manage.py makemigrations
# python manage.py migrate

