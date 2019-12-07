from django.urls import path

from .views import *

urlpatterns = [path("dummyget/", DummyGetAPI.as_view(), name="dummy_get")]

