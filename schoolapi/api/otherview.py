from django.http.response import JsonResponse
from base.models import User
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(["GET"])
def get_role(request):
    try:
        return JsonResponse({"role": request.user.role}, status = status.HTTP_200_OK)
    except:
        return JsonResponse({'message': "You dont have permissions"}, status = status.HTTP_401_UNAUTHORIZED)


@api_view(["GET"])
def get_user(request):
    user_id = request.query_params.get("id", None)
    if (user_id):
        user = User.objects.get(id = user_id)
        return JsonResponse({"username": user.username})
    else:
        return JsonResponse({"message": "You need to pass a username"}, status = status.HTTP_400_BAD_REQUEST)
