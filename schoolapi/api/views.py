from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from base.models import Student,subject,Grades,Classroom
from .serializers import StudentSerializer,TeacherSerializer,ClassroomSerializer,GradesSerializer,SubjectSerializer
from django.contrib.auth.models import User
from rest_framework import status
@api_view(['GET','POST','DELETE'])
def students(request):
	
	if request.method=="GET":
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
		
			
			serializer=StudentSerializer(students,many=True)
			return Response(serializer.data)
			
	elif request.method=="POST":
			serializer=StudentSerializer(data=request.data)
			
			if serializer.is_valid():			
					serializer.save()
					classroom=Classroom.objects.get(id=serializer.data["taxh"])
					classroom.students_in=Student.objects.filter(taxh=serializer.data["taxh"]).count()
					if classroom.students_in <= classroom.maximum :
							
							classroom.save()
							return Response(serializer.data)
					else: 
							student=Student.objects.get(student_id=serializer.data["student_id"])
							student.delete()
							return JsonResponse({'message':"You can't add more students in this classroom"},status=status.HTTP_400_BAD_REQUEST)
	elif request.method=="DELETE":
		
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
	

@api_view(['PUT'])
def student_update(request,id):
	try:
		student=Student.objects.get(student_id=id)
		classs=student.taxh.id
		
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
				student.save()
			else:
				taxh.save()
				taxh2.save()
		return JsonResponse({'message': ' Student  UPDATED successfully!'}, status=status.HTTP_204_NO_CONTENT)


	
	return JsonResponse({'message': ' Bad request'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST','DELETE'])
def classroom(request):
	if request.method=="GET":
			id = request.query_params.get("id",None)
			classname=request.query_params.get("classname",None)
			class_number=request.query_params.get("class_number",None)
			
			if id  :
				classroom = Classroom.objects.filter(id=id)
			elif classname  and class_number :
				classroom = Classroom.objects.filter(classname=classname)
			elif classname  and class_number :
				classroom = Classroom.objects.filter(classname=classname,class_number=class_number)
			else :
				classroom = Classroom.objects.all()
			
			
			serializer=ClassroomSerializer(classroom,many=True)
			return Response(serializer.data)
	elif request.method=="POST":
			serializer=ClassroomSerializer(data=request.data)
	
			if serializer.is_valid():			
				serializer.save()
			return Response(serializer.data)

	elif request.method=="DELETE":

			id=request.query_params.get("id",None)
			try:
				classroom =Classroom.objects.get(id=id)
				classroom.delete()
				return JsonResponse({'message': ' Student  deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
			except:
				return JsonResponse({'message' : 'Couldnts find classroom with that id'},status=status.HTTP_404_NOT_FOUND)




@api_view(["PUT"])
def classroom_update(request,id):
	try:
		classe=Classroom.objects.get(id=id)
	except:
		return JsonResponse({'message' : 'Couldnt find a class with that id'},status=status.HTTP_404_NOT_FOUND)

	data=JSONParser.parse(request.data)
	serializer=ClassroomSerializer(classe,data=data)

	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data)

	return JsonResponse({'message':'Bad request'},status=status.HTTP_400_BAD_REQUEST)





@api_view(["GET","POST","DELETE"])
def grade(request):
	if request.method=="GET":
			grade_id=request.query_params.get("id",None)
			student=request.query_params.get("student",None)
			Subject=request.query_params.get("subject_name",None)
			classroom=request.query_params.get("classroom",None)
			
			if classroom:
				grades=Grades.objects.filter(classroom=classroom)

			elif student and Subject :
				grades = Grades.objects.filter(student=student,subject_name=Subject)			

			elif student  :
				grades = Grades.objects.filter(student=student)
				
			elif grade_id:
				grades=Grades.objects.filter(id=grade_id)
			else :
				grades = Grades.objects.all()
		
			serializer=GradesSerializer(grades,many=True)
			return Response(serializer.data)	

	elif request.method=="POST":
			serializer=GradesSerializer(data=request.data)
			
			if serializer.is_valid():			
				
				student=Student.objects.get(student_id=request.data["student"])
				sub=subject.objects.get(subject_id=request.data["subject_name"])
				if student.taxh==sub.taxh:
						serializer.data["classroom"]=student.taxh
						serializer.save()
						return Response(serializer.data)
				else:
						return JsonResponse({"message":"This subject is not in student classroom"},status=status.HTTP_400_BAD_REQUEST)
			return JsonResponse({"message":"This grade already exists"},status=status.HTTP_400_BAD_REQUEST)
	elif request.method=="DELETE":
			id=request.query_params.get("id",None)
			try:
				grades =Grades.objects.get(id=id)
				grades.delete()
				return JsonResponse({'message': ' Grades  deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
			except:
				return JsonResponse({'message' : 'Couldnts find Grades with that id'},status=status.HTTP_404_NOT_FOUND)	


@api_view(["PUT"])
def grade_update(request,id):
	try:
		grade=Grades.objects.get(id=id)
	except:
		return JsonResponse({'message' : 'Couldnt find a Grade with that id'},status=status.HTTP_404_NOT_FOUND)

	data=JSONParser.parse(request.data)	
	serializer=GradesSerializer.parse(grade,data=data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data)

	return JsonResponse({'message':'Bad request'},status=status.HTTP_400_BAD_REQUEST)

	

@api_view(["GET","POST","DELETE"])
def SSubject(request):
	if request.method=="GET":
			
			teacher=request.query_params.get("teacher")
			onoma=request.query_params.get("onoma")
			taxh=request.query_params.get("taxh")
			subject_id=request.query_params.get("subject_id")
			if teacher  :
				Subject = subject.objects.filter(teacher=teacher)
				
			elif onoma  and taxh :
				Subject = subject.objects.filter(onoma=onoma,taxh=taxh)	
		
			elif onoma  :
				Subject = subject.objects.filter(onoma=onoma)	
			
			elif subject_id :
				Subject = subject.objects.filter(subject_id=subject_id)					
			else :
				Subject = subject.objects.all()
		 
			serializer=SubjectSerializer(grades,many=True)
			return Response(serializer.data)
		


	elif request.method=="POST":
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


@api_view(["PUT"])
def subject_update(request,id):
	try:
		subj=subject.objects.get(subject_id=id)
	except:
		return JsonResponse({'message':'Subject not found'},status=status.HTTP_404_NOT_FOUND)

	data=JSONParser.parsers(request.data)
	serializer=SubjectSerializer(subj,data=data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data)

	return JsonResponse({'message':'Bad request'},status=status.HTTP_400_BAD_REQUEST)





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
				teacher=teacher.objects.all()
		
	
			serializer=SubjectSerializer(teacher,many=True)
			return Response(serializer.data)		


	elif request.method=="POST":
			data=request.data
			new_user=User.objects.create(username =data["user"]["username"],password=data["user"]["password"])
			if new_user.is_valid():
				new_user.save()
		
			new_Teacher=Teacher.objects.create(user=new_user,irst_name=data["first_name"],last_name=data["last_name"],phone=data["phone"],email=data["email"])		
			if new_Teacher.is_valid():
				new_Teacher.save()
		
			serializer=TeacherSerializer
			return serializer
	
	elif request.method=="DELETE":
			teacher_id=request.query_params.get("teacher_id",None)
			try:
				teacher =Teacher.objects.get(teacher_id=teacher_id)
				teacher.delete()
				return JsonResponse({'message': ' teacher  deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
			except:
				return JsonResponse({'message' : 'Couldnts find teacher with that id'},status=status.HTTP_404_NOT_FOUND)




@api_view(["PUT"])
def teacher_update(request,id):
	try:
		teacher=Teacher.objects.get(teacher_id=id)
	except:
		return JsonResponse({'message':'Teacher not found'},status=status.HTTP_404_NOT_FOUND)

	data=JSONParser.parsers(request.data)
	serializer=TeacherSerializer(teacher,data=data)
	if serializer.is_valid():
		serializer.save()
		return Response(serializer.data)

	return JsonResponse({'message':'Bad request'},status=status.HTTP_400_BAD_REQUEST)