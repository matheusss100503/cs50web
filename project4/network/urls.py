
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_post, name='create'),
    path('edit/<int:postID>', views.edit_post, name='edit'),
    path('posts/<str:group>', views.posts, name='posts'),
    path('users/<str:username>', views.user_profile, name='user_profile'),
    path('follow/<str:username>', views.follow_user, name='follow'),
    path('unfollow/<str:username>', views.unfollow_user, name='unfollow'),
    path('like/<int:postID>', views.like, name='like'),
    path('unlike/<int:postID>', views.unlike, name='unlike'),
]
