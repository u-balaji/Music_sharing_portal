from django.shortcuts import render
from first_app.forms import UserForm,songForm
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Song
from django.shortcuts import render, redirect
from django.urls import reverse



def index(request):
    if request.user.is_authenticated:
        username = request.user.username
        my_dict = username
        user = request.user
        user_files = Song.objects.filter(user=user,allowed_emails="").distinct()
        #print(user_files.values())
        public_files = Song.objects.filter(audio_type = 'Public').exclude(user=user)
        #mails = Song.objects.filter(audio_type='Protected').exclude(user=user).values()
        #print(mails)
        # try:
        #     print(mails.get(allowed_emails = username))
        # except mails.DoesNotExist:
        #     user = None
        protected_files = Song.objects.filter(audio_type='Protected',allowed_emails = username).exclude(user=user)
        #print(protected_files.values())
        context = {
            'my_dict':my_dict,
            'user_files': user_files,
            'public_files': public_files,
            'protected_files': protected_files
        }
        return render(request, 'first_app/index.html',context=context)
    else:
        return render(request,'first_app/index.html')


def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save(0)
            registered = True

        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
        

    return render(request, 'first_app/registration.html', {'user_form': user_form,  'registered': registered})


def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                # my_dict = User.objects.filter(username = username )
                # print(my_dict)
                # return render(request , 'first_app/home.html',{'my_dict':my_dict})
                return redirect('index')
            else:
                return HttpResponse(" ACCOUNT IS NOT ACTIVE")
        else:
            print("Access failed. Username: {} Password: {}".format(
                username, password))
            return HttpResponse("Sorry please register before login ")
    else:
        return render(request, 'first_app/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



@login_required
def upload(request):
    if request.user.is_authenticated:
        username = request.user.username
        my_dict = username
        registered_users=[]
        unregistered_users=[]
        if request.method == "POST":
            registered_users=[]
            unregistered_users=[]
            song_form = songForm(request.POST, request.FILES)
            file = request.FILES.get('audio_file')
            access_type = request.POST.get('audio_type')
            audio_type = request.POST.get('audio_name')
            email_addresses = request.POST.get('allowed_emails').split(',')
            #print(email_addresses)
            
            if song_form.is_valid():
                if access_type == 'Protected':
                    registered_users = check_registered_users(email_addresses)[0]
                    unregistered_users = check_registered_users(email_addresses)[1]
                    #print(registered_users)
                    for registered_user in registered_users:
                        song = Song(audio_name=audio_type, audio_file=file, allowed_emails=registered_user, audio_type=access_type)
                        song.user = request.user
                        #song.audio_name = audio_type
                        #song.audio_type = access_type
                        #song.audio_file = file
                        #song.allowed_emails = registered_user
                        print(registered_user)
                        song.save()
                    song = Song(audio_name=audio_type, audio_file=file, allowed_emails="", audio_type=access_type)
                    song.user = request.user
                        #song.audio_name = audio_type
                        #song.audio_type = access_type
                        #song.audio_file = file
                        #song.allowed_emails = registered_user
                    song.save()
                elif access_type == 'Private':
                    song = song_form.save(commit=False)
                    song.user = request.user
                    song.audio_type = access_type
                    song.allowed_emails = ""
                    song.save()
                else:
                    song = song_form.save(commit=False)
                    song.user = request.user
                    song.allowed_emails = ""
                    song.save()
                song_form = songForm()
            else:
                print(song_form.errors)
            
        else:
            song_form = songForm()
        return render(request, 'first_app/upload.html',{'my_dict':my_dict,'song_form':song_form,'unregistered_users':unregistered_users})
    else:
        return render(request,'first_app/upload.html')

def check_registered_users(email_addresses):
    res=[]
    unregistered_users=[]
    registered_users = []
    for email in email_addresses:
        email = email.strip()
        if User.objects.filter(username=email).exists():
            registered_users.append(email)
        else:
            unregistered_users.append(email)
    res.append(registered_users)
    res.append(unregistered_users)
    return res
