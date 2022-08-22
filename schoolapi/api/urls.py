from django.urls import path


from . import views 

urlpatterns= [ 
path('student/',views.students),
path('student/update/',views.student_update),
path('student/update/<int:id>/',views.student_update),

path('classroom/',views.classroom),
path('classroom/update/<int:id>/',views.classroom_update),

path('grade/',views.grade),
path('grade/update/<int:id>/',views.grade_update),

path('subject/',views.SSubject),
path('subject/update/<int:id>/',views.subject_update),

path('teacher/',views.teacher),

]