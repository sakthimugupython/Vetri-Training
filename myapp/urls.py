from django.urls import path


from . import views

urlpatterns = [
    path('announcements/', views.announcements, name='announcements'),
    path('announcements/add/', views.add_announcement, name='add_announcement'),
    path('announcements/<int:announcement_id>/delete/', views.delete_announcement, name='delete_announcement'),
    path('announcements/<int:announcement_id>/edit/', views.edit_announcement, name='edit_announcement'),
    path('', views.login_options, name='login_options'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('student-login/', views.student_login, name='student_login'),
    path('student-logout/', views.student_logout, name='student_logout'),
    path('trainee-dashboard/', views.trainee_dashboard, name='trainee_dashboard'),
    path('my-courses/', views.my_courses, name='my_courses'),
    path('trainer-login/', views.trainer_login, name='trainer_login'),
    path('trainer-dashboard/', views.trainer_dashboard, name='trainer_dashboard'),
    path('courses/', views.course_list, name='course_list'),
    path('trainees/', views.trainee_list, name='trainee_list'),
    path('trainees/add/', views.add_trainee, name='add_trainee'),
    path('trainees/<int:trainee_id>/edit/', views.edit_trainee, name='edit_trainee'),
    path('courses/add/', views.add_course, name='add_course'),
    path('courses/<int:course_id>/edit/', views.edit_course, name='edit_course'),
    path('courses/<int:course_id>/delete/', views.delete_course, name='delete_course'),
    path('trainers/', views.trainer_list, name='trainer_list'),
    path('trainers/add/', views.add_trainer, name='add_trainer'),
    path('trainers/<int:trainer_id>/edit/', views.edit_trainer, name='edit_trainer'),
    path('trainers/<int:trainer_id>/delete/', views.delete_trainer, name='delete_trainer'),
    path('trainer-logout/', views.trainer_logout, name='trainer_logout'),
    path('update-assessment/<int:trainee_id>/', views.update_assessment, name='update_assessment'),
    path('trainer-trainee-list/', views.trainee_list_trainer, name='trainer_trainee_list'),

    # Attendance URLs
    path('trainee-attendance/', views.trainee_attendance_list, name='trainee_attendance_list'),
    path('trainer-trainee-attendance/', views.trainee_attendance_trainer, name='trainer_trainee_attendance'),
    path('trainee-attendance-detail/<int:trainee_id>/', views.trainee_attendance_detail, name='trainee_attendance_detail'),

    # Session URLs
    path('upload-session/', views.upload_session, name='upload_session'),
    path('sessions/', views.session_list, name='session_list'),
    path('sessions/<int:session_id>/', views.session_detail, name='session_detail'),
    path('sessions/<int:session_id>/delete/', views.delete_session, name='delete_session'),
    path('sessions/<int:session_id>/toggle-visibility/', views.toggle_session_visibility, name='toggle_session_visibility'),

    # Trainer Announcement URLs
    path('trainer-announcements/', views.trainer_announcements, name='trainer_announcements'),
    path('trainer-announcements/create/', views.create_announcement, name='create_announcement'),

    # Trainee Announcement URLs
    path('trainee-announcements/', views.trainee_announcements, name='trainee_announcements'),

    # Certificate URLs
    path('certificates/', views.student_certificates, name='student_certificates'),
    path('admin-certificates/', views.admin_certificates, name='admin_certificates'),
    path('certificates/<int:certificate_id>/download/', views.download_certificate, name='download_certificate'),
]
