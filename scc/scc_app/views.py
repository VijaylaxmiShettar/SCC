from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.template import loader
from .models import Complaint_registration, User, Contact
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.contrib.sessions.backends.db import SessionStore
import uuid
# from . import forms
# Create your views here.
def index(request):
    allcounts = Complaint_registration.objects.count()
    solvedcounts = Complaint_registration.objects.filter(complaint_status='completed').count()
    unsolvedcounts = Complaint_registration.objects.filter(complaint_status='pending').count()
    return render(request, 'index.html', {'allcounts': allcounts,'solvedcounts':solvedcounts,'unsolvedcounts':unsolvedcounts})

def homepage(request):
  if request.session.has_key('email'):
     if request.session.has_key('password'):
         allcounts = Complaint_registration.objects.count()
         solvedcounts = Complaint_registration.objects.filter(complaint_status='completed').count()
         unsolvedcounts = Complaint_registration.objects.filter(complaint_status='pending').count()
         return render(request, 'home.html', {'allcounts': allcounts,'solvedcounts':solvedcounts,'unsolvedcounts':unsolvedcounts})
  else:
      return redirect('/login')

def contactuspage(request):
  template = loader.get_template('contactus.html')
  return HttpResponse(template.render())

def complaintregistrationpage(request):
  template = loader.get_template('complaintregistration.html')
  return HttpResponse(template.render())

def forgotpasswordpage(request):
  template = loader.get_template('forgotpassword.html')
  return HttpResponse(template.render())

def loginpage(request):
  template = loader.get_template('login.html')
  return HttpResponse(template.render())

def signuppage(request):
  template = loader.get_template('signup.html')
  return HttpResponse(template.render())

@csrf_exempt
def verifyemail(request):
 error_message = None
 if request.method == 'POST':
  email = request.POST['email']
  unique_id = request.POST['unique_id']
  try:
    user = User.objects.get(email_id=email, unique_id=unique_id)
    return render(request, 'newpassword.html', {'email_id': email})
  except User.DoesNotExist:
    error_message = 'Unique ID and Email does not match.'
    return render(request, 'forgotpassword.html', {'error_message': error_message})
  else:
     return render(request, 'forgotpassword.html')

@csrf_exempt
def newpasswordpage(request):
   template = loader.get_template('newpassword.html')
   return HttpResponse(template.render())

@csrf_exempt
def newpasswordchangepage(request):
 error_message = None
 if request.method == 'POST':
  new_password = request.POST['new_password']
  confirm_password = request.POST['confirm_password']
  email = request.POST['email']
  try:
    user = User.objects.get(email_id=email)
    user.password = new_password
    user.save()
    return redirect('/login')
  except User.DoesNotExist:
    error_message = 'Unique ID and Email does not match.'
    return render(request, 'forgotpassword.html', {'error_message': error_message})
  else:
     return render(request, 'forgotpassword.html')

@csrf_exempt
def user_registrationpage(request):
    if request.method == 'POST':
        name = request.POST['full_name']
        unique_id = request.POST['unique_name']
        emailid = request.POST['your_email']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        pincode = request.POST['pincode']
        password = request.POST['password']
        usertype = "user"
        result = User(name=name,unique_id=unique_id, email_id=emailid,phonenumber=phonenumber,address=address,pincode=pincode, password=password, user_type=usertype)
        result.save()
        return redirect('index')  # redirect to index.html
    else:
        return render(request, 'signup.html')
     
@csrf_exempt
def login_check_page(request):
   error_message = None
   if request.method == 'POST':
        email = request.POST['username']
        password = request.POST['password']
        try:
          user = User.objects.get(email_id=email, password=password)
          if user.user_type == "user":
             session = SessionStore()
             request.session['email'] = email
             request.session['password'] = password
             session.save()
             return redirect('home/')
          else:
             session = SessionStore()
             request.session['email'] = email
             request.session['password'] = password
             session.save()
             return redirect('admin/')
        except User.DoesNotExist:
          error_message = 'Login failed. Please check your email and password.'
          return render(request, 'login.html', {'error_message': error_message})
        else:
           return render(request, 'login.html')
        
def adminpage(request):
  if request.session.has_key('email'):
    if request.session.has_key('password'):
      complaints = Complaint_registration.objects.all().values()
      mycomplaints = []
      for complaint in complaints:
        mycomplaints.append({'fname': complaint['fname'], 'lname': complaint['lname'], 'phonenumber': complaint['phonenumber'], 'email': complaint['email'], 'complaint_type': complaint['complaint_type'], 'area': complaint['area'], 'ward_no': complaint['ward_no'], 'desc': complaint['desc'], 'complaint_status': complaint['complaint_status'],'file_upload':complaint['file_upload']})
      template = loader.get_template('admindashboard.html')
      context = {'mycomplaints':mycomplaints}
      return HttpResponse(template.render(context, request))
  else:
     return redirect('/login')
  
def pendingcomplaints(request):
   if request.session.has_key('email'):
      if request.session.has_key('password'):
        pending = "pending"
        complaints = Complaint_registration.objects.filter(complaint_status=pending)
        mycomplaints = []
        for complaint in complaints:
           mycomplaints.append({'unique_id':complaint.unique_id,'fname': complaint.fname, 'lname': complaint.lname, 'phonenumber': complaint.phonenumber, 'email': complaint.email, 'complaint_type': complaint.complaint_type, 'area': complaint.area, 'ward_no': complaint.ward_no, 'desc': complaint.desc, 'complaint_status': complaint.complaint_status,'file_upload':complaint.file_upload})
        template = loader.get_template('pendingcomplaints.html')
        context = {'mycomplaints':mycomplaints}
        return HttpResponse(template.render(context, request))
   else:
       return redirect('/login')
      
def updatependingcomplaintspage(request, unique_id):
   if request.session.has_key('email'):
      if request.session.has_key('password'):
         complaint = Complaint_registration.objects.get(unique_id=unique_id)
         complaint.complaint_status= "completed"
         complaint.save()
         return redirect('/login/admin/pendingcomplaints')
   else:
      return redirect('/login')
   
def deletecomplaintpage(request, unique_id):
   if request.session.has_key('email'):
      if request.session.has_key('password'):
         complaint = Complaint_registration.objects.get(unique_id=unique_id)
         complaint.delete()
         return redirect('/login/home/profile')
   else:
      return redirect('/login')

def contactus(request):
   if request.session.has_key('email'):
    if request.session.has_key('password'):
      complaints = Contact.objects.all().values()
      mycomplaints = []
      for complaint in complaints:
        mycomplaints.append({'username': complaint['username'],'email_id': complaint['email_id'],'message': complaint['message']})
      template = loader.get_template('admincontactus.html')
      context = {'mycomplaints':mycomplaints}
      return HttpResponse(template.render(context, request))
   else:
     return redirect('/login')

def completedcomplaints(request):
   if request.session.has_key('email'):
      if request.session.has_key('password'):
        completed = "completed"
        complaints = Complaint_registration.objects.filter(complaint_status=completed)
        mycomplaints = []
        for complaint in complaints:
           mycomplaints.append({'fname': complaint.fname, 'lname': complaint.lname, 'phonenumber': complaint.phonenumber, 'email': complaint.email, 'complaint_type': complaint.complaint_type, 'area': complaint.area, 'ward_no': complaint.ward_no, 'desc': complaint.desc, 'complaint_status': complaint.complaint_status,'file_upload':complaint.file_upload})
        template = loader.get_template('resolvedcompliants.html')
        context = {'mycomplaints':mycomplaints}
        return HttpResponse(template.render(context, request))
   else:
       return redirect('/login')

def logoutpage(request):
   try:
      del request.session['email']
      del request.session['password']
   except KeyError:
      pass
   return redirect('/')

def logout(request):
   try:
      del request.session['email']
      del request.session['password']
   except KeyError:
      pass
   return redirect('/')

@csrf_exempt
def addcontactdetailspage(request):
   if request.method == 'POST':
      username = request.POST['username']
      email = request.POST['email']
      message = request.POST['message']
      result = Contact(username=username, email_id=email, message=message)
      result.save()
      return redirect('/login/home')
               
@csrf_exempt
def addcomplaintdetails(request):
  if request.session.has_key('email'):
    if request.session.has_key('password'):
       if request.method == 'POST':
        unique_id = uuid.uuid4().hex
        fname = request.POST['fname']
        lname = request.POST['lname']
        pnumber= request.POST['phonenumber']
        email = request.session['email']
        complaint_type = request.POST['typeOfComplaint']
        area = request.POST['area']
        wardnumber = request.POST['wardNumber']
        desc = request.POST['description']
        complaint_status = "pending"
        # Check if file is uploaded or not
        if 'file' in request.FILES:
            file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(file.name, file)
            uploaded_file_url = fs.url(filename)
        else:
            uploaded_file_url = ""
        
        # Create a new Complaint_registration object and save it to the database
        result = Complaint_registration(unique_id=unique_id,fname=fname, lname=lname, phonenumber=pnumber, email=email, complaint_type=complaint_type, area=area, ward_no=wardnumber, desc=desc, file_upload=uploaded_file_url, complaint_status=complaint_status)
        result.save()        
        return redirect('/login/home')
    else:
        return redirect('/login/home')

def profilepage(request):
  if request.session.has_key('email'):
     if request.session.has_key('password'):
        email = request.session['email']
        password = request.session['password']
        user = User.objects.get(email_id=email, password=password)
        mydata = {'email': user.email_id, 'name': user.name, 'phonenumber': user.phonenumber, 'unique_id':user.unique_id,'address':user.address,'pincode':user.pincode}
        complaints = Complaint_registration.objects.filter(email=email)
        mycomplaints = []
        for complaint in complaints:
           mycomplaints.append({'unique_id':complaint.unique_id,'fname': complaint.fname, 'lname': complaint.lname, 'phonenumber': complaint.phonenumber, 'email': complaint.email, 'complaint_type': complaint.complaint_type, 'area': complaint.area, 'ward_no': complaint.ward_no, 'desc': complaint.desc, 'complaint_status': complaint.complaint_status,'file_upload':complaint.file_upload})
        template = loader.get_template('profile.html')
        context = {'mymembers': mydata,'mycomplaints':mycomplaints}
        return HttpResponse(template.render(context, request))
  return redirect('/login')

def deleterecord(request, id):
   if request.session.has_key('email'):
    if request.session.has_key('password'):
       user = User.objects.get(pk=id)
       user.delete()
       return redirect('login/home/profile')
   else:
      return redirect('/login');