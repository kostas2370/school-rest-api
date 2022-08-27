from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from base.models import Student,subject,Grades,Classroom,Teacher,User
from .serializers import StudentSerializer,TeacherSerializer,ClassroomSerializer,GradesSerializer,SubjectSerializer
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes


@api_view(["GET","POST","DELETE"])
def teacher(request):
	if request.method=="GET":
			first_name=request.query_params.get("first_name",None)
			last_name=request.query_params.get("last_name",None)
			teacher_id=request.query_params.get("teacher_id",None)
			if first_name and last_name:
				teacher = Teacher.objects.filter(first_name=first_name,last_name=last_name)
				
			elif teacher_id :
				teacher = Teacher.objects.filter(teacher_id=teacher_id,last_name=last_name)
			else :
				teacher=Teacher.objects.all()
		
	
			serializer=TeacherSerializer(teacher,many=True)
			return Response(serializer.data)		


	elif request.method=="POST":
			data=request.data
			if request.user.role==4 :
				student=Student.objects.filter(user=request.user).count()
				if student==0:
					new_user=request.user
					new_user.role=2
					
				else:
					return JsonResponse({'message':"You already have a role"},status=status.HTTP_400_BAD_REQUEST)

			elif request.user.role==1:
				user_id=data["user"]
				new_user=User.objects.get(username=user_id)
			elif request.user.role==2:
				 return JsonResponse({'message':"You already are a teacher"},status=status.HTTP_400_BAD_REQUEST)			

			else:
				 return JsonResponse({'message':"You already are a student"},status=status.HTTP_400_BAD_REQUEST)			


			new_Teacher=Teacher.objects.create(user=new_user,first_name=data["first_name"],last_name=data["last_name"],phone=data["phone"],email=data["email"])		
			

			if new_Teacher:
				new_Teacher.save()
				new_user.save()
			serializer=TeacherSerializer(new_Teacher)
			return Response(serializer.data)
	
	elif request.method=="DELETE":
			if request.user.role==2:
				teacher_id=Teacher.objects.get(user=request.user)
			elif request.user.role==1:
				teacher_id=request.query_params.get("teacher_id",None)
			else:
				return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)

			try:
				teacher =Teacher.objects.get(teacher_id=teacher_id)
				teacher.delete()
				return JsonResponse({'message': ' teacher  deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
			except:
				return JsonResponse({'message' : 'Couldnts find teacher with that id'},status=status.HTTP_404_NOT_FOUND)




@api_view(["PUT"])
def teacher_update(request,id):
	if request.user.role==1:
		try:
			teacher=Teacher.objects.get(teacher_id=id)
		except:
			return JsonResponse({'message':'Teacher not found'},status=status.HTTP_404_NOT_FOUND)
	elif request.user.role==2:
		teacher=Teacher.objects.get(user=request.user)
	else:
		return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)

	data=JSONParser.parsers(request.data)
	serializer=TeacherSerializer(teacher,data=data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data)

	return JsonResponse({'message':'Bad request'},status=status.HTTP_400_BAD_REQUEST)