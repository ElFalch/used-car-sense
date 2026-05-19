from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.BookingCreateView.as_view(), name='booking'),
    path('my-bookings/', views.MyBookingsView.as_view(), name="my_bookings"),
    path(
        'edit/<int:pk>/',
        views.BookingUpdateView.as_view(),
        name="edit_booking"
    ),
    path(
        'delete/<int:pk>/',
        views.BookingDeleteView.as_view(),
        name="delete_booking"),
]
