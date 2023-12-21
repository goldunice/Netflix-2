from django.contrib import admin
from django.urls import path, include

from filmApp.views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register("izohlar", IzohModelViewSet),
router.register("movies", KinolarModelViewSet),
router.register("actors", AktyorModelViewSet),

urlpatterns = [
    path('admin/', admin.site.urls),
    path('token/', obtain_auth_token),
    path('hello/', HelloAPI.as_view()),
    path('', include(router.urls)),
    path('aktyorlar/', AktyorlarAPI.as_view()),
    path('aktyor/<int:pk>/', AktyorAPI.as_view()),
    path('tariflar/', TariflarAPI.as_view()),
    path('delete_tarif/<int:pk>/', TarifOchirAPI.as_view()),
    path('update_tarif/<int:pk>/', TarifUpdateAPI.as_view()),
    path('kinolar/', KinolarAPI.as_view()),

]
