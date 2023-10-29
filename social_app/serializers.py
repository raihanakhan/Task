import datetime

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Post, Like


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User.objects.create(**validated_data)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password')


class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        """
        returns user's information along with access and refresh token.
        :param attrs:
        :return:
        """
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)

        data["username"] = self.user.username

        user = User.objects.get(id=self.user.id)
        user.last_login = datetime.datetime.now()
        user.save()

        return data


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'text', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = self.context.get('user', None)
        if user:
            return Post.objects.create(user=user, **validated_data)


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('post', 'liked', 'created_at', 'updated_at')

    def create(self, validated_data):
        user = self.context.get('user', None)
        if user:
            return Like.objects.create(user=user, **validated_data)
