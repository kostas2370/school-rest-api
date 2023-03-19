from base.models import Student, Classroom, Teacher, User
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .serializers import StudentSerializer


@api_view(['GET', 'POST', 'DELETE'])
def students(request):
    if request.method == "GET":
        if request.user.role == 1 or request.user.role == 2:

            # Getting the request_query parameters
            student_id = request.query_params.get("student_id", None)
            classroom = request.query_params.get("classroom", None)

            # Filtering Data depending on our parameters

            if student_id:
                students = Student.objects.filter(student_id = student_id)

            elif classroom:
                students = Student.objects.filter(classroom = classroom)
            else:
                students = Student.objects.all()

            # returning our formmated data
            serializer = StudentSerializer(students, many = True)
            return Response(serializer.data)

        # If the request user has the student role it returns its own info
        elif request.user.role == 3:
            students = Student.objects.filter(user = request.user)
            serializer = StudentSerializer(students, many = True)
            return Response(serializer.data)

        # if the user doesnt have role it returns an error
        else:
            return JsonResponse({'message': "You dont have permissions"}, status = status.HTTP_401_UNAUTHORIZED)

    # ______post_______
    elif request.method == "POST":

        data = request.data

        # IF user role is school manager the new user will be the user that admin selected from the json file
        if request.user.role == 1:
            try:
                new_user = User.objects.get(username = request.data['user'])
            except:
                return JsonResponse({'message': "You need to add user in ur json form"},
                                    status = status.HTTP_400_BAD_REQUEST)

        # if request user role is no role it will put as a user itsself if there is no row in teacher table
        # with the same user
        elif request.user.role == 4:
            new_user = request.user

            if not Teacher.objects.filter(user = new_user).count() :
                new_user.role = 3

            else:
                return JsonResponse({'message': "You already are a student"}, status = status.HTTP_400_BAD_REQUEST)

                # if the user has other role than no role or admin
        else:

            return JsonResponse({'message': "You are already registered!"}, status = status.HTTP_400_BAD_REQUEST)

            # We check if we have files in our request to add the photo profile of the teacher

        classroom = Classroom.objects.get(id = (data['classroom']))

        try:
            if (len(request.FILES) > 0):
                new_student = Student.objects.create(user = new_user, photo = request.FILES["photo"],
                                                     first_name = data["first_name"], last_name = data["last_name"],
                                                     classroom = classroom, phone = data["phone"],
                                                     email = data["email"], apousies = 0)
            else:
                new_student = Student.objects.create(user = new_user, first_name = data["first_name"],
                                                     last_name = data["last_name"], classroom = classroom,
                                                     phone = data["phone"], email = data["email"], apousies = 0)

        except:
            return JsonResponse({'message': "You need to fix the student information"},
                                status = status.HTTP_400_BAD_REQUEST)

            # We get the amount of students in the classroom
        classroom = Classroom.objects.get(id = int(request.data["classroom"]))
        classroom.students_in = Student.objects.filter(classroom = int(request.data["classroom"])).count()

        # We check if there is free space in the class, and if we have free space we register the student succesfully ,
        # otherwise we delete the student
        if classroom.students_in <= classroom.maximum:

            classroom.save()
            new_user.save()
            serializer = StudentSerializer(new_student)
            return Response(serializer.data)
        else:
            student = Student.objects.get(student_id = serializer.data["student_id"])
            student.delete()
            return JsonResponse({'message': "You can't add more students in this classroom"},
                                status = status.HTTP_400_BAD_REQUEST)

    # _______________________DELETE____________________________
    elif request.method == "DELETE" and request.user.role == 1:
        # We get the student user id from query params
        student_id = request.query_params.get("student_id", None)

        try:
            # we delete the student
            student = Student.objects.get(student_id = student_id)

            # we delete the user
            user = User.objects.get(id = student.user.id)
            user.delete()
            student.delete()
            # we update the info of the classroom

            classroom = Classroom.objects.get(id = student.classroom.id)
            classroom.students_in = Student.objects.filter(classroom = student.classroom.id).count()
            classroom.save()

            return JsonResponse({'message': ' Student  deleted successfully!'}, status = status.HTTP_204_NO_CONTENT)

        except:
            return JsonResponse({'message': ' Student not found'}, status = status.HTTP_404_NOT_FOUND)

            # if the user's role is other than school manager it returns an aunauthorized error
    else:
        return JsonResponse({'message': "You dont have permissions"}, status = status.HTTP_401_UNAUTHORIZED)


# _____________________Update_____________
@api_view(['PUT'])
def student_update(request, id=''):
    """
    if the user role is school Manager and we
    have put an id in our link we get the id an get the user object,their classroom id and their apousies
    """
    if request.user.role == 1 and id != '':

        try:
            student = Student.objects.get(student_id = id)
            classs = student.classroom.id
        except:
            return JsonResponse({'message': ' Student not found'}, status = status.HTTP_404_NOT_FOUND)

        # we parse our request as a json and we put it in our seriallizer for studentss
        data = JSONParser().parse(request)
        serializer = StudentSerializer(student, data = data)

        # we check if the seriallizer is valid
        if not (serializer.is_valid()):
            return JsonResponse({'message': ' Bad request'}, status = status.HTTP_400_BAD_REQUEST)

        serializer.save()

        # we check if the school manager changed students class
        if classs != serializer.data['classroom']:
            taxh = Classroom.objects.get(id = classs)
            taxh2 = Classroom.objects.get(id = serializer.data['classroom'])
            taxh.students_in -= 1
            taxh2.students_in = Student.objects.filter(classroom = serializer.data['classroom']).count()
            if taxh2.maximum < taxh2.students_in:
                student.classroom = taxh
                student.save()
            else:
                taxh.save()
                taxh2.save()
        return JsonResponse({'message': ' Student  UPDATED successfully!'}, status = status.HTTP_204_NO_CONTENT)

    # if the students wanna change its own information
    elif request.user.role == 3:
        student = Student.objects.get(user = request.user)
        request.data._mutable = True
        data = request.data

        # we do this to not let the students change their classroom and their apousies

        try:
            student.email = data["email"]
            student.first_name = data["first_name"]
            student.last_name = data["last_name"]
            student.phone = data["phone"]
            if len(request.FILES) > 0:
                student.photo = request.FILES["photo"]
            student.save()

            return JsonResponse({'message': ' Student  UPDATED successfully!'}, status = status.HTTP_204_NO_CONTENT)
        except:

            return JsonResponse({'message': ' Bad request'}, status = status.HTTP_400_BAD_REQUEST)

    else:
        return JsonResponse({'message': "You dont have permissions"}, status = status.HTTP_401_UNAUTHORIZED)
