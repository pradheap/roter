from django.shortcuts import render, render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.views.generic import ListView
from django.core.urlresolvers import reverse
from datetime import datetime, date
from staffing.models import Branch, BranchForm, Leave, LeaveForm, Staff, Roster, \
    Shift, RosterForm, ShiftFormset, WardForm, Ward, SupervisorForm, DetailsForm, Personal_Details
from staffing.forms import UserCreationForm

# Create your views here.

def index(request):
    return render_to_response('index.html', RequestContext(request,))

def reporting_staff_add(request):
    form = SupervisorForm(request.user.mobile, request.POST or None)
    if form.is_valid():
        reporting_staff = form.save(commit=False)
        reporting_staff.supervisor = request.user
        reporting_staff.save()
        return  HttpResponseRedirect("/staffing/")
    return render_to_response('reporting_staff_add.html', RequestContext(request, {'form': form}))

def details_add(request):
    form = DetailsForm(request.POST or None)
    return render_to_response('details_add.html', RequestContext(request, {'form': form}))

def team_leave_list(request):
    if request.POST and 'leaveid' in request.POST:
        leave_approve(request, request.POST['leaveid']) 
    team = Personal_Details.objects.filter(supervisor=request.user)
    leaves = Leave.objects.filter(staff_id__in=team.values('staff_id'))
    return render_to_response('team_leave_list.html', RequestContext(request, {'leaves': leaves}))    

def leave_list(request):
    leaves = Leave.objects.filter(staff_id=request.user)
    return render_to_response('leave_list.html', RequestContext(request, {'leaves': leaves}))

def branch_add(request):
    form = BranchForm(request.POST or None) 
    if form.is_valid():
        new_branch = form.save()
        return HttpResponseRedirect("/staffing/branch/")
    return render_to_response('branch_add.html', RequestContext(request, {'form': form}))

def branch_edit(request, branch_id):
    branch = get_object_or_404(Branch, pk=branch_id)
    form = BranchForm(request.POST or None, instance=branch)
    if form.is_valid():
        new_branch = form.save()
        return HttpResponseRedirect("/staffing/branch/" + branch_id)
    return render_to_response('branch_edit.html', RequestContext(request, {'form': form}))

def branch_view(request, branch_id):
    branch = get_object_or_404(Branch, pk=branch_id)
    return render_to_response('branch_view.html', RequestContext(request, {'branch': branch}))

class ListBranchView(ListView):
    model = Branch
    template_name = 'branch_list.html'

def staff_add(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        new_staff = form.save()
        return HttpResponseRedirect("/staffing/")
    return render_to_response('staff_add.html', RequestContext(request, {'UserForm': form}))

def leave_add(request):
    form = LeaveForm(request.POST or None)
    if form.is_valid():
        leave = form.save(commit=False)
        leave.staff = request.user
        leave.status = 'open'
        leave.save()
        #To-Do
        #Send email/sms to suprvisor
        return HttpResponseRedirect("/staffing/")
    return render_to_response('leave_add.html', RequestContext(request, {'LeaveForm': form}))

def leave_view(request, leave_id):
    leave = get_object_or_404(Leave, pk=leave_id)
    return render_to_response('leave_view.html', RequestContext(request, {'leave': leave}))

def leave_approve(request, leave_id):
    leave = get_object_or_404(Leave, pk=leave_id)
    
    if leave.status == 'open' and request.method == 'POST':
       leave_obj = Leave.objects.get(pk=leave_id)
       if 'approve' in request.POST:
           leave_obj.status = 'approved' 
       elif 'reject' in request.POST:
           leave_obj.status = 'rejected'
       elif 'withhold' in request.POST:
           leave_obj.status = 'withhold'
       leave_obj.approved_on = date.today()
       leave_obj.approved_by = request.user
       leave_obj.comments = request.REQUEST['comments']
       leave_obj.save(update_fields=['comments', 'status', 'approved_on', 'approved_by',])
       #To-Do
       #Send the applicant the status of the leave by email/sms
    return

def ward_add(request, branch_id):
    form = WardForm(request.POST or None)
    if request.method == 'POST':
       if form.is_valid():
           form.save()
           return HttpResponseRedirect("/staffing/ward/")
    return render_to_response('ward_add.html', RequestContext(request, {'WardForm': form}))

def ward_edit(request, branch_id, ward_id):
    ward = get_object_or_404(Ward, pk=ward_id)
    form = WardForm(request.POST or None, instance=ward)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/staffing/ward/" + ward_id)
    return render_to_response('ward_edit.html', RequestContext(request, {'WardForm': form}))

def ward_view(request, branch_id, ward_id):
    ward = get_object_or_404(Ward, pk=ward_id)
    return render_to_response('ward_view.html', RequestContext(request, {'ward': ward}))

def ward_list(request, branch_id):
    wards = Ward.objects.filter(branch=branch_id)
    return render_to_response('ward_list.html', RequestContext(request, {'wards': wards}))

def roster_add(request, roster_id=None):
    if roster_id is not None:
        instance = Roster.objects.get(pk=roster_id)
    else:
        instance = Roster()

    if request.method == 'POST':
        form = RosterForm(request.POST, instance=instance)
        if 'add' in request.POST:
            cp = request.POST.copy()
            cp['shift-TOTAL_FORMS'] = int(cp['shift-TOTAL_FORMS'])+ 1
            shift_formset = ShiftFormset(cp, prefix='shift', instance=instance)
        elif 'submit' in request.POST:
            if form.is_valid():
                roster = form.save(commit=False)
                roster.drafted_by = request.user
                roster.save()
                shift_formset = ShiftFormset(request.POST,
                    request.FILES, instance=roster, prefix='shift')
                if shift_formset.is_valid():
                    shift_formset.save()
                    return HttpResponseRedirect('/staffing/')
    else:
        form = RosterForm(instance=instance)
        shift_formset = ShiftFormset(prefix='shift', instance=instance)
    return render_to_response('roster_add.html', {'shift_formset': shift_formset, 'form': form,}, context_instance=RequestContext(request))
