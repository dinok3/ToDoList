from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class todolist(models.Model):
    name = models.CharField(max_length=150)
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("todolist-detail",kwargs={"id":self.id})

    

class items(models.Model):
    todolist = models.ForeignKey(todolist,on_delete=models.CASCADE, null=True)
    item_name = models.CharField(max_length=300)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return self.item_name

    def get_absolute_url(self):
        return reverse("home-page")