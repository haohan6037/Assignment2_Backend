from django.urls import path
from . import views
from .views import CreatePostView, PostDetailView, PostListView, DeletePostView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),

    path('posts/create/', CreatePostView.as_view(), name='create-post'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/', PostListView.as_view(), name='post-list'),

    path('posts/<int:pk>/delete/', DeletePostView.as_view(), name='delete-post'),
]
