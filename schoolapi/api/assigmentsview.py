from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from base.models import Student,Assignments,StudentAssigments,subject
from .serializers import AssignmentsSerializer,StudentAssigmentsSerializer
from rest_framework import status
from rest_framework.decorators import api_view,permission_classes

taxh
@api_view(["GET","POST","DELETE"])
def assignments(request):
	if request.method=="GET" and request.user.role != 4 :
		subject_id=request.query_params.get("subject",None)
		id=request.query_params.get("id",None)
		classroom=request.query_params.get("classroom",None)
		if subject_id:
			assigment=Assignments.objects.filter(Subject=subject_id)
		elif classroom and subject_id:
			assigment=Assignments.objects.filter(classroom=classroom,Subject=subject_id)
		elif classroom:
			assigment=Assignments.objects.filter(classroom=classroom)
		elif id:
			assigment=Assignments.objects.filter(id=id)
		else:
			assigment=Assignments.objects.all()
		serializer=AssignmentsSerializer(assigment,many=True)
		return Response(serializer.data)

	if request.user.role==1 or request.user.role==2:
		if request.method=="POST":
			data=request.data
			Subject=subject.objects.get(subject_id=data['Subject'])
			if request.user.role==2:
				if Subject.teacher.user==request.user :
					try:
						new_assigment=Assignments.objects.create(pdf_question=request.FILES,Subject=Subject,deadline=data["deadline"],classroom=Subject.classroom,title=data["title"],question=data['question'])
						new_assigment.save()
					except:
						return JsonResponse({'message':"Bad request"},status=status.HTTP_400_BAD_REQUEST)
				else:
					return JsonResponse({"message":"You dont have permission to add assgment in this subject"},status=status.HTTP_400_BAD_REQUEST)
			else:
				try:
					new_assigment=Assignments.objects.create(pdf_question=request.FILES,Subject=Subject,deadline=data["deadline"],classroom=Subject.classroom,title=data["title"],question=data['question'])
				except:
					return JsonResponse({'message':"Bad request"},status=status.HTTP_400_BAD_REQUEST)
	
			return JsonResponse({'message': 'object created successfully'},status=status.HTTP_201_CREATED)
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
						return JsonResponse({'message':"No permissions"},status=status.HTTP_401_UNAUTHORIZED)
			return JsonResponse({'message': ' assigment  deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
		
	return JsonResponse({'message':"No permissions"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(["PUT"])
def assignments_update(request,id):
	assigment=Assignments.objects.get(id=id)
	if assigment.exists():	
		if request.user.role<3:
			if user.request.role==2:
				if assigment.Subject.teacher.user!=request.user:
					return JsonResponse({'message':"No permissions"},status=status.HTTP_401_UNAUTHORIZED)
			
			data=JSONParser().parse(request)
			serializer=AssignmentsSerializer(assigment,data=data)
			if serializer.is_valid():
				serializer.save()
				return Response(serializer.data)
			return JsonResponse({'message':'Bad request'},status=status.HTTP_400_BAD_REQUEST)
		else:		
			return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_401_UNAUTHORIZED)
	return JsonResponse({'message' : 'Couldnt find assigment with that id'},status=status.HTTP_404_NOT_FOUND)

			
