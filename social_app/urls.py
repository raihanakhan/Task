from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import LoginView, UserRegistrationView, PostCreateView, PostView, UnLikePostView, LikePostView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='auth_register'),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("login/", LoginView.as_view(), name="login"),
    path('post/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/', PostView.as_view(), name='post'),
    path('like/', LikePostView.as_view(), name='like-post'),
    path('unlike/<int:pk>/', UnLikePostView.as_view(), name='unlike-post'),
]
