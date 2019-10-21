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


@api_view(['GET'])
@permission_classes((AllowAny,))
def test(request):
    return Response({"data": "hello world"})


@api_view(['POST'])
@permission_classes((AllowAny,))
def test_jwt(request):
    data = {}
    try:
        post_data = request.data["data"]
        jwt_decoded = jwt.decode(
            post_data, settings.SECRET_KEY, algorithms=['HS256'])
        data["data"] = jwt_decoded
    except Exception as e:
        data["error"] = str(e)

    return Response(data)


@api_view(['POST'])
@permission_classes((AllowAny),)
def login(request):
    data = {}
    try:
        post_data = request.data["data"]
        jwt_decoded = jwt.decode(
            post_data, settings.SECRET_KEY, algorithms=['HS256'])
        user = User.object.filter(username=jwt_decoded["email"])
        if len(user) == 0:
            # Email does not exists
            user = User.objects.create_user(
                jwt_decoded["email"], jwt_decoded["email"], jwt_decoded["password"])

        else:
            user = user[0]
            if authenticate(username=user.username, password=jwt_decoded["password"]):
                token = Token.objects.get_or_create(user=user)
                data["token"] = token[0].key
            else:
                data["error"] = "Email / password invalid"

    except:
        data["error"] = "User not found"
    return Response(data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_workout(request):
    data = {}

    try:
        token = request.auth
        user = Token.objects.get(key=token)
        workout = Workout.objects.get(user=user.user)
        data["data"] = workout.workout
    except:
        data["error"] = "User not found"
    return Response(data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def post_workout(request):
    data = {}
    try:
        token = request.auth
        user = Token.objects.get(key=token)
        workout = Workout.objects.filter(user=user.user)
        if len(workout) == 0:
            workout = Workout()
            workout.workout = request.data
            workout.user = user.user
            workout.save()
        else:
            workout = workout[0]
            workout.workout = request.data
            workout.user = user.user
            workout.save()
        data["message"] = "{} user upload workout sucess".format(user.user)
    except Exception as e:
        data["error"] = str(e)
    return Response(data)
