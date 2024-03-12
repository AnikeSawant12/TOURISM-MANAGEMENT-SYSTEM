from . import views
from django.urls import path
from django.conf.urls import include, url

urlpatterns = [
# Auth
	path('user_login/', views.LoginView.as_view(), name='user_login'),
	path('registration/', views.SignupView.as_view(), name='registration'),	
	path('userlogout/', views.LogoutView.as_view(), name='userlogout'),

	path('', views.HomeView.as_view(), name='index'),
	path('upcomingTrips/', views.UpcomingTripsView.as_view(), name='upcomingTrips'),
	path('tripDetailsView/<str:slug>', views.TripDetailsView.as_view(), name='tripDetailsView'),
	path('bookNow/<str:slug>', views.BookTripView.as_view(), name='bookNow'),
	path('saveTrip/', views.CreateTrip.as_view(), name='saveTrip'),
	path('showTrips/', views.ShowTripView.as_view(), name='showTrips'),
]