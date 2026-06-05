from django.urls import path
from .views import (
    revision_plan_create,
    availability_list_create,
    revision_session_list_create,
    generate_ai_revision_plan,
)

urlpatterns = [
    path("", revision_plan_create),
    path("availabilities/", availability_list_create),
    path("sessions/", revision_session_list_create),
    path("generate-ai/", generate_ai_revision_plan, name="generate_ai_revision_plan"),
]