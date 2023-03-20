from rest_framework.response import Response
from django.http.response import JsonResponse
from base.models import Assignments, subject, Teacher
from .serializers import AssignmentsSerializer, StudentAssigmentsSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes


@api_view(["GET", "POST", "DELETE"])
def assignments(request):
    if request.method == "GET" and request.user.role != 4:
        subject_id = request.query_params.get("subject", None)
        id = request.query_params.get("id", None)
        classroom = request.query_params.get("classroom", None)
        teacher = request.query_params.get("teacher", None)

        if teacher:
            assigment = Assignments.objects.filter(teacher = teacher)

        elif subject_id:
            assigment = Assignments.objects.filter(Subject = subject_id)
        elif classroom and subject_id:
            assigment = Assignments.objects.filter(classroom = classroom, Subject = subject_id)
        elif classroom:
            assigment = Assignments.objects.filter(classroom = classroom)
        elif id:
            assigment = Assignments.objects.filter(id = id)
        else:
            assigment = Assignments.objects.all()
        serializer = AssignmentsSerializer(assigment, many = True)
        return Response(serializer.data)

    if request.user.role == 1 or request.user.role == 2 and request.method == "POST":
        data = request.data
        Subject = subject.objects.get(subject_id = data['Subject'])

        if Subject.teacher.user != request.user and request.user.role != 1:
            return JsonResponse({"message": "You dont have permission to add assgment in this subject"},
                                status = status.HTTP_400_BAD_REQUEST)

        try:
            new_assigment = Assignments.objects.create(teacher = Subject.teacher, pdf_question = request.FILES['file'],
                                                       Subject = Subject, deadline = data["deadline"],
                                                       classroom = Subject.classroom, title = data["title"],
                                                       question = data['question'])
            new_assigment.save()
        except :
            return JsonResponse({'message': "Bad request"}, status = status.HTTP_400_BAD_REQUEST)

        return JsonResponse({'message': 'object created successfully'}, status = status.HTTP_201_CREATED)

    elif request.user.role == 1 or request.user.role == 2 and request.method == "DELETE":
        id = request.query_params.get("id", None)
        if id == None:
            return JsonResponse({'message': "You need to add id param"}, status = status.HTTP_400_BAD_REQUEST)

        if not (Assignments.objects.filter(id = id).exists()):
            return JsonResponse({'message': "There is not an assgment with this id"},
                                status = status.HTTP_400_BAD_REQUEST)

        assigment = Assignments.objects.get(id = id)

        if assigment.Subject.teacher.user != request.user and request.user.role != 1:
            return JsonResponse({'message': "No permissions"}, status = status.HTTP_401_UNAUTHORIZED)

        assigment.delete()

        return JsonResponse({'message': ' assigment  deleted successfully!'}, status = status.HTTP_204_NO_CONTENT)

    return JsonResponse({'message': "No permissions"}, status = status.HTTP_401_UNAUTHORIZED)


@api_view(["PUT"])
def assignments_update(request, id):
    data = request.data
    if (request.user.role == 2):
        teacher = Teacher.objects.get(user = request.user)
        assigment = Assignments.objects.get(id = id, teacher = teacher)

    elif (request.user.role == 1):
        assigment = Assignments.objects.get(id = id)

    else:

        return JsonResponse({'message': "No permissions"}, status = status.HTTP_401_UNAUTHORIZED)

    try:

        if len(request.FILES) > 0:
            assigment.pdf_question = request.FILES["file"]

        assigment.deadline = data["deadline"]
        assigment.title = data["title"]
        assigment.question = data["question"]
        subj = subject.objects.get(subject_id = data["Subject"])
        assigment.Subject = subj
        assigment.save()
        return JsonResponse({'message': ' assigment  updated successfully!'}, status = status.HTTP_201_CREATED)

    except:
        return JsonResponse({'message': "Couldn't find that Student"}, status = status.HTTP_400_BAD_REQUEST)
