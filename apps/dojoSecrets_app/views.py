from django.shortcuts import render, redirect
from .models import User, Secret, Like, UserManager
from django.contrib import messages
from django.db.models import Count

# Create your views here.
def index(request):
    return render(request, 'dojoSecrets_app/index.html')

def register(request):
    if request.method == 'POST':
        data_stuff = {
        'fname':request.POST['first'],
        'lname':request.POST['last'],
        'email':request.POST['mail'],
        'password':request.POST['pass'],
        'pass_conf':request.POST['conf']
        }
        result = User.objects.register(data_stuff)
        if result['errors'] == None:
            request.session['id'] = result['user'].id
            request.session['fname'] = result['user'].first_name
            return redirect('/success')
        else:
            for error in result['errors']:
                messages.error(request, error, extra_tags='register')
            return redirect ('/')

def login(request):
    if request.method == "POST":
        login_stuff = {
        'email':request.POST['mail'],
        'password':request.POST['pass']
        }
    login_result = User.objects.login(login_stuff)
    if login_result['errors'] == None:
        request.session['fname'] = login_result['user'].first_name
        request.session['id'] = login_result['user'].id
        return redirect('/success')
    else:
        for error in login_result['errors']:
            messages.error(request, error, extra_tags='login')
        return redirect ('/')

def logout(request):
    request.session.clear()
    return redirect ('/')

def success(request):
    # if id not in request.session:
    #     return redirect('/')
    current_user = User.objects.get(id=request.session['id'])
    all_secrets = Secret.objects.all().order_by('-created_at')[:5]
    secrets_list = []
    for secret in all_secrets:
        secret.liked=True
        try:
            Like.objects.get(user=current_user, secret=secret)
        except:
            secret.liked=False
        secrets_list.append(secret)
    context = {
    "input":User.objects.all(),
    "secrets":secrets_list,
    "welcome":request.session['fname']
    }
    return render(request, 'dojoSecrets_app/success.html', context)

def popular_secrets(request):
    if id not in request.session:
        return redirect('/')
    current_user = User.objects.get(id=request.session['id'])
    all_secrets = Secret.objects.annotate(num_likes=Count('secret_likes')).order_by('-num_likes')[:5]
    secrets_list = []
    for secret in all_secrets:
        secret.liked=True
        try:
            Like.objects.get(user=current_user, secret=secret)
        except:
            secret.liked=False
        secrets_list.append(secret)
    context = {
    "input":User.objects.all(),
    "secrets":secrets_list,
    "welcome":request.session['fname']
    }
    return render(request, 'dojoSecrets_app/top_secrets.html', context)

def new_secret(request):
    current_user = User.objects.get(id=request.session['id'])
    a_secret = Secret.objects.create(content=request.POST['content'], user=current_user)
    return redirect('/success')

def add_like(request, secret_id):
    a_secret = Secret.objects.get(id=secret_id)
    a_user = User.objects.get(id=request.session['id'])
    Like.objects.create(secret=a_secret, user=a_user)
    return redirect('/success')

def destroy_secret(request, secret_id):
    a_secret = Secret.objects.get(id=secret_id)
    if a_secret.user.id == request.session['id']:
        a_secret.delete()
    else:
        messages.add_message(request, messages.ERROR, "You cant do that")
    return redirect('/success')











# end
