from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic.list import ListView
from django.core.paginator import Paginator

from . import models
from . import forms


# def index(request):
#     projects = models.Project.objects.all()
#
#     context = {
#         'projects': projects,
#     }
#     return render(request, 'main/index.html', context)


class ProjectsListView(ListView):
    queryset = models.Project.objects.all().order_by('created')
    context_object_name = 'projects'
    template_name = 'main/index.html'
    paginate_by = 3
    paginator_class = Paginator

    # def get_queryset(self):
    #     request, projects = utils.search_project(self.request)
    #     return projects

    # is_paginated, obj_list, ...


def project_detail(request, pk):
    project = models.Project.objects.get(id=pk)
    reviews = project.review_set.all().order_by('-created')

    if request.method == 'POST':
        review = models.Review.objects.create(
            owner=request.user,
            project=project,
            body=request.POST.get('review'),
        )
        review.save()
        return redirect('main:project_detail', pk=project.id)

    context = {
        'project': project,
        'reviews': reviews,
    }
    return render(request, 'main/project_detail.html', context)


@login_required(login_url='users:login')
def add_project(request):
    if request.method == 'POST':
        form = forms.ProjectForm(request.POST, request.FILES)

        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, 'Project has been created successfully')
            return redirect('users:account')
        else:
            messages.error(request, 'Fields are filled incorrectly')
            return redirect('main:add_project')

    form = forms.ProjectForm()
    context = {
        'form': form,
    }
    return render(request, 'form-template.html', context)


@login_required(login_url='users:signin')
def edit_project(request, pk):
    project = models.Project.objects.get(id=pk)

    if request.method == 'POST':
        form = forms.ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project has been edited successfully')
            return redirect('users:account')
        else:
            messages.error(request, 'Fields are filled incorrectly')
            return redirect('main:edit_project')

    form = forms.ProjectForm(instance=project)
    context = {
        'form': form,
        'project': project,
    }
    return render(request, 'main/project_edit.html', context)


@login_required(login_url='users:login')
def delete_project(request, pk):
    project = models.Project.objects.get(id=pk)

    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project has been deleted successfully')
        return redirect('users:account')

    context = {
        'object_name': project.title,
        'object_type': 'project'
    }
    return render(request, 'delete-template.html', context)
