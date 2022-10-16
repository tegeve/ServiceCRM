from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from tickets import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name=''),
    path('adminclick', views.adminclick_view),
    path('agentclick', views.agentclick_view),
    path('tehnicianclick', views.tehnicianclick_view),

    path('agentsignup', views.agent_signup_view, name='agentsignup'),
    path('tehniciansignup', views.tehnician_signup_view, name='tehniciansignup'),

    path('agentlogin', LoginView.as_view(template_name='tickets/agentlogin.html'), name='agentlogin'),
    path('tehnicianlogin', LoginView.as_view(template_name='tickets/tehnicianlogin.html'), name='tehnicianlogin'),
    path('adminlogin', LoginView.as_view(template_name='tickets/adminlogin.html'), name='adminlogin'),

    path('admin-dashboard', views.admin_dashboard_view, name='admin-dashboard'),

    path('admin-agent', views.admin_agent_view, name='admin-agent'),
    path('admin-view-agent', views.admin_view_agent_view, name='admin-view-agent'),
    path('delete-agent/<int:pk>', views.delete_agent_view, name='delete-agent'),
    path('update-agent/<int:pk>', views.update_agent_view, name='update-agent'),
    path('admin-add-agent', views.admin_add_agent_view, name='admin-add-agent'),
    path('admin-view-agent-enquiry', views.admin_view_agent_enquiry_view, name='admin-view-agent-enquiry'),
    path('admin-view-agent-deviz', views.admin_view_agent_deviz_view, name='admin-view-agent-deviz'),

    path('admin-request', views.admin_request_view, name='admin-request'),
    path('admin-view-request', views.admin_view_request_view, name='admin-view-request'),
    path('change-status/<int:pk>', views.change_status_view, name='change-status'),
    path('admin-delete-request/<int:pk>', views.admin_delete_request_view, name='admin-delete-request'),
    path('admin-add-request', views.admin_add_request_view, name='admin-add-request'),
    path('admin-approve-request', views.admin_approve_request_view, name='admin-approve-request'),
    path('approve-request/<int:pk>', views.approve_request_view, name='approve-request'),

    path('admin-view-service-cost', views.admin_view_service_cost_view, name='admin-view-service-cost'),
    path('update-cost/<int:pk>', views.update_cost_view, name='update-cost'),

    path('admin-tehnician', views.admin_tehnician_view, name='admin-tehnician'),
    path('admin-view-tehnician', views.admin_view_tehnician_view, name='admin-view-tehnician'),
    path('delete-tehnician/<int:pk>', views.delete_tehnician_view, name='delete-tehnician'),
    path('update-tehnician/<int:pk>', views.update_tehnician_view, name='update-tehnician'),
    path('admin-add-tehnician', views.admin_add_tehnician_view, name='admin-add-tehnician'),
    path('admin-approve-tehnician', views.admin_approve_tehnician_view, name='admin-approve-tehnician'),
    path('approve-tehnician/<int:pk>', views.approve_tehnician_view, name='approve-tehnician'),
    path('delete-tehnician/<int:pk>', views.delete_tehnician_view, name='delete-tehnician'),
    path('admin-view-tehnician-specialize', views.admin_view_tehnician_specialize_view, name='admin-view-tehnician'
                                                                                             '-specialize'),
    path('update-specialize/<int:pk>', views.update_specialize_view, name='update-specialize'),

    path('admin-tehnician-attendance', views.admin_tehnician_attendance_view, name='admin-tehnician-attendance'),
    path('admin-take-attendance', views.admin_take_attendance_view, name='admin-take-attendance'),
    # path('admin-view-attendance', views.admin_view_attendance_view, name='admin-view-attendance'),
    path('admin-feedback', views.admin_feedback_view, name='admin-feedback'),

    path('admin-report', views.admin_report_view, name='admin-report'),

    path('tehnician-dashboard', views.tehnician_dashboard_view, name='tehnician-dashboard'),
    path('tehnician-work-assigned', views.tehnician_work_assigned_view, name='tehnician-work-assigned'),
    path('tehnician-update-status/<int:pk>', views.tehnician_update_status_view, name='tehnician-update-status'),
    path('tehnician-feedback', views.tehnician_feedback_view, name='tehnician-feedback'),
    path('tehnician-specializare', views.tehnician_specializare_view, name='tehnician-specializare'),
    path('tehnician-profile', views.tehnician_profile_view, name='tehnician-profile'),
    path('edit-tehnician-profile', views.edit_tehnician_profile_view, name='edit-tehnician-profile'),

    path('tehnician-attendance', views.tehnician_attendance_view, name='tehnician-attendance'),

    path('agent-dashboard', views.agent_dashboard_view, name='agent-dashboard'),
    path('agent-request', views.agent_request_view, name='agent-request'),
    path('agent-add-request', views.agent_add_request_view, name='agent-add-request'),

    path('agent-profile', views.agent_profile_view, name='agent-profile'),
    path('edit-agent-profile', views.edit_agent_profile_view, name='edit-agent-profile'),
    path('agent-feedback', views.agent_feedback_view, name='agent-feedback'),
    path('agent-deviz', views.agent_deviz_view, name='agent-deviz'),
    path('agent-view-request', views.agent_view_request_view, name='agent-view-request'),
    path('agent-delete-request/<int:pk>', views.agent_delete_request_view, name='agent-delete-request'),
    path('agent-view-approved-request', views.agent_view_approved_request_view,
         name='agent-view-approved-request'),
    path('agent-view-approved-request-deviz', views.agent_view_approved_request_deviz_view,
         name='agent-view-approved-request-deviz'),

    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='tickets/index.html'), name='logout'),

    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),

]
