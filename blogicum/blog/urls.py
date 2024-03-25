from django.urls import include, path

from . import views

app_name = 'blog'

posts_urls = [
    path('create/',
         views.CreatePostView.as_view(), name='create_post'),
    path('<int:post_id>/',
         views.DetailPostView.as_view(), name='post_detail'),
    path('<int:post_id>/edit/',
         views.EditPostView.as_view(), name='edit_post'),
    path('<int:post_id>/delete/',
         views.DeletePostView.as_view(), name='delete_post'),
    path('<int:post_id>/comment/',
         views.CreateCommentView.as_view(), name='add_comment'),
    path('<int:post_id>/edit_comment/<int:comment_id>/',
         views.EditCommentView.as_view(), name='edit_comment'),
    path('<int:post_id>/delete_comment/<int:comment_id>/',
         views.DeleteCommentView.as_view(), name='delete_comment'),
]

profile_urls = [
    path('', views.EditProfileView.as_view(), name='edit_profile'),
    path('<slug:username>/', views.ProfileView.as_view(), name='profile'),
]

urlpatterns = [
    path('', views.PostView.as_view(), name='index'),
    path('posts/', include(posts_urls)),
    path('profile/', include(profile_urls)),
    path('category/<slug:category_slug>/',
         views.CategoryView.as_view(), name='category_posts'),
]
