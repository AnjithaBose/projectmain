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
    path('user/password/update/', PasswordChangeView.as_view(),name='password_change'),


    #password reset paths
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='common/forgot_password.html'),name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='common/password_reset_sent.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='common/set_new_password.html'),name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='common/password_reset_complete.html'),name='password_reset_complete'),


    path('administrator/home/',AdminDashboard.as_view(),name='admin_dashboard'),
    path('administrator/courses/',ViewCourses.as_view(),name='view_courses'),
    path('administrator/course/edit/<id>/',EditCourse.as_view(),name='edit_course'),
    path('administrator/course/delete/<id>/',DeleteCourse.as_view(),name='delete_course'),
    path('administrator/mails/',ViewMails.as_view(),name='view_mails'),
    path('administrator/mail/send/',SendMail.as_view(),name='send_mail'),
    path('administrator/mail/<id>/',ViewMail.as_view(),name='view_mail'),
    path('administrator/draft/send/<id>/',SendDraft.as_view(),name='send_draft'),
    path('administrator/draft/delete/<id>/',DeleteDraft.as_view(),name='delete_draft'),
    path('administrator/staff/add/',CreateStaff.as_view(),name='add_staff'),
    path('administrator/staff/edit/<id>/',EditStaff.as_view(),name='edit_staff'),
    path('administrator/staff/pending/',PendingStaff.as_view(),name='pending_staff'),
    path('administrator/staff/approval/view/<id>/',ViewPendingStaff.as_view(),name='view_pending_staff'),
    path('administrator/staff/approval/<id>/',ApproveStaff.as_view(),name='approve_staff'),
    path('administrator/mail/lead/<id>/',SendLeadMail.as_view(),name='send_lead_mail'),
    path('administrator/webinar/add/',AddWebinar.as_view(),name='add_webinar'),
    path('administrator/taskmanager/',TaskManager.as_view(),name='task_manager'),
    path('administrator/login/log/',GetLoginLog.as_view(),name='login_log'),

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
    path('operations/remove/subject/<id>/',DeleteStudentSubject.as_view(),name='remove_subject'),
    

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
    path('sales/remove/batch/<id>/',RemoveSCD.as_view(),name='remove_scd'),
    path('sales/reassign/lead/<id>/',ReassignLead.as_view(),name='reassign_lead'),


    path('trainer/home/',TrainerDashboard.as_view(),name='trainer_dashboard'),
    path('trainer/admin/home/',TrainerManagerDashboard.as_view(),name='trainer_manager_dashboard'),
    path('trainer/batches/',MyBatches.as_view(),name='my_batches'),
    path('trainer/students/',MyStudents.as_view(),name='my_students'),
    path('trainer/batch/current/',MyCurrentBatch.as_view(),name='my_current_batch'),
    path('trainer/upload/videos/<id>/',UploadVideos.as_view(),name='upload_videos'),
    path('trainer/update/videos/<id>/',UpdateVideo.as_view(),name='update_video'),
    path('trainer/assignments/',UploadAssignment.as_view(),name='upload_assignments'),
    path('trainer/projects/',UploadProject.as_view(),name='upload_projects'),
    path('trainer/projects/submissions/<id>/',Projects.as_view(),name='projects'),
    path('trainer/assignments/submissions/<id>/',Assignments.as_view(),name='assignments'),
    path('trainer/assignments/approve/<id>/',ApproveAssignment.as_view(),name='approve_assignment'),
    path('trainer/assignments/reject/<id>/',RejectAssignment.as_view(),name='reject_assignment'),
    path('trainer/projects/approve/<id>/',ApproveProject.as_view(),name='approve_project'),
    path('trainer/projects/reject/<id>/',RejectProject.as_view(),name='reject_project'),
    path('trainer/assignments/remove/<id>/',RemoveAssignment.as_view(),name='remove_assignment'),
    path('trainer/projects/remove/<id>/',RemoveProject.as_view(),name='remove_project'),
    path('trainer/projects/activate/<id>/',ActivateProject.as_view(),name='activate_project'),
    path('trainer/queries/',ViewQueries.as_view(),name='view_queries'),
    path('trainer/queries/read/<id>/',ReplyQuery.as_view(),name='reply_query'),
    path('trainer/delete/notes/<id>/',DeleteStudyMaterial.as_view(),name='delete_study_material'),


    path('staff/contacts/',ViewStaff.as_view(),name='view_contacts'),
    path('staff/students/',Students.as_view(),name='view_students'),
    path('staff/message/<id>/',Message.as_view(),name='message'),
    path('staff/message/<id>/<cid>/',GetMessage.as_view(),name='get_message'),
    path('staff/jobs/',Jobs.as_view(),name='jobs'),
    path('staff/jobs/add/',AddJob.as_view(),name='add_job'),
    path('staff/view/teqnews/',ViewTeqNews.as_view(),name='view_teqnews'),
    path('staff/view/profile/',ViewProfile.as_view(),name='view_profile'),
    path('staff/edit/profile/',EditProfile.as_view(),name='edit_profile'),
    path('staff/view/task/<id>/',ViewTask.as_view(),name='view_task'),
    path('staff/update/task/<id>/',UpdateTask.as_view(),name='update_task'),
    path('staff/view/tasks/',MyTask.as_view(),name='my_task'),
    path('staff/remove/task/<id>/',DeleteTask.as_view(),name='delete_task'),
    path('staff/assign/assignee/<id>/',AssignAssignee.as_view(),name='assignee'),
    path('staff/complaints/',AllComplaints.as_view(),name='all_complaints'),

    path('student/home/',StudentDashboard.as_view(),name='student_dashboard'),
    path('student/classrooms/',MyClassroom.as_view(),name='my_classroom'),
    path('student/recordings/',MyRecordings.as_view(),name='my_recordings'),
    path('student/recordings/<id>/',ClassRecordings.as_view(),name='class_recordings'),
    path('student/assignments/',ViewAssignments.as_view(),name='view_assignments'),
    path('student/projects/',ViewProjects.as_view(),name='view_projects'),
    path('student/submit/assignment/<id>/',SubmitAssignment.as_view(),name='submit_assignment'),
    path('student/assignment/submissions/',AssignemtSubmissions.as_view(),name='assignment_submissions'),
    path('student/submit/project/<id>/',SubmitProject.as_view(),name='submit_project'),
    path('student/project/submissions/',ProjectSubmissions.as_view(),name='project_submissions'),
    path('student/certificates/',MyCertificates.as_view(),name='my_certificates'),
    path('student/queries/<id>/',AskQuery.as_view(),name='ask_queries'),
    path('student/trainers/',MyTrainers.as_view(),name='my_trainers'),
    path('student/profile/',MyProfile.as_view(),name='my_profile'),
    path('student/complaints/',ViewMyComplaints.as_view(),name='my_complaints'),
    path('student/receipts/',MyReceipts.as_view(),name='my_receipts'),

    path('user/notes/',UserNotes.as_view(),name='user_notes'),
    path('user/delete/notes/<id>/',DeleteNote.as_view(),name='delete_notes'),
    path('user/status/notes/<id>/',PublicNote.as_view(),name='public_notes'),
    path('user/edit/notes/<id>/',EditNotes.as_view(),name='edit_notes'),
    path('user/poke/<id>/',Poke.as_view(),name='poke'),
    path('user/chat/notify/<id>/',SendChatNotification.as_view(),name='chat_notification'),
    path('user/video/<id>/',PlayVideo.as_view(),name='video_player'),
    path('user/notification/read/',MarkasRead.as_view(),name='mark_as_read'),
    path('user/notifications/',AllNotifications.as_view(),name='notifications'),
    path('user/complaint/<id>/',ViewComplaint.as_view(),name='complaint'),
    path('user/complaint/comment/<id>/',PostComplaintComment.as_view(),name='comment_complaint'),
    path('user/complaint/comment/update/<id>/',UpdateComplaintComment.as_view(),name='update_comment'),
    path('user/complaint/comment/delete/<id>/',DeleteComplaintComment.as_view(),name='delete_comment'),
    path('user/batch/materials/',UploadNotes.as_view(),name='upload_notes'),


    path('webinar/',ActiveWebinar.as_view(),name='active_webinar'),
    path('webinar/<id>/',WebinarRegister.as_view(),name='join'),
    path('notes/<id>/',ViewNotes.as_view(),name='view_notes'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = 'accounts.views.handler404'
handler500 = 'accounts.views.handler500'
