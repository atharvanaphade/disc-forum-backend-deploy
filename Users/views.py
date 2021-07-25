from os import stat
from django.contrib.auth.models import User
from django.db.models import query
from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import response
from .models import Profile, Thread, Post, Topic
from .serializers import AccountSerializer, ThreadSerializer, PostSerializer, TopicSerializer
from rest_framework import serializers, status, mixins, generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
# Create your views here.

class CreateUserView(generics.ListCreateAPIView):
	queryset = User.objects.all()
	serializer_class = AccountSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
	queryset = User.objects.all()
	serializer_class = AccountSerializer
	permission_classes = [IsAuthenticated]

class ThreadListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
	queryset = Thread.objects.all()
	serializer_class = ThreadSerializer
	parser_classes = [MultiPartParser, FormParser]
	permission_classes = [IsAuthenticated]

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)
	
class ThreadDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
	queryset = Thread.objects.all()
	serializer_class = ThreadSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)
	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)
	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


class PostListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

class PostDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = [IsAuthenticated]

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)
	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)
	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)

class TopicListCreateView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
	queryset = Topic.objects.all()
	serializer_class = TopicSerializer
	permission_classes = [AllowAny]

	def get(self, request, *args, **kwargs):
		return self.list(request, *args, **kwargs)
	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)

class TopicDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
	queryset = Topic.objects.all()
	serializer_class = TopicSerializer
	permission_classes = [IsAdminUser, IsAuthenticated]

	def get(self, request, *args, **kwargs):
		return self.retrieve(request, *args, **kwargs)
	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)
	def delete(self, request, *args, **kwargs):
		return self.destroy(request, *args, **kwargs)


class FeedView(generics.GenericAPIView):
	permission_classes = [AllowAny]
	def get(self, request, *args, **kwargs):
		threads = Thread.objects.all().order_by("-postedAt")
		ret_dict = {"data": []}
		for thread in threads:
			temp = {}
			temp["topic"] = thread.topicID.title
			temp["content"] = thread.content
			temp["id"] = thread.pk
			temp["title"] = thread.title
			temp["postedAt"] = thread.postedAt
			temp["author"] = thread.author.username
			temp["upvotes"] = thread.upvotes
			ret_dict["data"].append(temp)
		return Response(ret_dict, status=201)
		
class ThreadView(generics.GenericAPIView):
	permission_classes = [AllowAny]
	def get(self, request, pk, *args, **kwargs):
		ret_dict = {}
		thread = Thread.objects.get(pk=pk)
		ret_dict["thread"] = {}
		ret_dict["thread"]["topic"] = thread.topicID.title
		ret_dict["thread"]["content"] = thread.content
		ret_dict["thread"]["id"] = thread.id
		ret_dict["thread"]["title"] = thread.title
		ret_dict["thread"]["postedAt"] = thread.postedAt
		ret_dict["thread"]["author"] = thread.author.username
		ret_dict["thread"]["upvotes"] = thread.upvotes

		posts = Post.objects.filter(threadID=thread.pk)
		ret_dict["posts"] = []
		for post in posts:
			temp = {}
			print(post.content)
			temp["content"] = post.content
			temp["author"] = post.author.username
			ret_dict["posts"].append(temp)
		return Response(ret_dict, status=201)

class TopicView(generics.GenericAPIView):
	permission_classes = [AllowAny]
	parser_classes = [MultiPartParser, FormParser]
	def get(self, request, pk, *args, **kargs):
		ret_dict = {}
		topic = Topic.objects.get(pk=pk)
		temp_dict = {}
		temp_dict["id"] = topic.id
		temp_dict["title"] = topic.title
		temp_dict["media"] = topic.media
		# print(request.headers["Host"])
		topic_serializer = TopicSerializer(data=temp_dict)
		print(topic_serializer)
		if topic_serializer.is_valid():
			temp = topic_serializer.data
			temp["media"] = "http://" + request.headers["Host"] + temp["media"]
		else:
			temp = "No threads found"
		# temp["title"] = topic.title
		# temp["media"] = topic.media
		ret_dict["topic"] = temp

		threads = Thread.objects.filter(topicID=topic.pk)
		ret_dict["threads"] = []
		for thread in threads:
			temp = {}
			temp["topic"] = thread.topicID.title
			temp["content"] = thread.content
			temp["id"] = thread.pk
			temp["title"] = thread.title
			temp["postedAt"] = thread.postedAt
			temp["author"] = thread.author.username
			temp["upvotes"] = thread.upvotes
			ret_dict["threads"].append(temp)
		return Response(ret_dict, status=201)

class ProfileView(generics.GenericAPIView):
	permission_classes = [IsAuthenticated]
	def get(self, request):
		ret_dict = {}
		profile = Profile.objects.get(userID=request.user)
		ret_dict["id"] = profile.userID.pk
		ret_dict["username"] = profile.userID.username
		ret_dict["organisation"] = profile.organisation
		ret_dict["upvotesGiven"] = profile.likesGiven
		# ret_dict["photo"] = profile.photo

		# profile_serializer = ProfileSerializer(data=ret_dict)
		# print(profile_serializer)
		# if profile_serializer.is_valid():
		# ret_dict["photo"] = "http://" + request.headers["Host"] + str(ret_dict["photo"])
		# else:
		return Response(ret_dict, status=200)

class MyThreadView(generics.ListAPIView):
	serializer_class = ThreadSerializer
	permission_classes = [IsAuthenticated]
	def get_queryset(self):
		user = self.request.user
		return Thread.objects.all().filter(author=user)
