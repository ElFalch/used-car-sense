from django.urls import path 
from . import views


urlpatterns = [
    path('', views.BookingCreateView.as_view(), name='booking'),
    path("my-bookings/", MyBookingsView.as_view(), name="my_bookings"),
    path("edit/<int:pk>/", BookingUpdateView.as_view(), name="edit_booking"),
    path("delete/<int:pk>/", BookingDeleteView.as_view(), name="delete_booking"),
]