import json

from django.db import IntegrityError

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from main import models

from . import serializers


class ProfileViewSet(ModelViewSet):
    serializer_class = serializers.ProfileSerializer
    queryset = models.Profile.objects.all()

    '''
    /api/profiles/ -> Profile GET
    /api/profiles/ -> First profile POST
    /api/profiles/1/ -> First profile GET
    /api/profiles/1/ -> First profile PUT
    /api/profiles/1/ -> First profile PATCH
    /api/profiles/1/ -> First profile DElETE
    '''


@api_view(['GET', 'POST'])
def get_projects(request):
    # Handle POST request to create a new project
    if request.method == 'POST':
        title = request.data.pop('title')
        owner = request.data.pop('owner')  # thedevu101@gmail.com

        # request.data => {
        #     "owner": "thedevu101@gmail.com",
        #     "title": "Some project",
        #     "live_demo": "https://123.com",
        #     "source_code": "https://123.com"
        # }

        if title and owner:
            try:
                owner = models.Profile.objects.get(email=owner)
            except:
                owner = None

            if owner:
                try:
                    project = models.Project.objects.create(title=title, owner=owner, **request.data)
                    project = serializers.ProjectSerializer(project, many=False).data
                    return Response(data=project)

                except IntegrityError:
                    return Response(data={'error': 'Profile with this title already exists'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(data={'error': 'Profile with this email was not found'},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'error': 'Title and Owner fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Getting the projects list from database
    projects = models.Project.objects.all()  # <QuerySet>[]

    # Serializing (turning them into JSON list) objects
    projects = serializers.ProjectSerializer(projects, many=True).data

    # Returning serialized objects back to the frontend
    return Response(data=projects)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def get_project(request, pk):
    # Handle PUT request to update an existing project
    if request.method == 'PUT':
        try:
            project = models.Project.objects.get(id=pk)
            owner = request.data.get('owner')
            title = request.data.get('title')
            description = request.data.get('description')
            source_code = request.data.get('source_code')
            live_demo = request.data.get('live_demo')

            try:
                profile = models.Profile.objects.get(email=owner)
            except:
                profile = None

            if not profile:
                return Response(data={'error': 'Owner was not found'}, status=status.HTTP_400_BAD_REQUEST)

            if owner and title:
                project.owner = profile
                profile.title = title
                project.description = description
                project.source_code = source_code
                project.live_demo = live_demo
                project.save()

                project = serializers.ProjectSerializer(project, many=False).data
                return Response(data=project)

            else:
                return Response(data={'error': 'Title and Owner fields are required'},
                                status=status.HTTP_400_BAD_REQUEST)

        except:
            return Response(data={'error': 'Project was not found'})

    # Handle PATCH to partially update an existing project
    if request.method == 'PATCH':
        project = models.Project.objects.get(id=pk)

        title = request.data.get('title', project.title)
        description = request.data.get('description', project.description)
        source_code = request.data.get('source_code', project.source_code)
        live_demo = request.data.get('live_demo', project.live_demo)
        owner = request.data.get('owner', project.owner.email)

        try:
            owner = models.Profile.objects.get(email=owner)
        except:
            owner = None

        if not owner:
            return Response(data={'error': 'Project with this owner was not found'}, status=status.HTTP_400_BAD_REQUEST)

        project.title = title
        project.description = description
        project.source_code = source_code
        project.live_demo = live_demo
        project.owner = owner
        project.save()

        project = serializers.ProjectSerializer(project, many=False).data
        return Response(data=project)

    # Handle DELETE to destroy the project
    if request.method == 'DELETE':
        project = models.Project.objects.get(id=pk)
        project.delete()
        return Response(data={'success': 'Project has been successfully deleted'})

    # Handle GET request to get existing project's information
    try:
        project = models.Project.objects.get(id=pk)
        project = serializers.ProjectSerializer(project, many=False).data
        return Response(data=project)
    except:
        return Response(
            data={
                "error": "Project was not found"
            },
            status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def create_tag(request):
    tag_name = request.data.get('tagName')
    project_id = request.data.get('projectId')

    if tag_name:
        # Python
        tag, created = models.Tag.objects.get_or_create(name=tag_name.capitalize().strip())
        project = models.Project.objects.get(id=project_id)
        project.tags.add(tag)
        
        response = {
            'tag': tag.name,
            'created': created
        }
        response = json.dumps(response, ensure_ascii=False)

        return Response(data=response)

    return Response('Tag not specified!')


@api_view(['POST'])
def delete_tag(request):

    tag_id = request.data.get('tagId')

    try:
        tag = models.Tag.objects.get(id=tag_id)
        tag.delete()

        return Response({'status': 'ok'})
    
    except Exception as exp:
        print(exp)
        return Response({'status': 'error'})

# Function-based, APIView, ViewSet, ModelViewSet
