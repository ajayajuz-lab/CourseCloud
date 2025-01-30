from django.shortcuts import render,redirect
from django.views.generic import View
from student.forms import StudentCreateForm,StudentSigninForm
from django.contrib.auth import authenticate,login

# Create your views here.
class StudentCreateView(View):
    def get(self,request,*args,**kwargs):
        form_instance = StudentCreateForm()
        return render(request,"register.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):
        form_data=request.POST
        form_instance=StudentCreateForm(form_data)
        
        if form_instance.is_valid():
            form_instance.save()
            return redirect("student-create")
        
        else:
            return render(request,"register.html",{"form":form_instance})

class StudentSigninView(View):
    def get(self,request,*args,**kwargs):
        form_instance = StudentSigninForm()
        return render(request,"signin.html",{"form":form_instance})

    def post(self,request,*args,**kwargs):
        form_data = request.POST 
        form_instance = StudentSigninForm(form_data)
        
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            uname=data.get("username")
            pwd=data.get("password")
            
            user_instance=authenticate(request,username=uname,password=pwd)

            if user_instance and user_instance.role=="student":
                print(user_instance.role)
                login(request,user_instance)
                print(f"sign in success {request.user}")
                return redirect("student-create")
        
        else:
            return render(request,"signin.html",{"form":form_instance})
