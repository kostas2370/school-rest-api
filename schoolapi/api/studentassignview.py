from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from base.models import Student,subject,Grades,Classroom,Teacher,User,StudentAssigments,Assignments
from .serializers import StudentAssigmentsSerializer
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes

@api_view(["GET","POST","DELETE"])
def studentassigment(request):
	if request.method=='GET':
		id=request.query_params.get('id',None)
		Student=request.query_params.get('student',None)
		assigment=request.query_params.get('assigment',None)
		subj=request.query_params.get('subject',None)
		if request.user.role<3:
			if id :
				student_assigment=StudentAssigments.objects.filter(id=id)

			elif student and assigment :
				student_assigment=StudentAssigments.objects.filter(Student=Student,Assignment=assigment)


			elif student:
				student_assigment=StudentAssigments.objects.filter(Student=Student)

			elif assigment:
				student_assigment=StudentAssigments.objects.filter(Assignment=assigment)
			else:
				return JsonResponse({'message':'Bad request , you need to add params'},status=status.HTTP_400_BAD_REQUEST)
		
		elif request.user.role==3:
			stud=Student.objects.get(user=request.user)
			if id:
				student_assigment=StudentAssigments.objects.filter(id=id,student=stud)
			elif assigment:
				student_assigment=StudentAssigments.objects.filter(assigment=assigment,student=stud)
			else:
				student_assigment=StudentAssigments.objects.filter(student=stud)

		else :
			  return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)

		serializer=StudentAssigmentsSerializer(student_assigment,many=True)
		return Response(serializer.data)
	
	elif request.method=="POST":
		serializer=StudentAssigmentsSerializer(data=request.data)
		if serializer.is_valid():
			if request.user.role==1:
			
				serializer.save()
				return Response(serializer.data)
			elif request.user.role == 3:
				if serializer.data["student"] == request.user.Student.id :
					serializer.save()
					return Response(serializer.data)
				else:
					return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)
			else :
					return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)



