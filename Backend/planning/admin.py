from django.contrib import admin
from .models import Availability, RevisionPlan, RevisionSession

# Register your models here.
admin.site.register(Availability)
admin.site.register(RevisionPlan)
admin.site.register(RevisionSession)