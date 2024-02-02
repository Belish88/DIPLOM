from app_users.models import User
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from app_users.validators import TrueInviteCodeValidator


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone', 'active_invite_code')


class RegisterUserSerializer(serializers.ModelSerializer):

    password_again = serializers.CharField(
        max_length=128,
        label=_("Password (again)"),
        write_only=True
    )

    def save(self, *args, **kwargs):
        user = User(
            phone=self.validated_data.get('phone'),
            email=self.validated_data.get('email'),
            first_name=self.validated_data.get('first_name'),
            last_name=self.validated_data.get('last_name'),
            active_invite_code=self.validated_data.get('active_invite_code')
        )

        password = self.validated_data.get('password')
        password_again = self.validated_data.get('password_again')

        if password != password_again:
            raise serializers.ValidationError({'detail': "Введенные пароли не совпадают"})

        user.set_password(password)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('phone',
                  'email',
                  'password',
                  'password_again',
                  'first_name',
                  'last_name',
                  'active_invite_code',
                  'invite_code'
                  )
        read_only_fields = ('invite_code',)
        validators = [TrueInviteCodeValidator('active_invite_code')]
        extra_kwargs = {
            'password': {'write_only': True},
        }


class ProfileUserSerializer(serializers.ModelSerializer):

    user_list = serializers.SerializerMethodField()

    @staticmethod
    def get_user_list(obj: User):
        queryset = User.objects.filter(active_invite_code=obj.invite_code)
        return [q.phone for q in queryset]

    def save(self,  *args, **kwargs):
        user = self.instance
        for field in self.fields.keys():
            if self.validated_data.get(field):
                if field == 'active_invite_code':
                    if user.active_invite_code:
                        raise serializers.ValidationError({'detail': "Нельзя активировать больше одного invite code"})
                    if self.validated_data.get(field) == user.invite_code:
                        raise serializers.ValidationError({'detail': "Нельзя активировать свой invite code"})
                user.__dict__[field] = self.validated_data.get(field)
        user.save()
        return user

    class Meta:
        model = User
        fields = ('phone',
                  'email',
                  'password',
                  'first_name',
                  'last_name',
                  'active_invite_code',
                  'invite_code',
                  'user_list'
                  )
        read_only_fields = ('invite_code', 'user_list')
        validators = [TrueInviteCodeValidator('active_invite_code')]
        extra_kwargs = {
            'password': {'write_only': True},
        }
