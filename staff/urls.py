from django.urls import path
from staff import views

urlpatterns = [
    path('staff_dashboard/',views.staff_dashboard,name="staff_dashboard"),
    path('apply_leave/',views.apply_leave,name="apply_leave"),
    path('leave_details/',views.leave_details,name="leave_details"),
]
