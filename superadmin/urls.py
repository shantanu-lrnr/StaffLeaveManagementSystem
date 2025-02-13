from django.urls import path
from superadmin import views

urlpatterns = [
    path('admin_dashboard/',views.admin_dashboard,name="admin_dashboard"),
    path('password_change/',views.change_password,name="password_change"),
    path('update_profile/',views.update_profile,name="update_profile"),
    path('add_staff/',views.add_staff,name="add_staff"),
    path('activate/<str:uidb64>/<str:token>/',
         views.activate_account, name='activate'),
    path('manage_staff/',views.manage_staff,name="manage_staff"),
    path('update_staff/<int:pk>/',views.update_staff,name="update_staff"),
    path('confirm_delete/<int:pk>/',views.confirm_delete,name="confirm_delete"),
    path('delete_staff/<int:pk>/',views.delete_staff,name="delete_staff"),
    path('staff_leave/',views.staff_leave,name="staff_leave"),
    path('approve_leave/<int:pk>/',views.approve_leave,name="approve_leave"),
    path('reject_leave/<int:pk>/',views.reject_leave,name="reject_leave"),

]
