from django.urls import path 
from .  import views 
app_name= "ShowTimeApp"
urlpatterns = [
    path("",views.Login,name='Login'),
    path("validateLogin", views.validate_login, name='validate_login'),
    path("register", views.register, name='register'),
    path("displayMovies", views.displayMovies, name='displayMovies'),
    path("addMovie", views.addMovie, name='addMovie'),
    path("removeMovie", views.removeMovie, name="removeMovie"),
    path("updateMovie", views.updateMovie, name="updateMovie")
]