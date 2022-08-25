from django.urls import path
from home.views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
app_name = "home"

urlpatterns = [
    path('', home, name="home"),
    path('profile', Profile.as_view(), name="profile"),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='home/change_password.html',
            success_url = '/accounts/logout/'
        ),
        name='change_password'
    ),
    path('destination_details/<str:destination_id>', destination_details, name="destination_details"),
    path('destination', destination, name="destination"),
    path('post_comment/<str:destination_id>', post_comment, name="post_comment"),
    path('delete_comment/<str:destination_id>/<str:comment_id>', delete_comment, name="delete_comment"),
    path('rate_destination/<str:destination_id>', post_rate, name="post_rate"),
    path('category', category, name="category"),
    path('search', search_destination, name="search_destination"),
    path('report_comment/<str:destination_id>/<str:comment_id>', report_comment, name="report_comment"),
    path('verify-email/<str:verification_token>', verify_email, name="verify_email"),
    path('reaction/<str:destination_id>/<str:reaction>', reaction, name="reaction"),
    path('content_creator', content_creator, name="content_creator"),
    path('about', about, name="about"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
