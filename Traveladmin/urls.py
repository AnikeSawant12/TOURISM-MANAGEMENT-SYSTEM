from . import views
from django.urls import path
from django.conf.urls import include, url

urlpatterns = [
	path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # Site Urls
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Hotel Urls
    path('manageHotel/', views.ManageHotelView.as_view(), name='manageHotel'),
    path('createHotel/', views.CreateNewHotelView.as_view(), name='createHotel'), 
    path('editHotel/<str:slug>', views.EditHotelview.as_view(), name='editHotel'), 
    path('deleteHotel/<str:slug>', views.DeleteHotelView.as_view(), name='deleteHotel'), 

    # Trip Urls 
    path('manageUpcomingtrips', views.ManageTrips.as_view(), name='manageUpcomingtrips'),
    path('createTrip/', views.CreateTripView.as_view(), name='createTrip'),  
    path('tripDetails/<str:slug>', views.TripDetailsView.as_view(), name='tripDetails'), 
    path('editTrip/<str:slug>', views.EditTripView.as_view(), name='editTrip'),
    path('deleteTrip/<str:slug>', views.DeleteTripView.as_view(), name='deleteTrip'),  
    path('viewNewtrips/', views.ViewNewTripsView.as_view(), name='viewNewtrips'), 
    path('inProcess/<str:slug>', views.TripProcessView.as_view(), name='inProcess'),
    path('inProcess/', views.InProcessTrips.as_view(), name='inProcess'),
     
]