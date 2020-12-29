from django.urls import path

from . import views

app_name = 'posts'

urlpatterns = [

    path('', views.PostListView.as_view(), name='post-list'),
    path('post/<slug:post>/',
         views.detail_post_view,
         name='post-detail'),
    path('new_post/', views.NewPostView.as_view(), name='new-post'),
    path('<slug:slug>/delete/', views.DeletePostView.as_view(), name='post-delete'),
    path('<slug:slug>/update/', views.UpdatePostView.as_view(), name='post-update'),

    path('post/<slug:post>/comment/<int:pk>', views.comment_reply_view, name='comment-reply'),
    path('post/<slug:post>/comment/<int:pk>/delete/', views.DeleteCommentView.as_view(), name='comment-delete'),
    path('post/<slug:post>/comment/<int:pk>/update/', views.UpdateCommentView.as_view(), name='comment-update'),
]
