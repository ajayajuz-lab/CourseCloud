from django.shortcuts import render,redirect
from django.views.generic import View,FormView,CreateView,TemplateView
from student.forms import StudentCreateForm,StudentSigninForm
from django.contrib.auth import authenticate,login
from django.urls import reverse_lazy


class StudentCreateView(CreateView):
    template_name="register.html"
    form_class=StudentCreateForm
    success_url=reverse_lazy("signin")

class LoginView(FormView):
    template_name="signin.html"
    form_class=StudentSigninForm

    def post(self,request,*args,**kwargs):
        form_data = request.POST 
        form_instance = StudentSigninForm(form_data)
        
        if form_instance.is_valid():
            data=form_instance.cleaned_data
            uname=data.get("username")
            pwd=data.get("password")
            
            user_instance=authenticate(request,username=uname,password=pwd)

            if user_instance :
                print(user_instance.role)
                login(request,user_instance)
                print(f"sign in success {request.user}")
                return redirect("index")
            else:
                return render(request,"signin.html",{"form":form_instance})
                
        
        else:
            return render(request,"signin.html",{"form":form_instance})

class IndexView(TemplateView):
    template_name="index.html"
