from django.shortcuts import render,redirect
from django.views.generic import View,FormView,CreateView,TemplateView
from student.forms import StudentCreateForm,StudentSigninForm
from django.contrib.auth import authenticate,login
from django.urls import reverse_lazy
from django.contrib import messages
from instructor.models import Course,Cart
from django.db.models import Sum

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

class IndexView(View):
    def get(self,request,*args,**kwargs):
        all_courses=Course.objects.all()
        return render(request,"index.html",{"courses":all_courses})

class CourseDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        course_instance=Course.objects.get(id=id)
        return render(request,"course_detail.html",{"course":course_instance})

class AddToCartView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        course_instance=Course.objects.get(id=id)
        user_instance=request.user
        # Cart.objects.create(course_object=course_instance,user=user_instance)
        cart_instance,created=Cart.objects.get_or_create(course_object=course_instance,user=user_instance)
        if created:
            messages.success(request,"Successfully added to the cart")
            print(created,"======")
        else:
            messages.error(request,"Can't add.Item existing in cart")
        return redirect("index")

class CartSummaryView(View):
    def get(self,request,*args,**kwargs):
        qs=request.user.basket.all()
        cart_total=qs.values("course_object__price").aggregate(total=Sum("course_object__price")).get("total")
        print(cart_total,"**********************************")
        return render(request,"cart-summary.html",{"carts":qs,"basket_total":cart_total})

class CartItemDeleteView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Cart.objects.get(id=id).delete()
        return redirect("cart-summary")