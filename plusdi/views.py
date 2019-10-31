from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from api.models import Workout
from django.contrib.auth import authenticate
from jose import jwt
from django.conf import settings
import json

# Create your views here.


@api_view(['POST'])
@permission_classes((AllowAny,))
def test(request):
    data = {"message": "test completed"}
    try:
        data = {""}
    except Exception as e:
        data["error"] = str(e)

    return Response(data)
