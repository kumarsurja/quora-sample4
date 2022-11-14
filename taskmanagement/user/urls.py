from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from .views import RegisterView, LoginAPIView,UserListView,FollowTheUser
from django.conf import settings

urlpatterns = [
                  url(r'^login/', LoginAPIView.as_view(), name="login"),                 
                  url(r'^signup/',  RegisterView.as_view(), name="register"),
                  url(r'^user-list/',  UserListView.as_view(), name="all-user"),
                  url(r'^follow-to/',  FollowTheUser.as_view(), name="all-user"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

