from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    choices = ((1, "school_manager"), (2, "school_teacher"), (3, "student"), (4, 'no_role'))
    role = models.PositiveSmallIntegerField(choices = choices, blank = True, null = True)

    def getusername(sekf):
        self.user.getusername


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    phone = models.CharField(max_length = 10)
    teacher_id = models.AutoField(primary_key = True)
    email = models.EmailField(max_length = 254, unique = True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'{self.first_name}{self.last_name}'


class Classroom(models.Model):
    class_name = (
        ('A', 'dhmotiko_a'), ('B', 'dhmotiko_b'), ('C', 'dhmotiko_c'), ('D', 'dhmotiko_d'), ('E', 'dhmotiko_e'),
        ('ST', 'dhmotiko_st'), ('GA', 'gymnasio_a'), ('GB', 'gymnasio_b'), ('GC', 'gymnasio_c'), ('LA', 'lykeio_a'),
        ('LB', 'lykeio_b'), ('LC', 'lykeio_c')

    )

    classname = models.CharField(max_length = 2, choices = class_name, default = 'A')
    class_number = models.IntegerField(default = 1)
    maximum = models.IntegerField()
    id = models.AutoField(primary_key = True)
    students_in = models.IntegerField(default = 0)

    class Meta:
        unique_together = (('classname', 'class_number'),)

    def __str__(self):
        return f'{self.classname}{self.class_number}'


class subject(models.Model):
    onoma = models.CharField(max_length = 20)
    teacher = models.ForeignKey(Teacher, on_delete = models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete = models.CASCADE)
    subject_id = models.AutoField(primary_key = True)

    class Meta:
        unique_together = (('onoma', 'classroom'),)

    def __str__(self):
        return f'{self.onoma}{self.classroom}'


class Student(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, blank = True, null = True)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    classroom = models.ForeignKey(Classroom, on_delete = models.CASCADE)
    phone = models.CharField(max_length = 10)
    student_id = models.AutoField(primary_key = True)
    email = models.EmailField(max_length = 254, unique = True)
    created = models.DateTimeField(auto_now_add = True)
    photo = models.ImageField(default = "student_pics/default.png", upload_to = "student_pics")
    apousies = models.IntegerField(default = 0)

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.photo.path)
        if img.height > 184 or img.width > 184:
            outputsize = (184, 184)
            img.thumbnail(outputsize)
            img.save(self.photo.path)

    def __str__(self):
        return f'{self.first_name}{self.last_name}{self.student_id}'


class Grades(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    subject_name = models.ForeignKey(subject, on_delete = models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete = models.CASCADE)
    classroom = models.ForeignKey(Classroom, on_delete = models.CASCADE)
    grade = models.IntegerField(default = 0)
    id = models.AutoField(primary_key = True)

    def __str__(self):
        return f'{self.student.first_name}{self.student.last_name}{self.subject_name.onoma}'

    class Meta:
        unique_together = (('student', 'subject_name'),)


class Assignments(models.Model):
    pdf_question = models.FileField(upload_to = "assigments", blank = True)
    Subject = models.ForeignKey(subject, on_delete = models.CASCADE, blank = True)
    created = models.DateField(auto_now_add = True)
    deadline = models.DateField()
    classroom = models.ForeignKey(Classroom, on_delete = models.CASCADE, blank = True)
    title = models.CharField(max_length = 100)
    question = models.CharField(max_length = 1000, blank = True)
    teacher = models.ForeignKey(Teacher, on_delete = models.CASCADE)
    id = models.AutoField(primary_key = True)

    def __str__(self):
        return f'{self.title} {self.id}'


class StudentAssigments(models.Model):
    student = models.ForeignKey(Student, on_delete = models.CASCADE)
    assignment = models.ForeignKey(Assignments, on_delete = models.CASCADE)
    file = models.FileField(upload_to = "student_assigments", blank = True)
    score = models.IntegerField(default = 1, validators = [MaxValueValidator(100), MinValueValidator(1)], blank = True)

    id = models.AutoField(primary_key = True)

    def __str__(self):
        return f'Student :{self.student.user},{self.assignment.title}'

    class Meta:
        unique_together = (('student', 'assignment'),)


class Announcements(models.Model):
    title = models.CharField(max_length = 50)
    content = models.CharField(max_length = 1000)
    image_post = models.ImageField(upload_to = "post_images", default = "post_images/default.png")
    publisher = models.ForeignKey(User, on_delete = models.CASCADE)
    created = models.DateField(auto_now_add = True)
    id = models.AutoField(primary_key = True)

    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.image_post.path)
        if img.height > 280 or img.width > 340:
            outputsize = (280, 340)
            img.thumbnail(outputsize)
            img.save(self.image_post.path)
