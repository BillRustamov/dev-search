from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.models import Q
from django.views.generic.list import ListView

from . import models
from . import forms
from . import utils


# def index(request):
#     request, profiles = utils.search_profiles(request)
#     custom_range, profiles = utils.paginate_profiles(request, profiles)

#     context = {
#         'page_range': custom_range,
#         'profiles': profiles,
#         'search_query': request.GET.get('q') if request.GET.get('q') else ''
#     }
#     return render(request, 'users/index.html', context)


class ProfilesListView(ListView):
    template_name = 'users/index.html'
    context_object_name = 'profiles'
    paginate_by = 3
    paginator_class = Paginator

    def get_queryset(self):
        request, profiles = utils.search_profiles(self.request)
        # objects_list
        return profiles.order_by('created')


@login_required(login_url='users:signin')
def inbox(request):
    # Identify profile
    profile = request.user

    # Old way of getting profile's messages without related name
    # messages = profile.message_set.all()

    # New way of getting profile's message with related name
    received_messages = profile.received_messages.all()
    unread_messages = profile.received_messages.filter(is_read=False).count()
    messages_count = len(received_messages)

    context = {
        'received_messages': received_messages,
        'unread_messages': unread_messages,
        'messages_count': messages_count,
    }
    return render(request, 'users/inbox.html', context)


@login_required(login_url='users:signin')
def message_detail(request, pk):
    message = models.Message.objects.get(id=pk)

    if message.recipient != request.user:
        # error message
        return redirect('users:inbox')

    message.is_read = True
    message.save()

    context = {
        'message': message,
    }
    return render(request, 'users/message.html', context)


def send_message(request, pk):
    if request.method == 'POST':
        form = forms.MessageForm(request.POST)  # [fullname, email, subject, body]
        if request.user.is_authenticated:
            form.fields.pop('fullname')
            form.fields.pop('email')

        if form.is_valid():
            if request.user.is_authenticated:
                sender = request.user  # AnonymousUser
            else:
                sender = None
            recipient = models.Profile.objects.get(id=pk)

            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            message.fullname = sender.get_full_name
            message.email = sender.email
            message.save()
            messages.success(request, 'Messages has been sent successfully')
            return redirect('users:account_detail', pk=pk)

        else:
            messages.error(request, 'Fields are filled incorrectly')
            return redirect('users:send_message', pk=pk)

    form = forms.MessageForm()  # [fullname, email, subject, body]
    if request.user.is_authenticated:
        form.fields.pop('fullname')
        form.fields.pop('email')
        # [subject, body]

    context = {
        'form': form,
    }
    return render(request, 'form-template.html', context)


def account_detail(request, pk):
    profile = models.Profile.objects.get(id=pk)
    dev_skills = profile.skill_set.exclude(description="")
    other_skills = profile.skill_set.filter(description="")

    context = {
        'profile': profile,
        'dev_skills': dev_skills,
        'other_skills': other_skills,
    }
    return render(request, 'users/profile_detail.html', context)


@login_required(login_url='users:signin')
def account_update(request):
    profile = models.Profile.objects.get(id=request.user.id)

    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, 'Account has been updated successfully')
            return redirect('users:account')
        else:
            messages.error(request, 'Fields are filled incorrectly')
            return redirect('users:account_update')

    form = forms.ProfileForm(instance=profile)  # (request,), {instance: profile}
    context = {
        'form': form,
    }
    return render(request, 'form-template.html', context)


@login_required(login_url='users:signin')
def account(request):
    context = {
        'skills': request.user.skill_set.all(),
        'projects': request.user.project_set.all(),
    }
    return render(request, 'users/account.html', context)


@login_required(login_url='users:login')
def add_skill(request):
    if request.method == 'POST':
        profile = request.user
        form = forms.SkillForm(request.POST)

        if form.is_valid():
            skill = form.save(commit=False)
            skill.profile = profile
            skill.save()
            messages.success(request, 'Skill has been created successfully')
            return redirect('users:account')
        else:
            messages.error(request, 'Fields are filled incorrectly')
            return redirect('users:add_skill')

    form = forms.SkillForm()
    context = {
        'form': form,
    }
    return render(request, 'form-template.html', context)


@login_required(login_url='users:login')
def edit_skill(request, pk):
    skill = models.Skill.objects.get(id=pk)

    if skill.profile != request.user:
        messages.error(request, 'You cannot edit another person\'s skill')
        return redirect('users:account')

    if request.method == 'POST':
        form = forms.SkillForm(request.POST, instance=skill)

        if form.is_valid():
            form.save()
            messages.success(request, 'Skill has been edited successfully')
            return redirect('users:account')
        else:
            messages.success(request, 'Fields are filled incorrectly')
            return redirect('users:edit_skill', pk=pk)

    form = forms.SkillForm(instance=skill)
    context = {
        'form': form,
    }
    return render(request, 'form-template.html', context)


@login_required(login_url='users:login')
def delete_skill(request, pk):
    skill = models.Skill.objects.get(id=pk)

    if skill.owner != request.user:
        messages.error(request, 'You cannot delete another person\'s skill')
        return redirect('users:account')

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill has been deleted successfully')
        return redirect('users:account')

    context = {
        'object_name': skill.name,
        'object_type': 'skill',
    }
    return render(request, 'delete-template.html', context)


def signin(request):
    if request.session.session_key:
        messages.info(request, 'Logout first to access login page')
        return redirect('main:home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = models.Profile.objects.get(email=email)
            if user.check_password(raw_password=password):
                login(request, user)

                if user.short_intro and user.location and user.description:
                    messages.info(request, 'Logged in')

                else:
                    messages.info(request, 'Logged in, provide location, bio and short intro, otherwise you would \
                                                                not be shown in search results')

                return redirect('users:account')
            else:
                messages.error(request, 'Password is incorrect')
                return redirect('users:signin')
        except:
            messages.error(request, 'Account not found')
            return redirect('users:signin')

    context = {}
    return render(request, 'users/signin.html', context)


def signup(request):
    if request.session.session_key:
        messages.info(request, 'Logout first to the access signup page')
        return redirect('main:home')

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if first_name and last_name and email and password1 and password2:
            if password1 == password2:
                try:
                    user = models.Profile.objects.create_user(
                        email=email,
                        first_name=first_name,
                        last_name=last_name,
                        password=password2
                    )
                    messages.success(request, 'You have been successfully signed up, login here')
                    return redirect('users:signin')

                except:
                    messages.error(request, 'User with this email already exists')
                    return redirect('users:signup')

            else:
                messages.error(request, 'Passwords don\'t match')
                return redirect('users:signup')
        else:
            messages.error(request, 'Fields are filled incorrectly')
            return redirect('users:signup')

    context = {}
    return render(request, 'users/signup.html', context)


def signout(request):
    logout(request)
    messages.info(request, 'Logged out')
    return redirect('users:signin')
