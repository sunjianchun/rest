# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.renderers import JSONRenderer
from rest_framework import renderers
from rest_framework.parsers import JSONParser

from django.shortcuts import render
from snippets.models import *
from snippets.serializers import *

from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view


@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'snippets': reverse('snippet-list', request=request, format=format)
	})


@csrf_exempt
def snippet_list(request):
	"""
        List all code snippets, or create a new snippet.
	"""
	if request.method == 'GET':
		serializer = SnippetSerializer(Snippet.objects.all(), many=True)
		content = JSONRenderer().render(serializer.data)
		return HttpResponse(content)
	elif request.method == 'POST':
		data = JSONParser.parse(request)
		serializer = SnippetSerializer(data=data)
		if serializer.is_valid():
			serializers.save()
			return JsonResponse(serializer.data, status=200)
		else:
			return JsonResponse(serializer.errors, status=400)



@csrf_exempt
def snippet_detail(request, pk):
	"""
        Retrieve, update or delete a code snippet.
        """
	try:
		snippet = Snippet.objects.get(pk=pk)
	except Snippet.DoesNotExist:
		return HttpResponse(status=404)

	if request.method == 'GET':
		serializer = SnippetSerializer(snippet)
		return JsonResponse(serializer.data)

	elif request.method == 'PUT':
		data = JSONParser().parse(request)
		serializer = SnippetSerializer(snippet, data=data)
		if serializer.is_valid():
			serializer.save()
			return JsonResponse(serializer.data, status=200)
		else:
			return JsonResponse(serializer.errors, status=400)
	
	elif request.method == 'DELETE':
		snippet.delete()
		return HttpResponse(status=204)


from rest_framework import status
from rest_framework.response import Response

@api_view(['GET', 'POST'])
def snippet_list_by_decorators(request, format=None):
	if request.method == 'GET':
		serializer = SnippetSerializer(Snippet.objects.all(), many=True)
		return Response(serializer.data)

	elif request.method == 'POST':
		serializer = SnippetSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED) 
		else:
			return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def snippet_detail_by_decorators(request, pk, format=None):
	try:
		snippet = Snippet.objects.get(pk=pk)
	except Snippet.DoesNotExist:
		return Response('{"msg": "not fonud"}', status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET':
		serializer = SnippetSerializer(snippet)
		return Response(serializer.data)
	
	elif request.method == 'PUT':
		serializer = SnippetSerializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED) 
		else:
			return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
	
	elif request.method == 'DELETE':
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)	


from rest_framework.views import APIView
from django.http import Http404

class Snippet_list_by_class(APIView):
	def get(self, request, *arg, **kwargs):
		snippets = Snippet.objects.all()
		serializer = SnippetSerializer(snippets, many=True)
		return Response(serializer.data)

	def post(self, request, *arg, **kwarg):
		serializer = SnippetSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED) 
		else:
			return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
	

class Snippet_detail_by_class(APIView):
	def get_object(self, pk):
		try:
			snippet = Snippet.objects.get(pk=pk)
			return snippet
		except Snippet.DoesNotExist:
			return Http404

	def get(self, request, *arg, **kwargs):
		pk = kwargs.get('pk', '')
		if not pk:
			return Http404

		snippet	= self.get_object(pk)
		serializer = SnippetSerializer(snippet)

		return Response(serializer.data)

	def put(self, request, *arg, **kwargs):
		pk = kwargs.get('pk', '')
		if not pk:
			return Http404

		snippet	= self.get_object(pk)
		serializer = SnippetSerializer(snippet, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED) 
		else:
			return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, *arg, **kwargs):
		pk = kwargs.get('pk', '')
		if not pk:
			return Http404

		snippet	= self.get_object(pk)
		snippet.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)	


from rest_framework import mixins
from rest_framework import generics

class SnippetList(mixins.ListModelMixin,
		  mixins.CreateModelMixin,
		  generics.GenericAPIView):

	serializer_class = SnippetSerializer
	queryset = Snippet.objects.all()

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)
	

class SnippetDetail(mixins.RetrieveModelMixin,
		    mixins.UpdateModelMixin,
		    mixins.DestroyModelMixin,
		    generics.GenericAPIView):

	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializer

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


class SnippetHighlight(generics.GenericAPIView):
	queryset = Snippet.objects.all()
	renderer_classes = (renderers.StaticHTMLRenderer,)

	def get(self, request, *arg, **kwargs):
		snippet = self.get_object()
		return Response(snippet.highlighted)


from snippets.permission import IsOwnerOrReadOnly

class SnippetListByGenerics(generics.ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	queryset = Snippet.objects.all()
	#serializer_class = SnippetSerializer
	serializer_class = SnippetSerializerByHyperlinked 

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)


class SnippetDetailByGenerics(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
	queryset = Snippet.objects.all()
	#serializer_class = SnippetSerializer
	serializer_class = SnippetSerializerByHyperlinked 


class UserListByGenerics(generics.ListCreateAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
	queryset = User.objects.all()
	#serializer_class = UserSerializer
	serializer_class = UserSerializerByHyperlinked 


class UserDetailByGenerics(generics.RetrieveUpdateDestroyAPIView):
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
	queryset = User.objects.all()
	#serializer_class = UserSerializer
	serializer_class = UserSerializerByHyperlinked 


#ViewSets & Routers
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

class UserViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializerByHyperlinked
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, )


class SnippetViewSet(viewsets.ModelViewSet):
	queryset = Snippet.objects.all()
	serializer_class = SnippetSerializerByHyperlinked
	permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

	@action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
	def highlight(self, request, *arg, **kwargs):
		snippet = self.get_object()
		return Response(snippet.highlighted)

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)
