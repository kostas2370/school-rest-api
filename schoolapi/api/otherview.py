from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from base.models import User
from rest_framework.decorators import api_view

from rest_framework import status
@api_view(["GET"])
def get_role(request):
	try:
		return JsonResponse ({"role":request.user.role},status =status.HTTP_200_OK)
	except exception :
		return JsonResponse ({'message':"You dont have permissions"},status =status.HTTP_401_UNAUTHORIZED)

