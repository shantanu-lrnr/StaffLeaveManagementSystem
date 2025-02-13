from django.shortcuts import render,redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import UpdateProfileForm,AddStaffForm,UpdateStaffForm
from myapp.models import User,Staff,StaffLeave
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from superadmin.utils import send_activation_email

# Create your views here.

@login_required
def admin_dashboard(request):
    if request.user.is_superuser:
        total_staff = User.objects.all().count()-1
        total_leaves = StaffLeave.objects.all().count()
        rejected_leaves = StaffLeave.objects.filter(status="Rejected")
        approved_leaves = StaffLeave.objects.filter(status="Approved")
        pending_leaves = StaffLeave.objects.filter(status="Pending")
        return render(request,'superadmin/admin_dashboard.html',{"total_staff":total_staff,"total_leaves":total_leaves,"rejected_leaves":rejected_leaves,"approved_leaves":approved_leaves,"pending_leaves":pending_leaves})
    else:
        return redirect("staff_dashboard")

@login_required
def update_profile(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = UpdateProfileForm(request.POST, request.FILES, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request,"Profile updated successfully..")
                redirect("update_profile")

        else:
            form = UpdateProfileForm(instance=request.user)
        return render(request,'superadmin/update_profile.html',{"form":form})
    else:
        return redirect("staff_dashboard")

@login_required
def add_staff(request):
    if request.user.is_superuser:
        if request.method == 'POST':
            form = AddStaffForm(request.POST,request.FILES)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                user = form.save(commit=False)
                user.set_password(cleaned_data.get("password"))
                user = form.save()
                
                gender = cleaned_data.get("gender")
                address = cleaned_data.get("address")
                Staff(user=user,gender=gender,address=address).save()

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                activation_link = reverse(
                    'activate', kwargs={'uidb64': uidb64, 'token': token})
                activation_url = f'{settings.SITE_DOMAIN}{activation_link}'
                send_activation_email(user.email, activation_url)
                messages.success(
                    request,
                    'Staff Added successful! Please tell your staff member to activate the account.',
                )
              
                return redirect("add_staff")

        else:
            form = AddStaffForm()
        return render(request,'superadmin/add_staff.html',{"form":form})
    else:
        return redirect("staff_dashboard")
    
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

        if user.is_active:
            messages.warning(
                request, "This account has already been activated.")
            return redirect('login')

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request, "Your account has been activated successfully!"
            )
            return redirect('login')
        else:
            messages.error(
                request, "The activation link is invalid or has expired."
            )
            return redirect('login')
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request, "Invalid activation link.")
        return redirect('login')

@login_required
def manage_staff(request):
    if request.user.is_superuser:
        staff_list = User.objects.filter(is_superuser=False)
        return render(request,"superadmin/manage_staff.html",{"staff_list":staff_list})
    else:
        return redirect("staff_dashboard")

@login_required
def update_staff(request,pk):
    if request.user.is_superuser:
        user = User.objects.get(pk=pk)
        staff = Staff.objects.get(user=user)
        if request.method == 'POST':
            form = UpdateStaffForm(request.POST,request.FILES,instance=user)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                if cleaned_data.get("password"):
                    user = form.save(commit=False)
                    user.set_password(cleaned_data.get("password"))
                user = form.save()

                gender = cleaned_data.get("gender")
                address = cleaned_data.get("address")
                staff.address = address
                staff.gender = gender
                staff.save()
                
                messages.success(request,"Staff Updated Successfully!")
                return redirect("update_staff",pk=pk)
        else:
            form = UpdateStaffForm(instance=user)
        return render(request,'superadmin/update_staff.html',{"form":form,"staff":staff})
    else:
        return redirect("staff_dashboard")

@login_required
def confirm_delete(request,pk):
    if request.user.is_superuser:
        return render(request,'superadmin/confirm_delete.html',{"pk":pk})
    else:
        return redirect("staff_dashboard")

@login_required
def delete_staff(request,pk):
    if request.user.is_superuser:
        if request.method=='POST':
            staff = User.objects.get(pk=pk)
            staff.delete()
            return redirect('manage_staff')
    else:
        return redirect("staff_dashboard")

@login_required 
def staff_leave(request):
    if request.user.is_superuser:
        all_leaves = StaffLeave.objects.all()
        return render(request,'superadmin/staff_leave.html',{"all_leaves":all_leaves})
    else:
        return redirect("staff_dashboard")
    
@login_required
def approve_leave(request,pk):
    if request.user.is_superuser:
        staff_leave = StaffLeave.objects.get(pk=pk)
        staff_leave.status = "Approved"
        staff_leave.save()
        messages.success(request,"Leave Approved successfully..")
        return redirect("staff_leave")
    else:
        return redirect("staff_dashboard")
    
@login_required
def reject_leave(request,pk):
    if request.user.is_superuser:
        staff_leave = StaffLeave.objects.get(pk=pk)
        staff_leave.status = "Rejected"
        staff_leave.save()
        messages.success(request,"Leave Rejected successfully..")
        return redirect("staff_leave")
    else:
        return redirect("staff_dashboard")

@login_required
def change_password(request):
    if request.user.is_superuser:
        if request.method == "POST":
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                logout(request)
                messages.success(
                    request, "Password changed successfully. Please log in with your new password."
                )
                return redirect('login')
            # else:
            #     # Handle form errors and display them to the user
            #     for field, errors in form.errors.items():
            #         for error in errors:
            #             messages.error(request, error)
        else:
            form = PasswordChangeForm(user=request.user)
        return render(request, 'superadmin/password_change.html', {'form': form})
    else:
        return redirect("staff_dashboard")