from django.conf.urls import url

from . import views

app_name = 'wagtailcomments'
urlpatterns = [
    url('^add/(?P<content_type_pk>\d+)/(?P<object_pk>.*)/$',
        views.add_comment, name='add')
]
