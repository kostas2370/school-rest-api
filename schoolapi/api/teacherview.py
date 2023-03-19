from base.models import Student, Teacher, User
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TeacherSerializer


@api_view(["GET", "POST", "DELETE"])
def teacher(request):
    if request.method == "GET":
        first_name = request.query_params.get("first_name", None)
        last_name = request.query_params.get("last_name", None)
        teacher_id = request.query_params.get("teacher_id", None)

        if (request.user.role == 2):
            teacher = Teacher.objects.filter(user = request.user)
        elif first_name and last_name:
            teacher = Teacher.objects.filter(first_name = first_name, last_name = last_name)

        elif teacher_id:
            teacher = Teacher.objects.filter(teacher_id = teacher_id)
        else:
            teacher = Teacher.objects.all()

        serializer = TeacherSerializer(teacher, many = True)
        return Response(serializer.data)

    elif request.method == "POST" and (request.user.role == 1 or request.user.role == 4):
        data = request.data
        student = Student.objects.filter(user = request.user).count()
        if request.user.role == 4 and student == 0:
            new_user = request.user
            new_user.role = 2

        elif request.user.role == 1:
            new_user = User.objects.get(username = data["user"])

        new_Teacher = Teacher.objects.create(user = new_user, first_name = data["first_name"],
                                             last_name = data["last_name"], phone = data["phone"],
                                             email = data["email"])

        if new_Teacher:
            new_Teacher.save()
            new_user.save()

        serializer = TeacherSerializer(new_Teacher)
        return Response(serializer.data)

    elif request.method == "DELETE":
        if request.user.role == 2:
            teacher_id = Teacher.objects.get(user = request.user)
        elif request.user.role == 1:
            teacher_id = request.query_params.get("teacher_id", None)

        else:
            return JsonResponse({'message': "You dont have permission"}, status = status.HTTP_401_UNAUTHORIZED)

        try:
            teacher = Teacher.objects.get(teacher_id = teacher_id)
            teacher.delete()
            return JsonResponse({'message': ' teacher  deleted successfully!'}, status = status.HTTP_204_NO_CONTENT)
        except:
            return JsonResponse({'message': 'Couldnts find teacher with that id'}, status = status.HTTP_404_NOT_FOUND)


@api_view(["PUT"])
def teacher_update(request, id=None):
    data = request.data

    if request.user.role == 1:

        teacher = Teacher.objects.get(teacher_id = id)

    elif request.user.role == 2:
        teacher = Teacher.objects.get(user = request.user)
    else:
        return JsonResponse({'message': "You dont have authorasation"}, status = status.HTTP_401_UNAUTHORIZED)

    try:
        teacher.first_name = data["first_name"]
        teacher.last_name = data["last_name"]
        teacher.phone = data["phone"]
        teacher.email = data["email"]
        teacher.save()

        return JsonResponse({'message': "Success"}, status = status.HTTP_201_CREATED)



    except:
        return JsonResponse({'message': 'Bad request'}, status = status.HTTP_400_BAD_REQUEST)

    return JsonResponse({'message': 'Bad request'}, status = status.HTTP_400_BAD_REQUEST)
