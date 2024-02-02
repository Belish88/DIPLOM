from time import sleep

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import UpdateView
from rest_framework import response
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny

from app_users.models import User
from app_users.serializers import RegisterUserSerializer, ProfileUserSerializer
from app_users.utils import create_code, create_invite_code


class RegisterUserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]


class ProfileAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileUserSerializer
    permission_classes = [AllowAny]


@csrf_exempt
@api_view(('POST',))
def phone(request):
    if request.method == 'POST':
        user_phone = JSONParser().parse(request)['phone']
        try:
            get_object_or_404(User, phone=user_phone)
        except Exception:
            return response.Response('Номер телефона не зарегестрирован')
        else:
            user = User.objects.get(phone=user_phone)
            user.code = create_code()
            user.save()
            sleep(2)
            return response.Response({'code': user.code})


@csrf_exempt
@api_view(('POST',))
def code(request):
    user_code = JSONParser().parse(request)['code']
    user_phone = request.GET.get('phone')
    user = User.objects.get(phone=user_phone)

    if user_code == user.code:
        user.phone_verify = True
        user.invite_code = create_invite_code()
        user.save()
        return response.Response('Верификация номера телефона прошла успешно')
    else:
        return response.Response('Код введен не верно, попробуйте еще раз')
