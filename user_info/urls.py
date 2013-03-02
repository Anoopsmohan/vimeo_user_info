from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('user_info.views',
    url('^fetch_info/$', 'fetch_info', name='user_info_fetch'),
    url('^get_results/$', 'get_results', name='user_info_get_results'),
)
