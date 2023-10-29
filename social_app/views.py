from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import (TokenObtainPairView)

from .models import User, Post, Like
from .serializers import LoginSerializer, UserRegistrationSerializer, PostSerializer, LikeSerializer


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class LoginView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer


class PostCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        context = super(PostCreateView, self).get_serializer_context()
        context.update({"user": self.request.user})
        return context


class PostView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, ]
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        context = super(PostView, self).get_serializer_context()
        context.update({"user": self.request.user})
        return context


class LikePostView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super(LikePostView, self).get_serializer_context()
        context.update({"user": self.request.user})
        return context


class UnLikePostView(generics.UpdateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save(liked=False)
