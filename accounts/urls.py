from django.urls import path
from .views import profile,signup,edit_profile
app_name='accounts'
urlpatterns = [
	path('profile',profile,name='profile'),
	path('<int:id>/edit', edit_profile, name='edit_profile'),
    path('signup',signup,name='signup '),
 
]