"""crm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from django.conf.urls import url,include
from django.conf.urls.static import static
from django.conf import settings
from accounts.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(),name='login'),
    path('logout/', LogoutView.as_view(),name='logout'),
    path('', Home.as_view(),name='home'),


    path('administrator/home/',AdminDashboard.as_view(),name='admin_dashboard'),
    path('administrator/courses/',ViewCourses.as_view(),name='view_courses'),
    path('administrator/course/edit/<id>/',EditCourse.as_view(),name='edit_course'),
    path('administrator/course/delete/<id>/',DeleteCourse.as_view(),name='delete_course'),
    path('administrator/mails/',ViewMails.as_view(),name='view_mails'),
    path('administrator/mail/send/',SendMail.as_view(),name='send_mail'),
    path('administrator/mail/<id>/',ViewMail.as_view(),name='view_mail'),
    path('administrator/draft/send/<id>/',SendDraft.as_view(),name='send_draft'),
    path('administrator/staff/add/',CreateStaff.as_view(),name='add_staff'),
    path('administrator/staff/edit/<id>/',EditStaff.as_view(),name='edit_staff'),

    path('operations/home/',OperationsDashboard.as_view(),name='operations_dashboard'),
    path('operations/batches/',ViewBatches.as_view(),name='view_batches'),
    path('operations/batch/view/<id>/',ViewBatch.as_view(),name='view_batch'),
    path('operations/batch/notification/<id>/',SendMailNotification.as_view(),name='send_mail_notification'),
    path('operations/mail/send/<id>',SendSingleMail.as_view(),name='send_single_mail'),
    path('operations/student/share/<id>/',UpdateShare.as_view(),name='update_share'),
    path('operations/batch/edit/<id>/',EditBatch.as_view(),name='edit_batch'),
    path('operations/scd/add/<id>/',AddSCD.as_view(),name='add_scd'),
    path('operations/scd/delete/<id>/',DeleteSCD.as_view(),name='delete_scd'),
    path('operations/view/student/<id>/',ViewStudent.as_view(),name='view_student'),
    path('operations/view/batch/approvals/',ViewBatchEditApprovals.as_view(),name='batch_edit_approvals'),
    path('operations/batch/approve/<id>/',ApproveBatch.as_view(),name='approve_batch'),
    path('operations/batch/reject/<id>/',RejectBatch.as_view(),name='reject_batch'),

    path('sales/home/',SalesDashboard.as_view(),name='sales_dashboard'),
    path('sales/leads/',Leads.as_view(),name='view_leads'),
    path('sales/closure/',ViewClosure.as_view(),name='view_closure'),
    path('sales/history/',ViewHistory.as_view(),name='view_history'),
    path('sales/update/lead/<id>/',UpdateLead.as_view(),name='update_lead'),
    path('sales/convert/lead/<id>/',CreateStudentAccount.as_view(),name='convert_lead'),
    path('sales/reverse/lead/<id>/',DeleteLMSProfile.as_view(),name='revert_lead'),
    path('sales/student/payments/<id>/',GetStudentPaymentDetails.as_view(),name='get_student_payments'),
    path('sales/leads/pending/activation/',ListLMSApprovals.as_view(),name='list_lms_approvals'),
    path('sales/leads/approve/activation/<id>/',ApproveLMSProfile.as_view(),name='approve_lms_activate'),
    path('sales/leads/pending/deactivation/',ListLMSDeletion.as_view(),name='list_lms_revert'),
    path('sales/leads/approve/deactivation/<id>/',ApproveDelLMSProfile.as_view(),name='approve_lms_revert'),
    path('sales/leads/reject/deactivation/<id>/',RejectDelLMSProfile.as_view(),name='reject_lms_revert'),


    path('trainer/home/',TrainerDashboard.as_view(),name='trainer_dashboard'),
    path('trainer/admin/home/',TrainerManagerDashboard.as_view(),name='trainer_manager_dashboard'),
    path('trainer/batches/',MyBatches.as_view(),name='my_batches'),
    path('trainer/students/',MyStudents.as_view(),name='my_students'),



    path('staff/contacts/',ViewStaff.as_view(),name='view_contacts'),
    path('staff/students/',Students.as_view(),name='view_students'),
    path('staff/message/<id>/',Message.as_view(),name='message'),
    path('staff/message/<id>/<cid>/',GetMessage.as_view(),name='get_message'),
    path('staff/jobs/',Jobs.as_view(),name='jobs'),
    path('staff/jobs/add/',AddJob.as_view(),name='add_job'),
    path('staff/view/teqnews/',ViewTeqNews.as_view(),name='view_teqnews'),
    path('staff/view/profile/',ViewProfile.as_view(),name='view_profile'),
    path('staff/edit/profile/',EditProfile.as_view(),name='edit_profile'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
