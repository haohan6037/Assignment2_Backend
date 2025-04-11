from django.urls import path
from . import views
from .views import CreatePostView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('posts/create/', CreatePostView.as_view(), name='create-post'),
]
