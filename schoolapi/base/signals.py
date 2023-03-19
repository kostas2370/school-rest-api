from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Teacher


@receiver(post_save, sender = User)
def create_teacher(sender, instance, created, **kwargs):
    if created:
        Teacher.objects.create(user = instance)


@receiver(post_save, sender = User)
def save_teacher(sender, instance, **kwargs):
    instance.Teacher.save()


"""@receiver(post_save,sender=Student)
def create_grades(sender,instance,created,**kwargs):
	if created:
		Grades.objects.create(Student=instance)



@receiver(post_save,sender=Student)
def save_grades(sender,instance,**kwargs):
	
	instance.Grades.save()
"""
