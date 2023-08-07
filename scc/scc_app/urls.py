from django.urls import path
from . import views
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginpage, name='loginpage'),
    path('signup/', views.signuppage, name='signuppage'),
    path('login/signup/', views.signuppage, name='signuppage'),
    
    path('login/home/', views.homepage, name='homepage'),
    path('login/forgotpassword', views.forgotpasswordpage, name='forgotpasswordpage'),
    path('login/forgotpassword/verifyemail', views.verifyemail, name='verifyemail'),
    path('login/forgotpassword/verifyemail/newpassword', views.newpasswordpage, name='newpasswordpage'),
    path('login/forgotpassword/verifyemail/newpassword/change', views.newpasswordchangepage, name='newpasswordchangepage'),
    path('home/contactus/', views.contactuspage, name='contactuspage'),
    path('contactus/', views.contactuspage, name='contactuspage'),
    path('login/home/complaintregistration/', views.complaintregistrationpage, name='complaintregistrationpage'),
    path('login/home/complaintregistration/add_details', views.addcomplaintdetails, name='addcomplaintdetails'),
    path('login/home/profile', views.profilepage, name='profilepage'),
    
    path('signup/user_registration', views.user_registrationpage, name='user_registrationpage'),
    path('login/login', views.login_check_page, name='login_check_page'),
    path('login/home/contactus/', views.contactuspage, name='contactuspage'),
    path('login/home/logout/', views.logoutpage, name='logoutpage'),
    path('login/home/contactus/addDetails', views.addcontactdetailspage, name='addcontactdetailspage'),
    path('login/home/profile/delete/<str:unique_id>', views.deletecomplaintpage, name='deletecomplaintpage'),
    
    # admin urls
    path('login/admin/', views.adminpage, name='adminpage'),
    path('login/admin/pendingcomplaints', views.pendingcomplaints, name='pendingcomplaints'),
    path('login/admin/completedcomplaints', views.completedcomplaints, name='completedcomplaints'),
    path('login/admin/contactus', views.contactus, name='contactus'),
    path('login/admin/logout', views.logout, name='logout'),
    path('login/admin/pendingcomplaints/update/<str:unique_id>', views.updatependingcomplaintspage, name='updatependingcomplaintspage'),
     
     url(r'^uploads/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
    

]