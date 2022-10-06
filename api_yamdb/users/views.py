from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from users.models import User
from users.serializers import (SignupSerializer, TokenSerializer,
                               UsersSerializer)

from .permissions import IfUserAdmin


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IfUserAdmin]
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    pagination_class = PageNumberPagination

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=(IsAuthenticated,), url_path='me')
    def about_me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        if serializer.validated_data.get('role'):
            serializer.validated_data['role'] = request.user.role
        serializer.save()
        return Response(serializer.data)


class APISignup(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    @staticmethod
    def prepare_confirmation_email(email, code):
        email_body = (
            f'Код подтвержения к API:{code} '
        )
        return {
            'email_body': email_body,
            'to_email': email,
            'email_subject': 'Код подтверждения'
        }

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        email = request.data.get('email')
        user = User.objects.filter(email=email)
        if user.exists():
            code = User.objects.get(email=email).confirmation_code
            data = self.prepare_confirmation_email(code, email)
            self.send_email(data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        serializer.save(email=email)
        user = get_object_or_404(User, email=email)
        user_mail = user.email
        user_code = user.confirmation_code
        new_data = self.prepare_confirmation_email(user_mail, user_code)
        self.send_email(new_data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class APIToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        confirmation_code = serializer.validated_data['confirmation_code']
        username = serializer.validated_data['username']
        try:
            user = get_object_or_404(User, username=username)
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователя не существует'},
                status=status.HTTP_404_NOT_FOUND
            )
        if confirmation_code == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_201_CREATED
            )
        return Response(
            {'confirmation_code': 'Неверный код'},
            status=status.HTTP_400_BAD_REQUEST
        )
