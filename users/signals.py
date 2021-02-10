from django.db.models.signals import post_save
from django.dispatch import receiver

from admin_portal.models import User, LifeChoicesMember, LifeChoicesAcademy, LifeChoicesStuff


@receiver(post_save, sender=User)
def create_life_choices_member(sender, instance, created, **kwargs):
    if created:
        LifeChoicesMember.object.create(user=instance)


@receiver(post_save, sender=User)
def create_life_choices_member(sender, instance, **kwargs):
    instance.lifechoicesmember.save()
