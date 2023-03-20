from base.models import Student, StudentAssigments, Assignments
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import StudentAssigmentsSerializer


@api_view(["GET", "POST", "DELETE"])
def studentassigment(request):
    if request.method == 'GET':
        id = request.query_params.get('id', None)
        student = request.query_params.get('student', None)
        assigment = request.query_params.get('assigment', None)
        if request.user.role < 3:
            if id:
                student_assigment = StudentAssigments.objects.filter(id = id)

            elif student and assigment:
                student_assigment = StudentAssigments.objects.filter(Student = student, assignment = assigment)

            elif student:
                student_assigment = StudentAssigments.objects.filter(Student = student)

            elif assigment:
                student_assigment = StudentAssigments.objects.filter(assignment = assigment)
            else:
                return JsonResponse({'message': 'Bad request , you need to add params'},
                                    status = status.HTTP_400_BAD_REQUEST)

        elif request.user.role == 3:
            stud = Student.objects.get(user = request.user)

            if assigment:
                student_assigment = StudentAssigments.objects.filter(assignment = assigment, student = stud)

            else:
                return JsonResponse({'message': 'Bad request , you need to add params'},
                                    status = status.HTTP_400_BAD_REQUEST)

        else:
            return JsonResponse({'message': "You dont have permissions"}, status = status.HTTP_401_UNAUTHORIZED)

        serializer = StudentAssigmentsSerializer(student_assigment, many = True)
        return Response(serializer.data)

    elif request.method == "POST":

        data = request.data
        assgn = Assignments.objects.get(id = int(data["assignment"]))

        if request.user.role == 3:
            studt = Student.objects.get(user = request.user)

        else:
            studt = Student.objects.get(id = int(data["student"]))

        if request.user.role == 1 or (request.user.role == 3 and studt.classroom == assgn.classroom):
            try:
                new = StudentAssigments.objects.create(student = studt, assignment = assgn,
                                                       file = request.FILES["file"])
                new.save()
                return JsonResponse({'message': "Success"}, status = status.HTTP_200_OK)
            except:
                return JsonResponse({'message': 'Bad request'}, status = status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'message': "You dont have permissions"}, status = status.HTTP_401_UNAUTHORIZED)

    elif request.method == "DELETE":
        id = request.query_params.get('id', None)
        stud = Student.objects.get(user = request.user)
        if not id and not (StudentAssigments.objects.filter(id = id).exists()):
            return JsonResponse({'message': "Couldn't find an stud assign with that id"},
                                status = status.HTTP_400_BAD_REQUEST)

        assigment = StudentAssigments.objects.get(id = id)

        if request.user.role == 1 or (request.user.role == 3 and stud == assigment.student):
            assigment.delete()
            return JsonResponse({'message': ' assigment  deleted successfully!'}, status = status.HTTP_204_NO_CONTENT)
        else:
            return JsonResponse({'message': "You dont have permission"}, status = status.HTTP_400_BAD_REQUEST)

    return JsonResponse({'message': "You dont have authorasation"}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def student_assigment_add_grade(request, id):
    score = request.data["score"]

    if not (StudentAssigments.objects.filter(id = id).exists()):
        return JsonResponse({'message': 'Couldnts find Grades with that id'}, status = status.HTTP_400_BAD_REQUEST)

    assigm = StudentAssigments.objects.get(id = id)

    if (request.user.role == 2 and assigm.assignment.teacher.user == request.user) or request.user.role == 1:
        assigm.score = score
        assigm.save()
        return JsonResponse({'message': 'Score was added succesfully', "new grade ": score},
                            status = status.HTTP_200_OK)

    return JsonResponse({'message': "You dont have authorasation"}, status = status.HTTP_400_BAD_REQUEST)
