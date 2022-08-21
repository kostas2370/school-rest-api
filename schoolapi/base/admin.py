from django.contrib import admin

from .models import Student,subject,Classroom,Teacher,Grades
admin.site.register(Student)
admin.site.register(subject)
admin.site.register(Classroom)
admin.site.register(Teacher)
admin.site.register(Grades)