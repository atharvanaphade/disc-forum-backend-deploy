from .views import CreateUserView, FeedView, MyThreadView, PostListCreateView, ThreadView, TopicView, ProfileView, UserDetailView, ThreadListCreateView, ThreadDetailView, TopicListCreateView, TopicDetailView
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
	path('user/', CreateUserView.as_view()),
	path('user/<int:pk>', UserDetailView.as_view()),
	path('thread/', ThreadListCreateView.as_view()),
	path('thread/<int:pk>', ThreadDetailView.as_view()),
	path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('topic/', TopicListCreateView.as_view()),
	path('topic/<int:pk>', TopicDetailView.as_view()),
	path('api-auth/', include('rest_framework.urls')),
	path('feed/', FeedView.as_view()),
	path('createpost/', PostListCreateView.as_view()),
	path('viewthread/<int:pk>', ThreadView.as_view()),
	path('viewtopic/<int:pk>', TopicView.as_view()),
	path('viewprofile/', ProfileView.as_view()),
	path('mythreads/', MyThreadView.as_view()),
]