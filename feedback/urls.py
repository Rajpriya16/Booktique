from django.urls import path
from .views import feedback_user_view, feedback_superuser_view,delete_feedback

urlpatterns = [
    path('feedback/', feedback_user_view, name='feedback_user'),
    path('feedbacks/', feedback_superuser_view, name='feedback_superuser'),
    path('delete-feedback/<int:feedback_id>/', delete_feedback, name='delete_feedback'),
]
