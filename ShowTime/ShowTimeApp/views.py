from django import forms
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import User,movies




def Login(request):
    return render(request,'ShowTimeApp/Login.html',{"form":newLoginForm()})

def register(request):
    if request.method == 'POST':

        form = newLoginForm(request.POST)
        if form.is_valid():


            
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            if User.objects.filter(username=username).exists():
                return render(request, "ShowTimeApp/register.html",
                              {"form": form,"message": "username exists!"})

            else:
                new_account = User(username=username, password=password)
                new_account.save()
                return render(request, "ShowTimeApp/Login.html",
                              {"form": newLoginForm()})
    else:
        return render(request, "ShowTimeApp/register.html",
                      {"form":newLoginForm()})
    
def validate_login(request):
     if request.method == 'POST':

        form = newLoginForm(request.POST)
        if form.is_valid():


            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            if User.objects.filter(username=username ,password=password).exists():
                request.session['username'] = username 
                return displayMovies(request)
            

            else:
                return render(request, "ShowTimeApp/Login.html",
                              {"form": form,"message":"Username or password wrong"})
            
        
def displayMovies(request):
    username=request.session.get("username")
    user=User.objects.get(username=username)
    user_movies= user.movies.all()
    if request.method == 'POST':
        choice = request.POST.get('choice')

        if choice == 'add':

            return redirect("ShowTimeApp:addMovie")
        elif choice == 'update':
            return redirect("ShowTimeApp:updateMovie")

        elif choice == 'remove':
            return redirect("ShowTimeApp:removeMovie")
    return render(request, "ShowTimeApp/Main.html",{"movies":user_movies})

def addMovie(request):
    if request.method == "POST":
        form = newMovieForm(request.POST)
        if form.is_valid():
            title=form.cleaned_data["title"]
            year=form.cleaned_data["year"]
            genre=form.cleaned_data["genre"]
            rating = form.cleaned_data["rating"]
            status = form.cleaned_data["status"]

            username = request.session.get("username")

            try:
             new_movie = movies.objects.create(title=title,year=year,genre=genre,rating=rating,status=status)
             user = User.objects.get(username=username)
             user.movies.add(new_movie)
             new_movie.save()
            except IntegrityError:
                return render(request, "ShowTimeApp/Add.html",
                              {"form": newMovieForm(),"message":"movie already exist!!"} )
            return render(request, "ShowTimeApp/Add.html",
                              {"form": newMovieForm(),"message":"movie added successfully"} )
    else:
        return render(request, "ShowTimeApp/Add.html",
                              {"form": newMovieForm()})
    
def removeMovie(request):
     if request.method == "POST":
        movie_id= request.POST.get("id")
        username=request.session.get("username")
        user=User.objects.get(username=username)
        user_movies= user.movies.all()
        try:
            id = user.movies.get(id=movie_id)
            user.movies.remove(id)
            return render(request, "ShowTimeApp/Remove.html", {"movies": user_movies,
                                                        "message": "movie was removed successfully"})
        except Exception:
            return render(request, "ShowTimeApp/Remove.html", {"movies": user_movies,
                                                        "message": "movie doesnt exist!"})
     else:
        username = request.session.get("username")
        user = User.objects.get(username=username)
        user_movies = user.movies.all()
        return render(request, "ShowTimeApp/Remove.html", {"movies": user_movies})
     

def updateMovie(request):
    if request.method == "POST":
        form = newupdateMovieForm(request.POST)
        if form.is_valid():
            movie_id = form.cleaned_data["id"]
            title = form.cleaned_data["title"]
            year = form.cleaned_data["year"]
            genre = form.cleaned_data["genre"]
            rating = form.cleaned_data["rating"]
            status = form.cleaned_data["status"]
            try:
                username = request.session.get("username")
                user=User.objects.get(username=username)
                user_movies = user.movies.all()
                updated_movie = user.movies.get(id=movie_id)

                title = form.cleaned_data["title"]
                year = form.cleaned_data["year"]
                genre = form.cleaned_data["genre"]
                rating = form.cleaned_data["rating"]
                status = form.cleaned_data["status"]
            
                updated_movie.title=title
                updated_movie.year=year
                updated_movie.genre=genre
                updated_movie.rating=rating
                updated_movie.status=status
                updated_movie.save()
                return render(request, "ShowTimeApp/Update.html", {"form": newupdateMovieForm(), "movies": user_movies,"message": "movie was updated successfully"})
            except Exception:
                return render(request, "ShowTimeApp/Update.html",
                              {"form": newupdateMovieForm(), "movies": user_movies,"message": "movie id not found!"})

    else:
        username = request.session.get("username")
        user=User.objects.get(username=username)
        user_movies = user.movies.all()
        return render(request, "ShowTimeApp/Update.html", {"form": newupdateMovieForm(), "movies": user_movies})
            


MOVIE_genres = [
        ('romance', 'romance'),
        ('action', 'action'),
        ('drama', 'drama'),
        ('comedy', 'comedy'),
        ('sci-fi', 'sci-fi'),
        ('animation', 'animation'),
        ('horror', 'horror'),
        ('thriller', 'thriller'),
    ]   
MOVIE_status = [
        ('Watched', 'Watched'),
        ('Not watched', 'Not watched'),]
    
MOVIE_ratings = [
        ('Pending', 'Pending'),
        ('10', '10'),
        ('9', '9'),
        ('8', '8'),
        ('7', '7'),
        ('6', '6'),
        ('5', '5'),
        ('4', '4'),
        ('3', '3'),
        ('2', '2'),
        ('1', '1'),
    ]

    
class newLoginForm(forms.Form):
     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class newupdateMovieForm(forms.Form):
   
    id = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    year = forms.TypedChoiceField(
        choices=[(str(y), y) for y in range(2025, 1887, -1)],
        coerce=int,
        widget=forms.Select(attrs={'class': 'form-control'}))
    genre = forms.ChoiceField(label="genre",choices=MOVIE_genres,widget=forms.Select(attrs={'class': 'form-control'}))
    rating = forms.ChoiceField(choices=MOVIE_ratings, label="Rating", widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=MOVIE_status, label="Status", widget=forms.Select(attrs={'class': 'form-control'}))

class newMovieForm(forms.ModelForm):

    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    year = forms.TypedChoiceField(
        choices=[(str(y), y) for y in range(2025, 1887, -1)],  #the first movie ever was in 1888
        coerce=int,
        widget=forms.Select(attrs={'class': 'form-control'}))
    genre = forms.ChoiceField(choices=MOVIE_genres, label="Genre", widget=forms.Select(attrs={'class': 'form-control'}))
    rating = forms.ChoiceField(choices=MOVIE_ratings, label="Rating", widget=forms.Select(attrs={'class': 'form-control'}))
    status = forms.ChoiceField(choices=MOVIE_status, label="Status", widget=forms.Select(attrs={'class': 'form-control'}))
    
    class Meta:
        model = movies
        fields = ['title', 'year','genre','rating','status']
    




