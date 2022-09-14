from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from base.models import Student,Assignments,StudentAssigments
from .serializers import AssignmentsSerializer,StudentAssigmentsSerializer
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes


@api_view(["GET","POST","DELETE"])
def assignments(request):
	if request.method=="GET" :
		subject_id=request.query_params.get("subject",None)
		id=request.query_params.get("id",None)
		classroom=request.query_params.get("classroom",None)
		if subject_id:
			assignment=Assignments.objects.filter(Subject=subject_id)
		elif classroom and subject_id:
			assigment=Assignments.objects.filter(classroom=classroom,Subject=subject_id)
		elif classroom:
			assigment=Assignments.objects.filter(classroom=classroom)
		elif id:
			assigment=Assignments.objects.filter(id=id)
		else:
			assigment=Assignments.objects.all()
		serializer=AssignmentsSerializer(assigment,many=True)
		return Response(serializer)

	if request.user.role==1 or request.user.role==2:
		if request.method=="POST":
			data=request.data
			Subject=subject.objects.get(subject_id=data['subject_id'])
			if request.user.role==2:
				if Subject.teacher.user==request.user :
					try:
						new_assigment=Assignments.objects.create(pdf_question=request.FILES[0],Subject=Subject,deadline=data["deadline"],classroom=Subject.classroom,title=data["title"],question=data['question'])
						new_assigment.save()
					except:
						return JsonResponse({'message':"Bad request"},status=status.HTTP_400_BAD_REQUEST)
				else:
					return JsonResponse({"message":"You dont have permission to add assgment in this subject"},status=status.HTTP_400_BAD_REQUEST)
			else:
				try:
					new_assigment=Assignments.objects.create(pdf_question=request.FILES[0],Subject=Subject,deadline=data["deadline"],classroom=Subject.classroom,title=data["title"],question=data['question'])
				except:
					return JsonResponse({'message':"Bad request"},status=status.HTTP_400_BAD_REQUEST)
	

		elif request.method=="DELETE":
			id=request.query_params.get("id",None)
			if id == None:
				return JsonResponse({'message':"You need to add id param"},status=status.HTTP_400_BAD_REQUEST)

			assigment=Assignments.objects.get(id=id)
			if assigment.exists():
				pass
			else:
				return JsonResponse({'message':"Not found"},status=status.HTTP_404_NOT_FOUND)

			if request.user.role==1:	
				assigment.delete()		
			else:				
					if assigment.Subject.teacher.user==request.user :	
						assigment.delete()
					else:
						return JsonResponse({'message':"No permissions"},status=status.HTTP_400_BAD_REQUEST)
			return JsonResponse({'message': ' assigment  deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
		else:
			return JsonResponse({'message':"No permissions"},status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def assignments_update(request,id):