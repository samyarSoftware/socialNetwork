from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


app_name = 'social'

urlpatterns = [
    path("", views.home, name="home"),
    path("profile/", views.profile, name="profile"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("register/", views.register, name="register"),
    path("user-edit/", views.user_edit, name="user_edit"),
    path("ticket/", views.ticket, name="ticket"),
    path("password/change/", views.password_change, name="password_change"),
    path('password-reset', auth_views.PasswordResetView.as_view(success_url="password-reset/done"), name="password_reset"),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('password-reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(success_url="/password-reset/complete"), name="password_reset_confirm"),
    path('password-reset/complete', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('posts/', views.post_list, name="post_list"),
    path('posts/create/post/', views.create_post, name="create_post"),
    path('posts/<slug:tag_slug>/', views.post_list, name="post_list_by_tag"),
    path('posts/post-detail/<pk>', views.post_detail, name="post_detail"),
    path('search/', views.search, name="search"),
    path('posts/comment/post/<int:pk>/', views.comment, name="comment"),
    path('profile/delete-post/<post_id>', views.delete_post, name="delete_post"),
    # path('profile/edit-post/<post_id>', views.edit_post, name="edit_post"),
    path('like-post/', views.like_post, name="like_post"),
    path('save-post/', views.save_post, name="save_post"),
    path('user-detail/<username>', views.user_detail, name="user_detail"),
    path('follow/', views.follow, name="follow"),
    path('ticket-detail/<pk>', views.ticket_detail, name="ticket_detail"),
    path('ticket-reply/<int:id>', views.ticket_reply, name="ticket_reply"),
    
]