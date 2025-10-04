from django.db import models


from django.contrib.auth.models import User



class Course(models.Model):
	name = models.CharField(max_length=100)
	code = models.CharField(max_length=50, blank=True)
	is_active = models.BooleanField(default=True)
	description = models.TextField(blank=True)
	duration = models.CharField(max_length=100, blank=True)
	cover_image = models.ImageField(upload_to='course_covers/', blank=True, null=True)
	trainer = models.ForeignKey('Trainer', on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
	syllabus = models.FileField(upload_to='syllabus/', blank=True, null=True)
	learning_outcomes = models.CharField(max_length=255, blank=True)
	mode = models.CharField(max_length=10, choices=[('offline', 'Offline'), ('online', 'Online')], default='offline')
	category = models.CharField(max_length=20, choices=[('developer', 'Developer'), ('designer', 'Designer'), ('tester', 'Tester')], default='developer')

	def __str__(self):
		return self.name

class Trainee(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='trainees')
	phone = models.CharField(max_length=20, blank=True)
	batch = models.CharField(max_length=50, blank=True)
	progress = models.PositiveIntegerField(default=0)
	status = models.CharField(max_length=20, default='Active')
	profile_image = models.ImageField(upload_to='trainee_images/', blank=True, null=True)
	trainer = models.ForeignKey('Trainer', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_trainees')
	trainee_code = models.CharField(max_length=50, blank=True)
	certificate_status = models.CharField(max_length=20, default='Issued')
	daily_task = models.PositiveIntegerField(default=1)  # Number of tasks per day
	total_task = models.PositiveIntegerField(default=0)  # Total tasks for the course (editable)
	completed_task = models.PositiveIntegerField(default=0)  # Completed tasks entered by trainer
	pending_completed = models.PositiveIntegerField(default=0)  # Pending tasks completed entered by trainer
	remarks = models.TextField(blank=True)  # Remarks/notes about the trainee's daily tasks

	def __str__(self):
		return self.user.get_full_name() or self.user.username


# New model for trainee attendance
class TraineeAttendance(models.Model):
	trainee = models.ForeignKey('Trainee', on_delete=models.CASCADE, related_name='attendances')
	date = models.DateField()
	status = models.CharField(max_length=15, choices=[('present', 'Present'), ('absent', 'Absent'), ('informed', 'Informed'), ('not_informed', 'Not Informed')])
	# Optionally, you can add a field for remarks or class topic
	remarks = models.CharField(max_length=255, blank=True)

	class Meta:
		unique_together = ('trainee', 'date')

	def __str__(self):
		return f"{self.trainee} - {self.date} ({self.status})"

class Certificate(models.Model):
	trainee = models.ForeignKey('Trainee', on_delete=models.CASCADE)
	course = models.ForeignKey('Course', on_delete=models.CASCADE)
	issued_date = models.DateField(auto_now_add=True)
	certificate_number = models.CharField(max_length=100, unique=True, blank=True)
	completion_percentage = models.PositiveIntegerField(default=0)
	grade = models.CharField(max_length=2, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')], default='A')
	is_verified = models.BooleanField(default=True)

	def save(self, *args, **kwargs):
		if not self.certificate_number:
			# Generate unique certificate number
			self.certificate_number = f"CERT-{self.trainee.id}-{self.course.id}-{self.issued_date.strftime('%Y%m%d')}"
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.trainee} - {self.course} ({self.issued_date})"



class Trainer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	phone = models.CharField(max_length=20, blank=True)
	expertise = models.CharField(max_length=255, blank=True)
	assign_courses = models.CharField(max_length=255, blank=True)
	bio = models.TextField(blank=True)
	trainer_code = models.CharField(max_length=50, blank=True)
	batches = models.PositiveIntegerField(default=0)
	status = models.CharField(max_length=20, default='Active')
	profile_image = models.ImageField(upload_to='trainer_images/', blank=True, null=True)
	admin_locked = models.BooleanField(default=False)  # True if admin sets as Inactive

	def __str__(self):
		return self.user.get_full_name() or self.user.username


# Announcement model for dynamic announcements
class Announcement(models.Model):
    TARGET_CHOICES = [
        ('all', 'All'),
        ('trainers', 'Trainers'),
        ('trainees', 'Trainees'),
    ]
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    date_posted = models.DateField(null=True, blank=True)
    posted_by = models.CharField(max_length=100, default='Admin')
    academy = models.CharField(max_length=100, default='Vetri Academy')
    target_audience = models.CharField(max_length=20, choices=TARGET_CHOICES, default='all')

    def __str__(self):
        return self.title

class DailyAssessment(models.Model):
    trainee = models.ForeignKey('Trainee', on_delete=models.CASCADE, related_name='assessments')
    trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE, related_name='assessments')
    date = models.DateField(auto_now_add=True)
    score = models.PositiveIntegerField(default=0)
    max_score = models.PositiveIntegerField(default=100)
    remarks = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)

class SessionRecording(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    session_url = models.URLField(help_text="URL to the session recording (YouTube, Google Drive, etc.)")
    batch = models.CharField(max_length=50, help_text="Batch for which this session is recorded")
    trainer = models.ForeignKey('Trainer', on_delete=models.CASCADE, related_name='session_recordings')
    upload_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_visible = models.BooleanField(default=True, help_text="Whether this session is visible to trainees")
    upload_status = models.CharField(max_length=20, choices=[
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('pending', 'Pending')
    ], default='pending')

    def __str__(self):
        return f"{self.title} - Batch {self.batch} ({self.upload_date.strftime('%Y-%m-%d')})"
