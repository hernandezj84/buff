from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from plusdi.models import Discount
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


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def post_discount(request):
    data = {}
    try:
        token = request.auth
        user = Token.objects.get(key=token)
        discount = Discount.objects.filter(user=user.user)
        if len(discount) == 0:
            discount = Discount()
            discount.discount = request.data
            discount.user = user.user
            discount.save()
        else:
            discount = discount[0]
            discount.discount = request.data
            discount.user = user.user
            discount.save()
        data["message"] = "{} user upload discount sucess".format(user.user)
    except Exception as e:
        data["error"] = str(e)
    return Response(data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_discount(request):
    data = {}

    try:
        token = request.auth
        user = Token.objects.get(key=token)
        discount = Discount.objects.get(user=user.user)
        data["data"] = discount.discount
    except:
        data["error"] = "User not found"
    return Response(data)
