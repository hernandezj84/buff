from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from plusdi.models import Discount
from django.contrib.auth import authenticate
from jose import jwt
from django.conf import settings
import json
from plusdi.jwt_helper import JwtHelper
from plusdi.user_helper import UserHelper
from django.db import IntegrityError

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


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_commerce(request):
    data = {}
    try:
        jwt = JwtHelper()
        post_data = jwt.decode_data(request.data["data"])
        user_helper = UserHelper()
        commerce = user_helper.create_commerce(
            post_data["email"], post_data["password"])
        data["data"] = jwt.encode_data({"token": commerce[0].key})
    except IntegrityError:
        data["error"] = "Error: User already registered"
    except Exception as error:
        data["error"] = "Error {}".format(str(error))
    return Response(data)


@api_view(['POST'])
@permission_classes((AllowAny))
def login_commerce(request):
    data = {}
    try:
        jwt = JwtHelper()
        user_helper = UserHelper()
        post_data = jwt.decode_data(request.data["data"])
        if authenticate(username=post_data["email"], password=post_data["password"]):
            commerce = User.objects.get(username=post_data["email"])
            data["data"] = jwt.encode_data(
                {"token": user_helper.get_token(commerce)[0].key})
    except Exception as error:
        data["error"] = "Error: {}".format(error)

    return Response(data)
