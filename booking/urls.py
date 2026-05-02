from django.urls import path 
from . import views

urlpatterns = [
    path('', views.BookingCreateView.as_view(), name='booking'),
    path('', views.MyBookingsView.as_view(), name="my_bookings"),
    path('', views.BookingUpdateView.as_view(), name="edit_booking"),
    path('', views.BookingDeleteView.as_view(), name="delete_booking"),
]