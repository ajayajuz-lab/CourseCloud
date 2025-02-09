from django.urls import path
from student import views

urlpatterns=[
    path('register/',views.StudentCreateView.as_view(),name="student-register"),
    path('signin/',views.LoginView.as_view(),name="signin"),
    path('index/',views.IndexView.as_view(),name="index"),
    path('courses/detail/<int:pk>/',views.CourseDetailView.as_view(),name="course-detail"),
    path('courses/<int:pk>/add-to-cart/',views.AddToCartView.as_view(),name="add-to-cart"),
    path('cart/summary/',views.CartSummaryView.as_view(),name="cart-summary"),
    path('cart/<int:pk>/remove/',views.CartItemDeleteView.as_view(),name="cart-item-remove"),
    path('checkout/',views.OrderCheckoutView.as_view(),name="checkout"),
    path('purchased/',views.MycoursesView.as_view(),name="purchased-courses"),
]