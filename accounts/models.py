from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# from cloudinary import models as cloudinary_models

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile')
    image = models.ImageField(
        upload_to='profiles',
        default='profiles/default.jpg')
        # image = cloudinary_models.CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return self.user.username



@receiver(post_save, sender=User)
def user_created(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        # Use getattr to handle the case where instance.profile is not available
        profile = getattr(instance, 'profile', None)
        if profile:
            profile.save()
