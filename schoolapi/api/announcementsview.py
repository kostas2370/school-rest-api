from rest_framework.response import Response
from django.http.response import JsonResponse
from base.models import Announcements
from .serializers import AnnouncementsSerializer
from rest_framework import status
from rest_framework.decorators import api_view
import filetype


@api_view(["GET", "POST", "DELETE"])
def announcements(request):
    if request.method == "GET":

        id = request.query_params.get("id", None)

        if id:
            announcements = Announcements.objects.filter(id=id)
        else:
            announcements = Announcements.objects.all()

        seriazer = AnnouncementsSerializer(announcements, many=True)
        return Response(seriazer.data)

    elif request.method == "POST" and (request.user.role < 3):
        data = request.data

        try:

            if (len(request.FILES) > 0) and filetype.is_image(request.FILES["image_post"]):

                announcement = Announcements.objects.create(title=data["title"], content=data["content"],
                                                            image_post=request.FILES["image_post"],
                                                            publisher=request.user)
            else:
                announcement = Announcements.objects.create(title=data["title"], content=data["content"],
                                                            publisher=request.user)

            announcement.save()
            return JsonResponse({'message': "Success"}, status=status.HTTP_201_CREATED)

        except:
            return JsonResponse({'message': "You need to fix the announcement information"},
                                status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE" and (request.user.role < 3):
        announcement_id = request.query_params.get("id", None)

        if not announcement_id and not (Announcements.objects.filter(id=announcement_id)):
            return JsonResponse({'message': "You need to inserd a valid post it"}, status=status.HTTP_401_UNAUTHORIZED)

        announcement = Announcements.objects.get(id=announcement_id)

        if announcement.publisher == request.user or request.user.role == 1:
            announcement.delete()
            return JsonResponse({'message': ' announcement  deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

        else:
            return JsonResponse({'message': "You dont have permissions"}, status=status.HTTP_401_UNAUTHORIZED)

    else:
        return JsonResponse({'message': "You dont have permissions"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(["PUT"])
def announcement_update(request, id):
    if not (Announcements.objects.filter(id=id).exists()):
        return JsonResponse({'message': "You need to inserd a valid post it"}, status=status.HTTP_401_UNAUTHORIZED)

    announcement = Announcements.objects.get(id=id)

    if (announcement.publisher == request.user or request.user.role == 1):
        announcement.title = request.data["title"]
        announcement.content = request.data["content"]
        if len(request.FILES) > 0:
            announcement.image_post = request.FILES["image_post"]

        announcement.save()
        return JsonResponse({'message': "Success"}, status=status.HTTP_201_CREATED)

    else:
        return JsonResponse({'message': "You dont have permissions"}, status=status.HTTP_401_UNAUTHORIZED)
