from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    CHOICES = [('male', 'MALE'),
               ('female', 'FEMALE')]

    sex = models.CharField(max_length=10,choices=CHOICES,default="male")
    if sex =="male" or sex == "MALE":

        image = models.ImageField(default="man.png",upload_to="profile_pics")
    else:
        image = models.ImageField(default="female.png", upload_to="profile_pics")


    def __str__(self):
        return f"{self.user.username} Profile"

    def save(self,*args,**kwargs):
        super().save()

        img = Image.open(self.image.path)
        if img.height != 300 or img.width != 300:
            output = (300,300)
            img.thumbnail(output)
            img.save(self.image.path)

        def get_absolute_url(self):
            return reverse("post-detail", kwargs={"pk": self.pk})




@receiver(post_save, sender=User, dispatch_uid='save_new_user_profile')
def save_profile(sender, instance, created, **kwargs):
    user = instance
    if created:
        profile = Profile(user=user)
        profile.save()



"""
>>> from django.contrib.auth.models import User
>>> user = User.objects.filter(username="dino")
>>> user = User.objects.filter(username="dino").first()
>>> user
<User: dino>
>>> user.profile
<Profile: dino Profile>
>>> user.profile.image
<ImageFieldFile: profile_pics/kriteriji1.jpg>
>>> user.profile.image.width
765
>>> user.profile.image.height
185
>>> user.profile.image.size
25252
>>> user.profile.image.url
'/media/profile_pics/kriteriji1.jpg'

"""