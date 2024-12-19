from django.shortcuts import render, redirect,get_object_or_404
from .models import Feedback
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def feedback_superuser_view(request):
    feedbacks = Feedback.objects.all().order_by('-timestamp')
    return render(request, 'feedback_superuser.html', {'feedbacks': feedbacks})


@login_required(login_url='login')
def feedback_user_view(request):
    if request.method == 'POST':
        feedback_content = request.POST.get('feedback')
        Feedback.objects.create(user=request.user, content=feedback_content)
        return redirect('home')

    return render(request, 'feedback_user.html')

@login_required
def delete_feedback(request, feedback_id):
    feedback = get_object_or_404(Feedback, id=feedback_id)
    if request.user.is_superuser:  # Only superusers can delete feedback
        feedback.delete()
    return redirect('feedback_superuser')
