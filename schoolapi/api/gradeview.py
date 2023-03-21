from base.models import Subject, Grades, Teacher, Student
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from .serializers import GradesSerializer
from rest_framework import status
from rest_framework.decorators import api_view
import pandas as pd

@api_view(["GET"])
def grade(request):
    if request.method == "GET":
        student = request.query_params.get("student", None)
        subj = request.query_params.get("subject_name", None)
        classroom = request.query_params.get("classroom", None)

        if request.user.role == 1:
            if classroom:
                grades = Grades.objects.filter(classroom = classroom)
            elif student and subj:
                grades = Grades.objects.filter(student = student, subject_name = subj)
            elif subj:
                grades = Grades.objects.filter(subject = subj)
            elif student:
                grades = Grades.objects.filter(student = student)
            else:
                grades = Grades.objects.all()

        elif request.user.role == 2:
            teacher = Teacher.objects.get(user = request.user)

            if student:
                grades = Grades.objects.filter(teacher = teacher.teacher_id, student = student)

            elif classroom:
                grades = Grades.objects.filter(teacher = teacher.teacher_id, classroom = classroom)

            elif subj:
                grades = Grades.objects.filter(teacher = teacher.teacher_id, subject_name = Subject)

            else:
                grades = Grades.objects.filter(teacher = teacher.teacher_id)

        elif request.user.role == 3:
            global Student
            stud = Student.objects.get(user = request.user)
            if subj:
                grades = Grades.objects.filter(student = stud, subject_name = subj)
            elif classroom:
                grades = Grades.objects.filter(student = stud, classroom = classroom)
            else:
                grades = Grades.objects.filter(student = stud)
        else:
            return JsonResponse({'message': "You dont have permissions"}, status = status.HTTP_401_UNAUTHORIZED)

        serializer = GradesSerializer(grades, many = True)

        return Response(serializer.data)


@api_view(["PUT"])
def grade_update(request, id):
    if request.user.role == 1:
        grade = Grades.objects.get(id = id)
    elif request.user.role == 2:
        grade = Grades.objects.get(id = id, teacher = request.user)
    else:
        return JsonResponse({'message': "You dont have permissions"}, status = status.HTTP_401_UNAUTHORIZED)

    if grade:
        data = JSONParser().parse(request)
        serializer = GradesSerializer.parse(grade, data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    return JsonResponse({'message': 'Bad request'}, status = status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def add_through_csv(request):
    data = request.data
    subj = Subject.objects.get(subject_id = data["subject_id"])

    if subj.teacher.user != request.user:
        return JsonResponse({"message": f"No permissions"}, status = status.HTTP_401_UNAUTHORIZED)

    df = pd.read_excel(request.FILES["file"])
    if list(df.columns) != ["ids", "grade"]:
        return JsonResponse({
                                "message": "Wrong excel format , you need to have 2 headers titles ids for students "
                                           " grade for the grade"
        },
                            status = status.HTTP_400_BAD_REQUEST)

    for index, row in df.iterrows():
        ids = row.get("ids")
        if not Student.objects.filter(student_id = row["ids"]).exists():
            return JsonResponse({"message": f"Student with id : {ids} does not exists"},
                                status = status.HTTP_400_BAD_REQUEST)

        stud = Student.objects.get(student_id = ids)

        if stud.classroom != subj.classroom:
            return JsonResponse({"message": f"Student with id : {ids} is not in the subject's classroom"},
                                status = status.HTTP_400_BAD_REQUEST)

        if Grades.objects.filter(student = stud, subject_name = subj).exists() and not pd.isna(row["grade"]):

            grad = Grades.objects.get(student = stud, subject_name = subj)
            grad.grade = row.get("grade")
            grad.save()

            continue

        if pd.isna(row["grade"]):
            row["grade"] = 0

        grad = Grades.objects.create(student = stud, subject_name = subj, teacher = subj.teacher,
                                      classroom = subj.classroom, grade = row["grade"])
        grad.save()
    return JsonResponse({'message': ' Grades  added successfully!'}, status = status.HTTP_200_OK)
