from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from . import models
from .. import utils


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = models.User
        fields = ['email', 'username', 'password', 'confirm_password', 'address', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }

    def save(self):
        user = models.User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            address=self.validated_data['address'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
        )
        confirm, password = self.validated_data['confirm_password'], self.validated_data['password']
        if confirm and password and confirm == password:
            user.set_password(password)
            user.save()
            user.is_active = False  # wait until email activation
        else:
            raise serializers.ValidationError({'password_mismatch': _('The two password fields didn’t match.')})
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'first_name', 'last_name']
        read_only_fields = fields


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    confirm_new_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})


class ForgetPasswordSerializer(serializers.Serializer):
    # todo
    token = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    confirm_new_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})


class PrivateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['username', 'email', 'first_name', 'last_name', 'address', 'phone']


class FriendSerializer(utils.FlattenMixin, serializers.ModelSerializer):
    class Meta:
        fields = ['date_added']
        model = models.Friend
        flatten = [('friend', PrivateUserSerializer)]
        composite_names = False


class MemberSerializer(utils.FlattenMixin, serializers.ModelSerializer):
    class Meta:
        fields = []
        model = models.Member
        flatten = [('member', PrivateUserSerializer)]
        composite_names = False


class CliqueSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = models.Clique
        fields = ['date_created', 'name', 'members', 'id']
        read_only_fields = ['date_created', 'members', 'id']


class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField(label=_("Username"), allow_blank=False, required=True)


class InviteSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"), allow_blank=True, required=False)
    phone = serializers.CharField(label=_("Phone"), allow_blank=True, required=False)


class EgoUserSerializer(PrivateUserSerializer):
    class Meta:
        model = models.User
        fields = PrivateUserSerializer.Meta.fields
