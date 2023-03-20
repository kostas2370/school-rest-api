from django.contrib import admin
from .models import User
from .models import Student,Subject,Classroom,Teacher,Grades,Assignments,StudentAssigments,Announcements
admin.site.register(Student)
admin.site.register(Subject)
admin.site.register(Classroom)
admin.site.register(Teacher)
admin.site.register(Grades)
admin.site.register(User)
admin.site.register(Assignments)
admin.site.register(StudentAssigments)
admin.site.register(Announcements)