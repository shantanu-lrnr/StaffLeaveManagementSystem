from django.shortcuts import render,redirect
from .forms import ApplyLeaveForm
from django.contrib import messages
from myapp.models import StaffLeave
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def staff_dashboard(request):
    if not request.user.is_superuser:
        all_leaves = StaffLeave.objects.filter(staff=request.user.staff)
        rejected_leaves = all_leaves.filter(status="Rejected")
        approved_leaves = all_leaves.filter(status="Approved")
        pending_leaves = all_leaves.filter(status="Pending")
        return render(request,'staff/staff_dashboard.html',{"all_leaves":all_leaves,"rejected_leaves":rejected_leaves,"approved_leaves":approved_leaves,"pending_leaves":pending_leaves})
    else:
        return redirect("admin_dashboard")
    
    
@login_required
def apply_leave(request):
    if not request.user.is_superuser:
        if request.method=='POST':
            form = ApplyLeaveForm(request.POST)
            if form.is_valid():
                staff_leave = form.save(commit=False)
                staff_leave.staff = request.user.staff
                staff_leave.save()
                messages.success(request,"Leave applied successfully..")
                return redirect("staff_dashboard")
        else:
            form = ApplyLeaveForm()
        return render(request,'staff/apply_leave.html',{"form":form})
    else:
        return redirect("admin_dashboard")

@login_required
def leave_details(request):
    if not request.user.is_superuser:
        all_leaves = StaffLeave.objects.filter(staff=request.user.staff)
        return render(request,'staff/leave_details.html',{"all_leaves":all_leaves})
    else:
        return redirect("admin_dashboard")