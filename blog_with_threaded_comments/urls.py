from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from posts import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.RegistrationView.as_view(), name='signup'),
    path('user/<username>/', views.ProfileView.as_view(), name='profile'),

    path('', include('posts.urls', namespace='posts')),
    path('api/', include('posts.api.urls', namespace='posts-api')),
]
