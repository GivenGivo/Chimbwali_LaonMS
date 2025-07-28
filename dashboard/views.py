from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from users.models import User

@login_required
def ceo_dashboard(request):
    if request.user.role != 'CEO':
        return render(request, '403.html')  # optionally create this
    return render(request, 'dashboard/ceo_dashboard.html')

@login_required
def officer_dashboard(request):
    if request.user.role != 'OFFICER':
        return render(request, '403.html')  # optionally create this
    return render(request, 'dashboard/officer_dashboard.html')
