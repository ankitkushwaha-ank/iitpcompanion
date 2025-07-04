from django.db import models
from Webusers.models import Users

class Notification(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}"
