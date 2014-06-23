from django.conf.urls import patterns, url, include
from staffing.views import ListBranchView
import django.contrib.auth

urlpatterns = patterns('staffing.views', 
    url(r'^$', 'index'),
    url(r'^register/$', 'staff_add'),
    url(r'^team/$', 'reporting_staff_add'),
    url(r'^team/leave/$', 'team_leave_list'),
    url(r'^profile/$', 'details_add'),
    url(r'^branch/add/$', 'branch_add'),
    url(r'^branch/$', ListBranchView.as_view(), name='branch-list',),
    url(r'^branch/edit/(?P<branch_id>[0-9]+)/$', 'branch_edit'),
    url(r'^branch/(?P<branch_id>[0-9]+)/$', 'branch_view'),
    url(r'^branch/(?P<branch_id>[0-9]+)/wards/$', 'ward_list'),
    url(r'^branch/(?P<branch_id>[0-9]+)/ward/add/$', 'ward_add'),
    url(r'^branch/(?P<branch_id>[0-9]+)/ward/edit/(?P<ward_id>[0-9]+)/$', 'ward_edit'),
    url(r'^branch/(?P<branch_id>[0-9]+)/ward/(?P<ward_id>[0-9]+)/$', 'ward_view'),
    url(r'^leave/add/$', 'leave_add'),
    url(r'^leave/$', 'leave_list'),
    url(r'^leave/(?P<leave_id>[0-9]+)/$', 'leave_view'),
    url(r'^roster/add/$', 'roster_add'),
    url(r'^roster/edit/(?P<roster_id>[0-9]+)/$', 'roster_add')
    #url(r'^(?P<staff_mobile>[0-9]+)/leave/$', 'apply_leave'),
    #url(r'^(?P<staff_mobile>[0-9]+)/leave/(?P<leave_id>[0-9]+)/$', 'leave_details'),
    #url(r'^(?P<staff_mobile>[0-9]+)/shifts/$', 'shifts'),
    #url(r'^(?P<staff_mobile>[0-9]+)/ward/$', 'ward'),
    #url(r'^(?P<staff_mobile>[0-9]+)/holidays/$', 'holidays'),
    #url(r'^(?P<staff_mobile>[0-9]+)/attendance/$', 'attendance'),
    #url(r'^/roster/(?P<roster_id>[0-9]+)/roster/$', ''),
)

urlpatterns += patterns('',
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
)
