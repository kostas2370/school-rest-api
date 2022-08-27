from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from base.models import Student,subject,Grades,Teacher
from .serializers import GradesSerializer
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(["GET","POST","DELETE"])
def grade(request):
    if request.method=="GET":
        if request.user.role==1:            
            grade_id=request.query_params.get("id",None)
            student=request.query_params.get("student",None)
            Subject=request.query_params.get("subject",None)
            classroom=request.query_params.get("classroom",None)
            
            if classroom:
                grades=Grades.objects.filter(classroom=classroom)
    
            elif student and Subject :
                grades = Grades.objects.filter(student=student,subject_name=Subject)            
            elif Subject:
                grades = Grades.objects.filter(subject=Subject)
            elif student  :
                grades = Grades.objects.filter(student=student)
                    
            elif grade_id:
                grades=Grades.objects.filter(id=grade_id)
            
            else :
                grades = Grades.objects.all()
            
        elif request.user.role==2:
            teacher=Teacher.objects.get(user=request.user)
            student=request.query_params.get("student",None)
            Subject=request.query_params.get("subject_name",None)
            classroom=request.query_params.get("classroom",None)
            if student and Subject:
                grades=Grades.objects.filter(teacher=teacher.teacher_id,student=student.student_id,subject_name=Subject)
            elif student:
                grades=Grades.objects.filter(teacher=teacher.teacher_id,student=student.student_id)
                    
            elif classroom and Subject :
                grades=Grades.objects.filter(teacher=teacher.teacher_id,classroom=classroom,subject_name=Subject)

            elif Subject :
                grades=Grades.objects.filter(teacher=teacher.teacher_id,subject_name=Subject)
            elif classroom :
                grades=Grades.objects.filter(teacher=teacher.teacher_id,classroom=classroom)    
            else:
                grades=Grades.objects.filter(teacher=teacher.teacher_id)

        elif request.user.role==3:
            student=Student.objects.get(user=request.user)
            
            Subject=request.query_params.get("subject_name",None)
            classroom=request.query_params.get("classroom",None)
            if Subject :
                grades=Grades.objects.filter(student=student,subject_name=Subject)
            elif classroom:
                grades=Grades.objects.filter(student=student,classroom=classroom)
            else:
                grades=Grades.objects.filter(student=student)
        else:
            return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)
    


        serializer=GradesSerializer(grades,many=True)
                
        return Response(serializer.data)    

    elif request.method=="POST":
            if request.user.role==1:
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
            elif request.user.role==2:
                    subject=request.data['subject_name']
                    student=request.data['student']
                    teacher=Teacher.objects.get(user=request.user)
                    Subject=subject.objects.get(subject_id=request.data["subject"])
                    Student=Student.objects.get(student_id=request.data['id'])
                    try:
                        if Subject.taxh ==student.taxh and subject.teacher == teacher.teacher_id :
                            grades=Grades.objects.create(student=student.student_id,subject_name=Subject.subject_id,teacher=teacher.id,classroom=Subject.taxh,grade=request.data["grade"])
                        else :
                            return JsonResponse({"message":"No permissions"},status=status.HTTP_400_BAD_REQUEST)
                    except:
                            return JsonResponse({"message":"Bad request"},status=status.HTTP_400_BAD_REQUEST)

            else:
                    return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)


    elif request.method=="DELETE":
            if request.user.role==1:
                id=request.query_params.get("id",None)
                try:
                    grades =Grades.objects.get(id=id)
                    grades.delete()
                    return JsonResponse({'message': ' Grades  deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)
                except:
                    return JsonResponse({'message' : 'Couldnts find Grades with that id'},status=status.HTTP_404_NOT_FOUND) 
            else:
                return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def grade_update(request,id):
    if request.user.role==1:
            grade=Grades.objects.get(id=id)
    elif request.user.role==2:
            grade=Grades.objects.get(id=id,teacher=request.user)    
    else:
        return JsonResponse({'message':"You dont have authorasation"},status=status.HTTP_400_BAD_REQUEST)
    
    if grade:
        data=JSONParser.parse(request.data) 
        serializer=GradesSerializer.parse(grade,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
    
    return JsonResponse({'message':'Bad request'},status=status.HTTP_400_BAD_REQUEST)