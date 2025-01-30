from django.urls import path
from student import views

urlpatterns=[
    path('register/',views.StudentCreateView.as_view(),name="student-create"),
    path('signin/',views.StudentSigninView.as_view(),name="signin"),
]