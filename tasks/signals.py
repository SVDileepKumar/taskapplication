from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from tasks.models import UserModel


@receiver(post_save, sender=User)
def create_UserModel(sender, instance, **kwargs):
    try:
        usermodel = UserModel.objects.get(user=instance)
    except:
        usermodel = UserModel(user=instance)
        usermodel.save()


@receiver(pre_delete, sender=User)
def remove_UserModel(sender, instance, **kwargs):
    usermodel = UserModel.objects.get(user=instance)
    usermodel.delete()
