from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings
from django.db.models import Q


def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'tickets/index.html')


# for showing signup/login button for customer
def agentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'tickets/agentclick.html')


# for showing signup/login button for tehnicians
def tehnicianclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'tickets/tehnicianclick.html')


# for showing signup/login button for ADMIN(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return HttpResponseRedirect('adminlogin')


def agent_signup_view(request):
    userForm = forms.AgentUserForm()
    agentForm = forms.AgentForm()
    mydict = {'userForm': userForm, 'agentForm': agentForm}
    if request.method == 'POST':
        userForm = forms.AgentUserForm(request.POST)
        agentForm = forms.AgentForm(request.POST, request.FILES)
        if userForm.is_valid() and agentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            agent = agentForm.save(commit=False)
            agent.user = user
            agent.save()
            lista_agenti = Group.objects.get_or_create(name='AGENTI')
            lista_agenti[0].user_set.add(user)
        return HttpResponseRedirect('agentlogin')
    return render(request, 'tickets/agentsignup.html', context=mydict)


def tehnician_signup_view(request):
    userForm = forms.TehnicianUserForm()
    tehnicianForm = forms.TehnicianForm()
    mydict = {'userForm': userForm, 'tehnicianForm': tehnicianForm}
    if request.method == 'POST':
        userForm = forms.TehnicianUserForm(request.POST)
        tehnicianForm = forms.TehnicianForm(request.POST, request.FILES)
        if userForm.is_valid() and tehnicianForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            tehnician = tehnicianForm.save(commit=False)
            tehnician.user = user
            tehnician.save()
            lista_tehnicieni = Group.objects.get_or_create(name='TEHNICIAN')
            lista_tehnicieni[0].user_set.add(user)
        return HttpResponseRedirect('tehnicianlogin')
    return render(request, 'tickets/tehniciansignup.html', context=mydict)


# for checking user customer, mechanic or admin(by sumit)
def is_agent(user):
    return user.groups.filter(name='AGENT').exists()


def is_tehnician(user):
    return user.groups.filter(name='TEHNICIAN').exists()


def afterlogin_view(request):
    if is_agent(request.user):
        return redirect('agent-dashboard')
    elif is_tehnician(request.user):
        accountapproval = models.Tehnician.objects.all().filter(user_id=request.user.id, status=True)
        if accountapproval:
            return redirect('tehnician-dashboard')
        else:
            return render(request, 'tickets/tehnician_wait_for_approval.html')
    else:
        return redirect('admin-dashboard')


# ============================================================================================
# ADMIN RELATED views start
# ============================================================================================

@login_required(login_url='adminlogin')
def admin_dashboard_view(request):
    enquiry = models.Request.objects.all().order_by('-id')
    agents = []
    for enq in enquiry:
        agent = models.Agent.objects.get(id=enq.customer_id)
        agents.append(agent)
    dict = {
        'total_agent': models.Agent.objects.all().count(),
        'total_tehnician': models.Tehnician.objects.all().count(),
        'total_request': models.Request.objects.all().count(),
        'total_feedback': models.Feedback.objects.all().count(),
        'data': zip(agents, enquiry),
    }
    return render(request, 'tickets/admin_dashboard.html', context=dict)


@login_required(login_url='adminlogin')
def admin_agent_view(request):
    return render(request, 'tickets/admin_agent.html')


@login_required(login_url='adminlogin')
def admin_view_agent_view(request):
    agenti = models.Agent.objects.all()
    return render(request, 'tickets/admin_view_agent.html', {'agenti': agenti})


@login_required(login_url='adminlogin')
def delete_agent_view(request, pk):
    agent = models.Agent.objects.get(id=pk)
    user = models.User.objects.get(id=agent.user_id)
    user.delete()
    agent.delete()
    return redirect('admin-view-agent')


@login_required(login_url='adminlogin')
def update_agent_view(request, pk):
    agent = models.Agent.objects.get(id=pk)
    user = models.User.objects.get(id=agent.user_id)
    userForm = forms.AgentUserForm(instance=user)
    agentForm = forms.AgentForm(request.FILES, instance=agent)
    mydict = {'userForm': userForm, 'agentForm': agentForm}
    if request.method == 'POST':
        userForm = forms.AgentUserForm(request.POST, instance=user)
        agentForm = forms.AgentForm(request.POST, request.FILES, instance=agent)
        if userForm.is_valid() and agentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            agentForm.save()
            return redirect('admin-view-agent')
    return render(request, 'tickets/update_agent.html', context=mydict)


@login_required(login_url='adminlogin')
def admin_add_agent_view(request):
    userForm = forms.AgentUserForm()
    agentForm = forms.AgentForm()
    mydict = {'userForm': userForm, 'agentForm': agentForm}
    if request.method == 'POST':
        userForm = forms.AgentUserForm(request.POST)
        agentForm = forms.AgentForm(request.POST, request.FILES)
        if userForm.is_valid() and agentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            agent = agentForm.save(commit=False)
            agent.user = user
            agent.save()
            lista_agenti = Group.objects.get_or_create(name='AGENT')
            lista_agenti[0].user_set.add(user)
        return HttpResponseRedirect('/admin-view-agent')
    return render(request, 'tickets/admin_add_agent.html', context=mydict)


@login_required(login_url='adminlogin')
def admin_view_agent_enquiry_view(request):
    enquiry = models.Request.objects.all().order_by('-id')
    agenti = []
    for enq in enquiry:
        agent = models.Agent.objects.get(id=enq.agent_id)
        agenti.append(agent)
    return render(request, 'tickets/admin_view_agent_enquiry.html', {'data': zip(agenti, enquiry)})


@login_required(login_url='adminlogin')
def admin_view_agent_deviz_view(request):
    enquiry = models.Request.objects.values('agent_id').annotate(Sum('cost'))
    print(enquiry)
    agenti = []
    for enq in enquiry:
        print(enq)
        agent = models.Agent.objects.get(id=enq['agent_id'])
        agenti.append(agent)
    return render(request, 'tickets/admin_view_agent_deviz.html', {'data': zip(agenti, enquiry)})


@login_required(login_url='adminlogin')
def admin_tehnician_view(request):
    return render(request, 'tickets/admin_tehnician.html')


@login_required(login_url='adminlogin')
def admin_approve_tehnician_view(request):
    tehnicieni = models.Tehnician.objects.all().filter(status=False)
    return render(request, 'tickets/admin_approve_tehnician.html', {'tehnicieni': tehnicieni})


@login_required(login_url='adminlogin')
def approve_tehnician_view(request, pk):
    tehnicianSpecialize = forms.TehnicianForm()
    if request.method == 'POST':
        tehnicianSpecialize = forms.TehnicianForm(request.POST)
        if tehnicianSpecialize.is_valid():
            tehnician = models.Tehnician.objects.get(id=pk)
            tehnician.specializare = tehnicianSpecialize.cleaned_data['specializare']
            tehnician.status = True
            tehnician.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-tehnicians')
    return render(request, 'tickets/admin_approve_tehnician_details.html', {'tehnicianSpecialize': tehnicianSpecialize})


@login_required(login_url='adminlogin')
def delete_tehnician_view(request, pk):
    tehnician = models.Tehnician.objects.get(id=pk)
    user = models.User.objects.get(id=tehnician.user_id)
    user.delete()
    tehnician.delete()
    return redirect('admin-approve-tehnician')


@login_required(login_url='adminlogin')
def admin_add_tehnician_view(request):
    userForm = forms.TehnicianUserForm()
    tehnicianForm = forms.TehnicianForm()
    tehnicianSpecialize = forms.TehnicianSpecializeForm()
    mydict = {'userForm': userForm, 'tehnicianForm': tehnicianForm, 'tehnicianSpecialize': tehnicianSpecialize}
    if request.method == 'POST':
        userForm = forms.TehnicianUserForm(request.POST)
        tehnicianForm = forms.TehnicianForm(request.POST, request.FILES)
        tehnicianSpecialize = forms.TehnicianSpecializeForm(request.POST)
        if userForm.is_valid() and tehnicianForm.is_valid() and tehnicianSpecialize.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            tehnician = tehnicianForm.save(commit=False)
            tehnician.user = user
            tehnician.status = True
            tehnician.salary = tehnicianSpecialize.cleaned_data['specializare']
            tehnician.save()
            lista_tehnicieni = Group.objects.get_or_create(name='TEHNICIAN')
            lista_tehnicieni[0].user_set.add(user)
            return HttpResponseRedirect('admin-view-tehnician')
        else:
            print('problem in form')
    return render(request, 'tickets/admin_add_tehnicieni.html', context=mydict)


@login_required(login_url='adminlogin')
def admin_view_tehnician_view(request):
    tehnicieni = models.Tehnician.objects.all()
    return render(request, 'tickets/admin_view_tehnician.html', {'tehnicieni': tehnicieni})


@login_required(login_url='adminlogin')
def delete_tehnician_view(request, pk):
    tehnician = models.Tehnician.objects.get(id=pk)
    user = models.User.objects.get(id=tehnician.user_id)
    user.delete()
    tehnician.delete()
    return redirect('admin-view-tehnician')


@login_required(login_url='adminlogin')
def update_tehnician_view(request, pk):
    tehnician = models.Tehnician.objects.get(id=pk)
    user = models.User.objects.get(id=tehnician.user_id)
    userForm = forms.TehnicianUserForm(instance=user)
    tehnicianForm = forms.TehnicianForm(request.FILES, instance=tehnician)
    mydict = {'userForm': userForm, 'tehnicianForm': tehnicianForm}
    if request.method == 'POST':
        userForm = forms.TehnicianUserForm(request.POST, instance=user)
        tehnicianForm = forms.TehnicianForm(request.POST, request.FILES, instance=tehnician)
        if userForm.is_valid() and tehnicianForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            tehnicianForm.save()
            return redirect('admin-view-tehnician')
    return render(request, 'tickets/update_tehnician.html', context=mydict)


@login_required(login_url='adminlogin')
def admin_view_tehnician_specialize_view(request):
    tehnicieni = models.Tehnician.objects.all()
    return render(request, 'tickets/admin_view_tehnician_specialize.html', {'tehnicieni': tehnicieni})


@login_required(login_url='adminlogin')
def update_specialize_view(request, pk):
    tehnicianSpecialize = forms.TehnicianSpecializeForm()
    if request.method == 'POST':
        tehnicianSpecialize = forms.TehnicianSpecializeForm(request.POST)
        if tehnicianSpecialize.is_valid():
            tehnician = models.Tehnician.objects.get(id=pk)
            tehnician.salary = tehnicianSpecialize.cleaned_data['salary']
            tehnician.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-tehnician-salary')
    return render(request, 'tickets/admin_approve_tehnician_details.html', {'tehnicianSpecialize': tehnicianSpecialize})


@login_required(login_url='adminlogin')
def admin_request_view(request):
    return render(request, 'tickets/admin_report.html')


@login_required(login_url='adminlogin')
def admin_view_request_view(request):
    enquiry = models.Request.objects.all().order_by('-id')
    agenti = []
    for enq in enquiry:
        agent = models.Agent.objects.get(id=enq.agent_id)
        agenti.append(agent)
    return render(request, 'tickets/admin_view_request.html', {'data': zip(agenti, enquiry)})


@login_required(login_url='adminlogin')
def change_status_view(request, pk):
    adminenquiry = forms.AdminApproveRequestForm()
    if request.method == 'POST':
        adminenquiry = forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x = models.Request.objects.get(id=pk)
            enquiry_x.tehnician = adminenquiry.cleaned_data['tehnician']
            enquiry_x.cost = adminenquiry.cleaned_data['cost']
            enquiry_x.status = adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-request')
    return render(request, 'vehicle/admin_approve_request_details.html', {'adminenquiry': adminenquiry})


@login_required(login_url='adminlogin')
def admin_delete_request_view(request, pk):
    requests = models.Request.objects.get(id=pk)
    requests.delete()
    return redirect('admin-view-request')


@login_required(login_url='adminlogin')
def admin_add_request_view(request):
    enquiry = forms.RequestForm()
    adminenquiry = forms.AdminRequestForm()
    mydict = {'enquiry': enquiry, 'adminenquiry': adminenquiry}
    if request.method == 'POST':
        enquiry = forms.RequestForm(request.POST)
        adminenquiry = forms.AdminRequestForm(request.POST)
        if enquiry.is_valid() and adminenquiry.is_valid():
            enquiry_x = enquiry.save(commit=False)
            enquiry_x.customer = adminenquiry.cleaned_data['agent']
            enquiry_x.tehnician = adminenquiry.cleaned_data['tehnician']
            enquiry_x.cost = adminenquiry.cleaned_data['cost']
            enquiry_x.status = 'Aprobat'
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-view-request')
    return render(request, 'vehicle/admin_add_request.html', context=mydict)


@login_required(login_url='adminlogin')
def admin_approve_request_view(request):
    enquiry = models.Request.objects.all().filter(status='Pending')
    return render(request, 'tickets/admin_approve_request.html', {'enquiry': enquiry})


@login_required(login_url='adminlogin')
def approve_request_view(request, pk):
    adminenquiry = forms.AdminApproveRequestForm()
    if request.method == 'POST':
        adminenquiry = forms.AdminApproveRequestForm(request.POST)
        if adminenquiry.is_valid():
            enquiry_x = models.Request.objects.get(id=pk)
            enquiry_x.mechanic = adminenquiry.cleaned_data['tehnician']
            enquiry_x.cost = adminenquiry.cleaned_data['cost']
            enquiry_x.status = adminenquiry.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-approve-request')
    return render(request, 'tickets/admin_approve_request_details.html', {'adminenquiry': adminenquiry})


@login_required(login_url='adminlogin')
def admin_view_service_cost_view(request):
    enquiry = models.Request.objects.all().order_by('-id')
    agenti = []
    for enq in enquiry:
        agent = models.Agent.objects.get(id=enq.customer_id)
        agenti.append(agent)
    print(agenti)
    return render(request, 'vehicle/admin_view_service_cost.html', {'data': zip(agenti, enquiry)})


@login_required(login_url='adminlogin')
def update_cost_view(request, pk):
    updateCostForm = forms.UpdateCostForm()
    if request.method == 'POST':
        updateCostForm = forms.UpdateCostForm(request.POST)
        if updateCostForm.is_valid():
            enquiry_x = models.Request.objects.get(id=pk)
            enquiry_x.cost = updateCostForm.cleaned_data['cost']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/admin-view-service-cost')
    return render(request, 'tickets/update_cost.html', {'updateCostForm': updateCostForm})


@login_required(login_url='adminlogin')
def admin_tehnician_attendance_view(request):
    return render(request, 'tickets/admin_tehnician_attendance.html')


@login_required(login_url='adminlogin')
def admin_take_attendance_view(request):
    tehnicieni = models.Tehnician.objects.all().filter(status=True)
    aform = forms.AttendanceForm()
    if request.method == 'POST':
        form = forms.AttendanceForm(request.POST)
        if form.is_valid():
            Attendances = request.POST.getlist('present_status')
            date = form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel = models.Attendance()

                AttendanceModel.date = date
                AttendanceModel.present_status = Attendances[i]
                print(tehnicieni[i].id)
                print(int(tehnicieni[i].id))
                tehnician = models.Tehnician.objects.get(id=int(tehnicieni[i].id))
                AttendanceModel.tehnician = tehnician
                AttendanceModel.save()
            return redirect('admin-view-attendance')
        else:
            print('form invalid')
    return render(request, 'tickets/admin_take_attendance.html', {'tehnicieni': tehnicieni, 'aform': aform})


@login_required(login_url='adminlogin')
def admin_report_view(request):
    reports = models.Request.objects.all().filter(Q(status="Reparat") | Q(status="Trimis"))
    dict = {
        'reports': reports,
    }
    return render(request, 'tickets/admin_report.html', context=dict)


@login_required(login_url='adminlogin')
def admin_feedback_view(request):
    feedback = models.Feedback.objects.all().order_by('-id')
    return render(request, 'tickets/admin_feedback.html', {'feedback': feedback})


# ============================================================================================
# ADMIN RELATED views END
# ============================================================================================


# ============================================================================================
# CUSTOMER RELATED views start
# ============================================================================================
@login_required(login_url='agentlogin')
@user_passes_test(is_agent)
def agent_dashboard_view(request):
    agent = models.Agent.objects.get(user_id=request.user.id)
    work_in_progress = models.Request.objects.all().filter(customer_id=agent.id, status='Repairing').count()
    work_completed = models.Request.objects.all().filter(customer_id=agent.id).filter(
        Q(status="Reparat") | Q(status="Trimis")).count()
    new_request_made = models.Request.objects.all().filter(customer_id=agent.id).filter(
        Q(status="In Asteptare") | Q(status="Aprobat")).count()
    bill = models.Request.objects.all().filter(customer_id=agent.id).filter(
        Q(status="Reparat") | Q(status="Trimis")).aggregate(Sum('cost'))
    print(bill)
    dict = {
        'work_in_progress': work_in_progress,
        'work_completed': work_completed,
        'new_request_made': new_request_made,
        'bill': bill['cost__sum'],
        'agent': agent,
    }
    return render(request, 'tickets/agent_dashboard.html', context=dict)


@login_required(login_url='agentlogin')
@user_passes_test(is_agent)
def agent_request_view(request):
    agent = models.Agent.objects.get(user_id=request.user.id)
    return render(request, 'tickets/agent_request.html', {'agent': agent})


@login_required(login_url='agentlogin')
@user_passes_test(is_agent)
def agent_view_request_view(request):
    agent = models.Agent.objects.get(user_id=request.user.id)
    enquiries = models.Request.objects.all().filter(customer_id=agent.id, status="In asteptare")
    return render(request, 'tickets/agent_view_request.html', {'agent': agent, 'enquiries': enquiries})


@login_required(login_url='agentlogin')
@user_passes_test(is_agent)
def agent_delete_request_view(request, pk):
    agent = models.Agent.objects.get(user_id=request.user.id)
    enquiry = models.Request.objects.get(id=pk)
    enquiry.delete()
    return redirect('agent-view-request')


@login_required(login_url='agentlogin')
@user_passes_test(is_agent)
def agent_view_approved_request_view(request):
    agent = models.Agent.objects.get(user_id=request.user.id)
    enquiries = models.Request.objects.all().filter(agent_id=agent.id).exclude(status='In Asteptare')
    return render(request, 'tickets/agent_view_approved_request.html',
                  {'agent': agent, 'enquiries': enquiries})


@login_required(login_url='agentlogin')
@user_passes_test(is_agent)
def agent_view_approved_request_deviz_view(request):
    agent = models.Agent.objects.get(user_id=request.user.id)
    enquiries = models.Request.objects.all().filter(agent_id=agent.id).exclude(status='In Asteptare')
    return render(request, 'tickets/agent_view_approved_request_deviz.html',
                  {'agent': agent, 'enquiries': enquiries})


@login_required(login_url='agentlogin')
@user_passes_test(is_agent)
def agent_add_request_view(request):
    agent = models.Agent.objects.get(user_id=request.user.id)
    enquiry = forms.RequestForm()
    if request.method == 'POST':
        enquiry = forms.RequestForm(request.POST)
        if enquiry.is_valid():
            agent = models.Agent.objects.get(user_id=request.user.id)
            enquiry_x = enquiry.save(commit=False)
            enquiry_x.agent = agent
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('agent-dashboard')
    return render(request, 'tickets/agent_add_request.html', {'enquiry': enquiry, 'agent': agent})


@login_required(login_url='agentlogin')
@user_passes_test(is_agent)
def agent_profile_view(request):
    agent = models.Agent.objects.get(user_id=request.user.id)
    return render(request, 'tickets/agent_profile.html', {'agent': agent})


@login_required(login_url='agentlogin')
@user_passes_test(is_agent)
def edit_agent_profile_view(request):
    agent = models.Agent.objects.get(user_id=request.user.id)
    user = models.User.objects.get(id=agent.user_id)
    userForm = forms.AgentUserForm(instance=user)
    customerForm = forms.AgentForm(request.FILES, instance=agent)
    mydict = {'userForm': userForm, 'agentForm': customerForm, 'agent': agent}
    if request.method == 'POST':
        userForm = forms.AgentUserForm(request.POST, instance=user)
        agentForm = forms.AgentForm(request.POST, instance=agent)
        if userForm.is_valid() and agentForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            customerForm.save()
            return HttpResponseRedirect('agent-profile')
    return render(request, 'tickets/edit_agent_profile.html', context=mydict)


@login_required(login_url='agentlogin')
@user_passes_test(is_agent)
def agent_deviz_view(request):
    agent = models.Agent.objects.get(user_id=request.user.id)
    enquiries = models.Request.objects.all().filter(customer_id=agent.id).exclude(status='In asteptare')
    return render(request, 'tickets/agent_deviz.html', {'agent': agent, 'enquiries': enquiries})


@login_required(login_url='agentlogin')
@user_passes_test(is_agent)
def agent_feedback_view(request):
    agent = models.Agent.objects.get(user_id=request.user.id)
    feedback = forms.FeedbackForm()
    if request.method == 'POST':
        feedback = forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request, 'tickets/feedback_sent_by_agent.html', {'agent': agent})
    return render(request, 'tickets/agent_feedback.html', {'feedback': feedback, 'agent': agent})


# ============================================================================================
# CUSTOMER RELATED views END
# ============================================================================================


@login_required(login_url='tehnicianlogin')
@user_passes_test(is_tehnician)
def tehnician_dashboard_view(request):
    tehnician = models.Tehnician.objects.get(user_id=request.user.id)
    work_in_progress = models.Request.objects.all().filter(tehnician_id=tehnician.id, status='In repartie').count()
    work_completed = models.Request.objects.all().filter(tehnician_id=tehnician.id, status='Reparat').count()
    new_work_assigned = models.Request.objects.all().filter(tehnician_id=tehnician.id, status='Aprobat').count()
    dict = {
        'work_in_progress': work_in_progress,
        'work_completed': work_completed,
        'new_work_assigned': new_work_assigned,
        'specializare': tehnician.specializare,
        'mechanic': tehnician,
    }
    return render(request, 'tickets/tehnician_dashboard.html', context=dict)


@login_required(login_url='tehnicianlogin')
@user_passes_test(is_tehnician)
def tehnician_work_assigned_view(request):
    tehnician = models.Tehnician.objects.get(user_id=request.user.id)
    works = models.Request.objects.all().filter(tehnician_id=tehnician.id)
    return render(request, 'tickets/tehnician_work_assigned.html', {'works': works, 'tehnician': tehnician})


@login_required(login_url='tehnicianlogin')
@user_passes_test(is_tehnician)
def tehnician_update_status_view(request, pk):
    tehnician = models.Tehnician.objects.get(user_id=request.user.id)
    updateStatus = forms.TehnicianUpdateStatusForm()
    if request.method == 'POST':
        updateStatus = forms.TehnicianUpdateStatusForm(request.POST)
        if updateStatus.is_valid():
            enquiry_x = models.Request.objects.get(id=pk)
            enquiry_x.status = updateStatus.cleaned_data['status']
            enquiry_x.save()
        else:
            print("form is invalid")
        return HttpResponseRedirect('/tehnician-work-assigned')
    return render(request, 'tickets/tehnician_update_status.html',
                  {'updateStatus': updateStatus, 'tehnician': tehnician})


@login_required(login_url='tehnicianlogin')
@user_passes_test(is_tehnician)
def tehnician_attendance_view(request):
    tehnician = models.Tehnician.objects.get(user_id=request.user.id)
    attendaces = models.Attendance.objects.all().filter(tehnician=tehnician)
    return render(request, 'tickets/tehnician_view_attendance.html', {'attendaces': attendaces, 'tehnician': tehnician})


@login_required(login_url='tehnicianlogin')
@user_passes_test(is_tehnician)
def tehnician_feedback_view(request):
    tehnician = models.Tehnician.objects.get(user_id=request.user.id)
    feedback = forms.FeedbackForm()
    if request.method == 'POST':
        feedback = forms.FeedbackForm(request.POST)
        if feedback.is_valid():
            feedback.save()
        else:
            print("form is invalid")
        return render(request, 'tickets/tehnician_sent.html', {'tehnician': tehnician})
    return render(request, 'tickets/tehnician_feedback.html', {'feedback': feedback, 'tehnician': tehnician})


@login_required(login_url='tehnicianlogin')
@user_passes_test(is_tehnician)
def tehnician_specializare_view(request):
    tehnician = models.Tehnician.objects.get(user_id=request.user.id)
    workdone = models.Request.objects.all().filter(mechanic_id=tehnician.id).filter(
        Q(status="Repairing Done") | Q(status="Released"))
    return render(request, 'tickets/tehnician_specializare.html', {'workdone': workdone, 'tehnician': tehnician})


@login_required(login_url='tehnicianlogin')
@user_passes_test(is_tehnician)
def tehnician_profile_view(request):
    tehnician = models.Tehnician.objects.get(user_id=request.user.id)
    return render(request, 'tickets/tehnician_profile.html', {'tehnician': tehnician})


@login_required(login_url='tehnicianlogin')
@user_passes_test(is_tehnician)
def edit_tehnician_profile_view(request):
    tehnician = models.Tehnician.objects.get(user_id=request.user.id)
    user = models.User.objects.get(id=tehnician.user_id)
    userForm = forms.TehnicianUserForm(instance=user)
    tehnicianForm = forms.TehnicianForm(request.FILES, instance=tehnician)
    mydict = {'userForm': userForm, 'tehnicianForm': tehnicianForm, 'tehnician': tehnician}
    if request.method == 'POST':
        userForm = forms.TehnicianUserForm(request.POST, instance=user)
        tehnicianForm = forms.TehnicianForm(request.POST, request.FILES, instance=tehnician)
        if userForm.is_valid() and tehnicianForm.is_valid():
            user = userForm.save()
            user.set_password(user.password)
            user.save()
            tehnicianForm.save()
            return redirect('tehnician-profile')
    return render(request, 'tickets/edit_tehnician_profile.html', context=mydict)


# ============================================================================================
# MECHANIC RELATED views start
# ============================================================================================


# for aboutus and contact
def aboutus_view(request):
    return render(request, 'tickets/aboutus.html')


def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name) + ' || ' + str(email), message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER,
                      fail_silently=False)
            return render(request, 'tickets/contactussuccess.html')
    return render(request, 'tickets/contactus.html', {'form': sub})
