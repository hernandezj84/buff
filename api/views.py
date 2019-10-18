from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from api.models import Workout


@api_view(['GET'])
@permission_classes((AllowAny,))
def test(request):
    return Response({"data": "hello world"})


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
