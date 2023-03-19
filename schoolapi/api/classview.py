from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from base.models import Classroom
from .serializers import ClassroomSerializer
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes


@api_view(['GET', 'POST', 'DELETE'])
def classroom(request):
    if request.method == "GET":
        id = request.query_params.get("id", None)
        classname = request.query_params.get("classname", None)
        class_number = request.query_params.get("class_number", None)

        if id:
            classroom = Classroom.objects.filter(id = id)
        elif classname and class_number:
            classroom = Classroom.objects.filter(classname = classname, class_number = class_number)
        elif classname:
            classroom = Classroom.objects.filter(classname = classname)
        else:
            classroom = Classroom.objects.all()

        serializer = ClassroomSerializer(classroom, many = True)
        return Response(serializer.data)
    if request.user.role == 1:

        if request.method == "POST":
            serializer = ClassroomSerializer(data = request.data)

            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)

        elif request.method == "DELETE":

            id = request.query_params.get("id", None)

            classroom = Classroom.objects.get(id = id)
            if classroom.exists():
                classroom.delete()
                return JsonResponse({'message': ' Student  deleted successfully!'}, status = status.HTTP_204_NO_CONTENT)

            return JsonResponse({'message': 'Couldnts find classroom with that id'}, status = status.HTTP_404_NOT_FOUND)
    return JsonResponse({'message': "You dont have permissions"}, status = status.HTTP_401_UNAUTHORIZED)


@api_view(["PUT"])
def classroom_update(request, id):
    if request.user.role == 1:

        classe = Classroom.objects.get(id = id)
        if not classe.exists():
            return JsonResponse({'message': 'Couldnt find a class with that id'}, status = status.HTTP_404_NOT_FOUND)

        data = JSONParser().parse(request)
        serializer = ClassroomSerializer(classe, data = data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return JsonResponse({'message': 'Bad request'}, status = status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse({'message': "You dont have permissions"}, status = status.HTTP_401_UNAUTHORIZED)
