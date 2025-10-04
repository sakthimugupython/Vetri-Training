from django.contrib import admin


from .models import Trainee, Trainer, Course, Certificate
admin.site.register(Trainee)
admin.site.register(Trainer)
admin.site.register(Course)
admin.site.register(Certificate)
