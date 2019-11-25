from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User, Group
from plusdi.models import Discount, Commerce, Client, ClientCategory
from django.contrib.auth import authenticate
from jose import jwt
from django.conf import settings
import json
from plusdi.jwt_helper import JwtHelper
from plusdi.user_helper import UserHelper
from django.db import IntegrityError
import datetime
from django.db.models import Q

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
def post_discount_test(request):
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
@permission_classes((AllowAny,))
def login_commerce(request):
    data = {}
    try:
        jwt = JwtHelper()
        user_helper = UserHelper()
        post_data = jwt.decode_data(request.data["data"])
        if authenticate(username=post_data["email"], password=post_data["password"]):
            commerce = User.objects.get(username=post_data["email"])
            commerce_account = Commerce.objects.get(commerce=commerce)
            if commerce.groups.filter(name="commerce").exists():
                data["data"] = jwt.encode_data({"token": user_helper.get_token(commerce)[0].key, "email": commerce.email, "id": commerce.id, "company": commerce_account.company})
            else:
                data["error"] = "User not found"
        else:
            data["error"] = "User not found"
    except Exception as error:
        data["error"] = "Error: {}".format(error)

    return Response(data)



@api_view(['POST'])
@permission_classes((AllowAny,))
def login_user(request):
    data = {}
    try:
        jwt = JwtHelper()
        user_helper = UserHelper()
        post_data = jwt.decode_data(request.data["data"])
        if authenticate(username=post_data["email"], password=post_data["password"]):
            client = User.objects.get(username=post_data["email"])
            if client.groups.filter(name="client").exists():
                data["data"] = jwt.encode_data({"token": user_helper.get_token(client)[0].key, "email": client.email, "id": client.id})
            else:
                data["error"] = "User not found"
        else:
            data["error"] = "User not found"
    except Exception as error:
        data["error"] = "Error: {}".format(error)

    return Response(data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_commerce(request):
    data = {}
    try:
        jwt = JwtHelper()
        post_data = jwt.decode_data(request.data["data"])
        token = Token.objects.get(key=request.auth)
        commerce = Commerce.objects.get(commerce=token.user)
        commerce.company = post_data["company"]
        commerce.phone = post_data["phone"]
        commerce.web = post_data["web"]
        commerce.save()
        data["update"] = "Commerce {} updated!".format(token.user.email)

    except Exception as error:
        data["error"] = "Error {}".format(error)
    return Response(data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_commerce(request):
    data = {}
    try:
        jwt = JwtHelper()
        token = Token.objects.get(key=request.auth)
        commerce = Commerce.objects.get(commerce=token.user)
        data["data"] = jwt.encode_data(
                {"company": commerce.company, "phone": commerce.phone, "web": commerce.web})
    except Exception as error:
        data["error"] = "Error {}".format(error)
    return Response(data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def post_discount(request):
    data = {}
    try:
        jwt = JwtHelper()
        token = Token.objects.get(key=request.auth)
        commerce = Commerce.objects.get(commerce=token.user)
        post_data = jwt.decode_data(request.data["data"])
        new_discount = Discount(
            user=commerce.commerce, discount=post_data["discount"])
        new_discount.save()
        data["data"] = jwt.encode_data({"id": new_discount.pk})
    except Exception as error:
        data["error"] = "Error {}".format(error)
    return Response(data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_commerce_discount(request):
    data = {}
    try:
        jwt = JwtHelper()
        token = Token.objects.get(key=request.auth)
        commerce = Commerce.objects.get(commerce=token.user)
        discounts = Discount.objects.filter(user=commerce.commerce)
        discounts_list = []
        for x in discounts:
            x.discount["id"] = x.id
            discounts_list.append(x.discount)
        data["data"] = discounts_list

    except Exception as error:
        data["error"] = "Error {}".format(error)
    return Response(data)

@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_commerce_valid_discount(request):
    data = {}
    try:
        jwt = JwtHelper()
        token = Token.objects.get(key=request.auth)
        commerce = Commerce.objects.get(commerce=token.user)
        discounts = Discount.objects.filter(Q(expire_date__gte=now.date()), & (user=commerce.commerce)).order_by('expire_date')
        discounts_list = []
        for x in discounts:
            x.discount["id"] = x.id
            discounts_list.append(x.discount)
        data["data"] = discounts_list

    except Exception as error:
        data["error"] = "Error {}".format(error)
    return Response(data)

@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_commerce_discount(request):
    data = {}
    try:
        jwt = JwtHelper()
        token = Token.objects.get(key=request.auth)
        commerce = Commerce.objects.get(commerce=token.user)
        post_data = jwt.decode_data(request.data["data"])
        discount = Discount.objects.get(
            pk=post_data["id"], user=commerce.commerce)
        discount.discount = post_data["discount"]
        if 'endDate' in post_data["discount"]:
            year = post_data["discount"]["endDate"]["date"]["year"]
            month = post_data["discount"]["endDate"]["date"]["month"]
            day = post_data["discount"]["endDate"]["date"]["day"]
            discount.expire_date = datetime.datetime(year, month, day, 0, 0, 0)

        discount.save()
        data["data"] = "Discount {} updated successfully".format(
            discount.pk)

    except Exception as error:
        data["error"] = "Error {}".format(error)
    return Response(data)


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_client(request):
    data = {}
    try:
        jwt = JwtHelper()
        user_helper = UserHelper()
        post_data = jwt.decode_data(request.data["data"])
        token, client = user_helper.create_client(
            post_data["email"], post_data["password"])
        client_profile = Client(user=client)
        client_profile.account = post_data
        client_profile.save()
        data["data"] = jwt.encode_data({"token": token[0].key})
    except Exception as error:
        data["error"] = "Error {}".format(error)
    return Response(data)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def update_client_categories(request):
    data = {}
    try:
        jwt = JwtHelper()
        new_client_category = ""
        token = Token.objects.get(key=request.auth)
        client = User.objects.get(username=token.user)
        post_data = jwt.decode_data(request.data["data"])
        client_category = ClientCategory.objects.filter(user=client)
        if len(client_category) == 0:
            new_client_category = ClientCategory(user=client)

        else:
            new_client_category = client_category[0]

        new_client_category.category = post_data["categories"]
        new_client_category.save()

        data["data"] = "Client {} categories updated successfully".format(
            client.email)
    except Exception as error:
        data["error"] = "Error {}".format(error)
    return Response(data)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_client_discounts(request):
    data = {}
    try:
        now = datetime.datetime.now()
        client_discounts = Discount.objects.filter(
            Q(expire_date__gte=now.date())).order_by('expire_date')
        data["data"] = [x.discount for x in client_discounts]
        data["commerce"] = []
        for x in client_discounts:
            commerce = Commerce.objects.get(commerce=x.user)
            data["commerce"].append({"discountId": x.id, "company": commerce.company, "phone": commerce.phone, "web": commerce.web, "commerceId": x.user.id})

    except Exception as error:
        data["error"] = "Error {}".format(error)
    return Response(data)
