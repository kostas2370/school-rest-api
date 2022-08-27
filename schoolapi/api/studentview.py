from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser

from base.models import Student,subject,Grades,Classroom,Teacher,User
from .serializers import StudentSerializer

from rest_framework import status
from rest_framework.decorators import api_view


@api_view(['GET','POST','DELETE'])
def students(request):	
	if request.method=="GET":
			if request.user.role==1 or request.user.role==2:
				first_name = request.query_params.get("first_name",None)
				student_id=request.query_params.get("student_id",None)
				last_name=request.query_params.get("last_name",None)
				classroom=request.query_params.get("classroom",None)
				
				if student_id  :
					students=Student.objects.filter(student_id=student_id)
				elif first_name and last_name and classroom:
					students=Student.objects.filter(first_name=first_name,last_name=last_name,taxh=classroom)		 
				elif first_name and last_name:
					students=Student.objects.filter(first_name=first_name,last_name=last_name)
				elif classroom:
					students=Student.objects.filter(taxh=classroom)
				elif last_name:
					students=Student.objects.filter(last_name=last_name)
				elif first_name:
					students=Student.objects.filter(first_name=first_name)
				else:
					students=Student.objects.all()
					print(request.user.username)
				
				serializer=StudentSerializer(students,many=True)
				return Response(serializer.data)
			



			elif request.user.role==3: 
				students=Student.objects.get(user=request.user)
				serializer=StudentSerializer(students)
				return Response(serializer.data)
			else:
				return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)
	elif request.method=="POST":
			
				data=request.data
				if request.user.role==1 :
					try:
						user_id=request.data['user']
						new_user=User.objects.get(username=user_id)
					except:
						return JsonResponse({'message':"You need to add user in ur json form"},status=status.HTTP_400_BAD_REQUEST)			
				elif request.user.role ==4:
					new_user=request.user
					teacher=Teacher.objects.filter(user=new_user).count()
					if teacher==0:
						new_user.role=3
						
					else:
						return JsonResponse({'message':"You already are a teacher"},status=status.HTTP_400_BAD_REQUEST)			
				else:
						return JsonResponse({'message':"You already are a studentr"},status=status.HTTP_400_BAD_REQUEST)			

				taxh=Classroom.objects.get(id=data['classroom'])
				try:
					new_student=Student.objects.create(user=new_user,first_name=data["first_name"],last_name=data["last_name"],taxh=taxh,phone=data["phone"],email=data["email"],apousies=0)
				except:
					return JsonResponse({'message':"You need to fix the student information"},status=status.HTTP_400_BAD_REQUEST)	
				
				classroom=Classroom.objects.get(id=request.data["classroom"])
				classroom.students_in=Student.objects.filter(taxh=request.data["classroom"]).count()
				if classroom.students_in <= classroom.maximum :
						
						classroom.save()
						new_user.save()
						serializer=StudentSerializer(new_student)
						return Response(serializer.data)
				else: 
						student=Student.objects.get(student_id=serializer.data["student_id"])
						student.delete()
						return JsonResponse({'message':"You can't add more students in this classroom"},status=status.HTTP_400_BAD_REQUEST)
			
				
	
	elif request.method=="DELETE":
		if request.user.role==1 :
			student_id=request.query_params.get("student_id",None)
			try:
				student=Student.objects.get(student_id=student_id)
				classroom=Classroom.objects.get(id=student.taxh.id)
				classroom.students_in=Student.objects.filter(taxh=student.taxh.id).count()
				classroom.save()
				student.delete()
				return JsonResponse({'message': ' Student  deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
	
			except:
					return JsonResponse({'message': ' Student not found'}, status=status.HTTP_404_NOT_FOUND)		
		else:
			return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def student_update(request,id=''):
	if request.user.role==1 and id!='':
			
		try:
			student=Student.objects.get(student_id=id)
			classs=student.taxh.id
			apous=student.apousies
		except :
			return JsonResponse({'message': ' Student not found'}, status=status.HTTP_404_NOT_FOUND)
		
			
		data=JSONParser().parse(request)
		serializer=StudentSerializer(student,data=data)
		if serializer.is_valid():
			serializer.save()
			if classs!=serializer.data['taxh']:
				taxh=Classroom.objects.get(id=classs)
				taxh2=Classroom.objects.get(id=serializer.data['taxh'])
				taxh.students_in-=1
				taxh2.students_in=Student.objects.filter(taxh=serializer.data['taxh']).count()
				if taxh2.maximum < taxh2.students_in:
					student.taxh=taxh
					if request.user.role==3:
						student.apousies=apous
					student.save()
				else:
					taxh.save()
					taxh2.save()
			return JsonResponse({'message': ' Student  UPDATED successfully!'}, status=status.HTTP_204_NO_CONTENT)
	
		
			
		return JsonResponse({'message': ' Bad request'}, status=status.HTTP_400_BAD_REQUEST)
	else:
		return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)
