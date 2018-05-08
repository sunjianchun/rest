#encoding: utf-8
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import renderers
from snippets import views
'''
urlpatterns = [
    #url(r'^snippets/$', views.snippet_list),
    #url(r'^snippets/(?P<pk>[0-9]+)$', views.snippet_detail),
    #url(r'snippets/$', views.snippet_list_by_decorators),
    #url(r'^snippets/(?P<pk>[0-9]+)$', views.snippet_detail_by_decorators),
    #url(r'^snippets/$', views.Snippet_list_by_class.as_view()),
    #url(r'^snippets/(?P<pk>[0-9]+)$', views.Snippet_detail_by_class.as_view()),
    #url(r'^snippets/$', views.SnippetList.as_view()),
    #url(r'^snippets/(?P<pk>[0-9]+)$', views.SnippetDetail.as_view()),
    url(r'^$', views.api_root),
    url(r'^snippets/$', views.SnippetListByGenerics.as_view(), name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)$', views.SnippetDetailByGenerics.as_view(), name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', views.SnippetHighlight.as_view(), name='snippet-highligh'),
    url(r'^users/$', views.UserListByGenerics.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)$', views.UserDetailByGenerics.as_view(), name='user-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
'''

'''
#ViewSets & Routers
snippet_list = views.SnippetViewSet.as_view({
	'get': 'list',
	'post': 'create',
})

snippet_detail = views.SnippetViewSet.as_view({
	'get': 'retrieve',
	'put': 'update',
	'delete': 'destroy'
})

snippet_highlight = views.SnippetViewSet.as_view({
	'get': 'highlight'
}, renderer_classes=[renderers.StaticHTMLRenderer])

user_list = views.UserViewSet.as_view({
	'get': 'list'
})

user_detail = views.UserViewSet.as_view({
	'get': 'retrieve',
})

urlpatterns = [
    url(r'^$', views.api_root),
    url(r'^snippets/$', snippet_list, name='snippet-list'),
    url(r'^snippets/(?P<pk>[0-9]+)$', snippet_detail, name='snippet-detail'),
    url(r'^snippets/(?P<pk>[0-9]+)/highlight/$', snippet_highlight, name='snippet-highligh'),
    url(r'^users/$', user_list, name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)$', user_detail, name='user-detail'),
]
'''

from rest_framework.routers import DefaultRouter
from django.conf.urls import include

router = DefaultRouter()
router.register(r'snippets', views.SnippetViewSet)
router.register(r'users', views.UserViewSet)

urlpatterns = [
	url(r'^', include(router.urls))
]

