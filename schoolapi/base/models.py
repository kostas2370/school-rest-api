from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Teacher(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	first_name=models.CharField(max_length=100)
	last_name=models.CharField(max_length=100)
	phone=models.CharField(max_length=10)
	teacher_id = models.AutoField(primary_key=True)
	email=models.EmailField(max_length=254)
	created=models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return f'{self.first_name}{self.last_name}'

class Classroom(models.Model):
	class_name = (
        ('A', 'dhmotiko_a'),
        ('B', 'dhmotiko_b'),
        ('C', 'dhmotiko_c'),
        ('D', 'dhmotiko_d'),
        ('E', 'dhmotiko_e'),
        ('ST', 'dhmotiko_st'),
        ('GA', 'gymnasio_a'),
        ('GB', 'gymnasio_b'),
        ('GC', 'gymnasio_c'),
        ('LA', 'lykeio_a'),
        ('LB', 'lykeio_b'),
        ('LC', 'lykeio_c')

    )
	
	classname=models.CharField(max_length=2,choices=class_name,default='A')
	class_number=models.IntegerField(default=1)
	maximum=models.IntegerField()
	id=models.AutoField(primary_key=True)
	students_in=models.IntegerField(default=0)
	class Meta:
		unique_together = (('classname', 'class_number'),)

	def __str__(self):
		return f'{self.classname}{self.class_number}'
class subject(models.Model):
	onoma=models.CharField(max_length=20)
	teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
	taxh=models.ForeignKey(Classroom,on_delete=models.CASCADE)
	subject_id = models.AutoField(primary_key=True)
	class Meta:
		unique_together = (('onoma', 'taxh'),)
	def __str__(self):
		return f'{self.onoma}{self.taxh}'
class Student(models.Model):
	
	first_name=models.CharField(max_length=100)
	last_name=models.CharField(max_length=100)
	taxh=models.ForeignKey(Classroom,on_delete=models.CASCADE)
	phone=models.CharField(max_length=10)
	student_id = models.AutoField(primary_key=True)
	email=models.EmailField(max_length=254)
	created=models.DateTimeField(auto_now_add=True)
	photo=models.ImageField(default="student_pics/default.png",upload_to="student_pics")
	apousies=models.IntegerField(default=0)
	def save(self,*args, **kwargs):
		super().save()
		img= Image.open(self.photo.path)	
		if img.height >300 or img.width >300:
			outputsize=(300,300)
			img.thumbnail(outputsize)
			img.save(self.photo.path)
	def __str__(self):
		return f'{self.first_name}{self.last_name}{self.student_id}'
class Grades(models.Model):
	student=models.ForeignKey(Student,on_delete=models.CASCADE)
	subject_name=models.ForeignKey(subject,on_delete=models.CASCADE)
	teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
	classroom=models.ForeignKey(Classroom,on_delete=models.CASCADE)
	grade=models.IntegerField(default=0)
	id=models.AutoField(primary_key=True)
	def __str__(self):
		return f'{self.student.first_name}{self.student.last_name}{self.subject_name.onoma}'
	class Meta:
		unique_together = (('student', 'subject_name'),)