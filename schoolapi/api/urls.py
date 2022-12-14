from django.urls import path


from . import teacherview,studentview,classview ,gradeview,subjectview,assigmentsview,studentassignview,otherview

urlpatterns= [ 
path('student/',studentview.students),
path('student/update/',studentview.student_update),
path('student/update/<int:id>/',studentview.student_update),
path('classroom/',classview.classroom),
path('classroom/update/<int:id>/',classview.classroom_update),
path('grade/',gradeview.grade),
path('grade/update/<int:id>/',gradeview.grade_update),
path('subject/',subjectview.SSubject),
path('subject/update/<int:id>/',subjectview.subject_update),
path('teacher/',teacherview.teacher),
path('teacher/update',teacherview.teacher_update),
path('assigment/',assigmentsview.assignments),
path('assigment/update/<int:id>',assigmentsview.assignments_update),
path('student/assigment/addgrade/<int:id>',studentassignview.student_assigment_add_grade),
path('student/assigment/',studentassignview.studentassigment),
path('getrole/',otherview.get_role)
 ]