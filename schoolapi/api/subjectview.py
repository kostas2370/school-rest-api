
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from base.models import subject
from .serializers import SubjectSerializer
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(["GET","POST","DELETE"])
def SSubject(request):
	
		if request.method=="GET":
				
				teacher=request.query_params.get("teacher",None)
				onoma=request.query_params.get("onoma",None)
				classroom=request.query_params.get("classroom",None)
				subject_id=request.query_params.get("subject_id",None)
				if teacher  :
					Subject = subject.objects.filter(teacher=teacher)
					
				elif onoma  and classroom :
					Subject = subject.objects.filter(onoma=onoma,classroom=classroom)	
			
				elif onoma  :
					Subject = subject.objects.filter(onoma=onoma)	
				
				elif subject_id :
					Subject = subject.objects.filter(subject_id=subject_id)					
				else :
					Subject = subject.objects.all()
	
				serializer=SubjectSerializer(Subject,many=True)
				return Response(serializer.data)
			
		As
		elif request.user.role==1 and request.method != "GET":
			if request.method=="POST":
					serializer=SubjectSerializer(data=request.data)
					
					if serializer.is_valid():			
						serializer.save()
					return Response(serializer.data)
		
		
			elif request.method=="DELETE":
					subject_id=request.query_params.get("subject_id",None)
					try:
						Subject =subject.objects.get(subject_id=subject_id)
						Subject.delete()
						return JsonResponse({'message': ' Subject  deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
					except:
						return JsonResponse({'message' : 'Couldnts find Subject with that id'},status=status.HTTP_404_NOT_FOUND)
		else:

			return JsonResponse({'message':"You dont have permission"},status=status.HTTP_401_UNAUTHORIZED)

@api_view(["PUT"])
def subject_update(request,id):
	if request.user.role==1:
		
		subj=subject.objects.get(subject_id=id)
		
		if subj==[]:
			return JsonResponse({'message':'Subject not found'},status=status.HTTP_404_NOT_FOUND)
		
		data=JSONParser().parse(request)
		serializer=SubjectSerializer(subj,data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
	
		return JsonResponse({'message':'Bad request'},status=status.HTTP_400_BAD_REQUEST)
	else:
		return JsonResponse({'message':"You dont have permissions"},status=status.HTTP_401_UNAUTHORIZEDT)

