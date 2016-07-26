from django.conf.urls import patterns, url
from django.conf import settings
import views

urlpatterns = patterns('',
                       url(r'^$', views.index, name='index'),
                       url(r'^SubmitTask', views.submit_task, name='SubmitTask'),
                       url(r'^SubmitTrack', views.submit_track, name='SubmitTrack'),
                       url(r'^Register', views.register, name='Register'),
                       url(r'^SubmitRun', views.submit_run, name='SubmitRun'),
                       url(r'^Login', views.user_login, name='Login'),
                       url(r'^Logout', views.user_logout, name='Logout'),
                       url(r'^UpdateProfile', views.update_profile, name='UpdateProfile'),
                       url(r'^Profile', views.profile, name='Profile'),
                       url(r'^Results/', views.result, name='Result'),
                       url(r'^Visitor/', views.visitor, name='Visitor'),
                       url(r'^get_results/', views.get_results, name='Result'),
                       url(r'^get_runs/(?P<pk>[0-9]+)', views.get_runs, name='Result'),
                       url(r'^get_runs', views.get_runs, {'pk': '-1'}, name='get_runs'),
                       url(r'^get_init_data', views.get_init_data, name='get_init_data'),
                       url(r'^get_tasks', views.get_tasks, name='get_tasks'),
                       url(r'^get_profile_picture', views.get_profile_pic, name='get_profile_picture'),
                       url(r'^get_widgets', views.get_widgets, name='get_widgets'),
                       url(r'^terms_and_conditions', views.terms, name='terms'),
                       url(r'^cookie_policy', views.cookie_policy, name='cookie_policy'),
                       url(r'^about', views.about, name='about'),
                       )

urlpatterns += patterns('', (r'^media/profile_pictures/(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT + '/profile_pictures/', 'show_indexes': True}),)
