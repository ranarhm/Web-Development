from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from actions.models import Action
# from users.models import UserEditForm
from django.urls import reverse

# Create your views here.


def profile(request, username):
    user1 = get_object_or_404(User, username=username)
    if request.session.get("username", False):
        usr_obj = User.objects.get(username=request.session.get("username")) #username is unique
        user_id = getattr(usr_obj, "id")
        actions = Action.objects.filter(user_id=user_id).order_by('-created')
        return render(request,
                      "users/user/profile.html",
                      {"actions": actions, "user": user1},
                      )
    else:
        user1 = User.objects.get(username=username)
        return render(request,
                      "users/user/profile.html",
                      {"user": user1}
                      )


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username, email, password)
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

        user1 = authenticate(username=username, password=password)
        if user1 is not None:
            request.session['username'] = user1.username
            request.session['role'] = user1.details.role

        # log the action
        action = Action(
            user=user,
            verb="joined the ISVT",
            target=user
        )
        action.save()

        messages.add_message(request, messages.SUCCESS, "You successfully registered with the username: %s" % user.username)

        return redirect('events:home')

    else:
        return render(request,
                      "users/user/register.html",
                      )


def login_user(request):
    username = request.POST.get("username")
    password = request.POST.get("pw")

    user = authenticate(username=username, password=password)
    if user is not None:
        request.session['username'] = user.username
        request.session['role'] = user.details.role
        messages.add_message(request, messages.SUCCESS,
                             "You successfully logged in.")
    else:
        messages.add_message(request, messages.ERROR,
                             "Invalid username or password.")
    return redirect('events:home')


def logout_user(request):
    del request.session['username']
    del request.session['role']
    return redirect('events:home')


def edit_profile(request, username):
    pf = User.objects.all()
    print(username)

    for field in pf:
        if field == username:
            break
    print(field)

    usr_obj = User.objects.get(username=username)  # username is unique
    return render(request,
                  "users/user/useredit_form.html",
                  {"username": usr_obj}
                  )


def user_edit(request):
    if request.method == 'POST':
        # process the form
        first_name = request.POST.get('edit-first-name')
        last_name = request.POST.get('edit-last-name')
        role = request.POST.get('edit-role')
        password = request.POST.get('edit-password')

        user = User.objects.get(username=request.session.get("username"))

        ur = User.objects.all()[0]
        if first_name:
            ur.first_name = first_name
        if last_name:
            ur.last_name = last_name
        if role:
            ur.role = role
        if password:
            ur.password = password
        ur.save()

        return redirect('users:profile', ur.username)



