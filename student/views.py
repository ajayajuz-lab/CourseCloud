from django.shortcuts import render,redirect
from django.views.generic import View,FormView,CreateView,TemplateView
from student.forms import StudentCreateForm,StudentSigninForm
from django.contrib.auth import authenticate,login
from django.urls import reverse_lazy
from django.contrib import messages
from instructor.models import Course,Cart,Order,Module,Lesson
from django.db.models import Sum
import razorpay



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
        purchased_courses=Order.objects.filter(student=request.user).values_list("course_objects",flat=True)
        print(purchased_courses)
        return render(request,"index.html",{"courses":all_courses,"purchased_courses":purchased_courses})

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

class OrderCheckoutView(View):
    def get(self,request,*args,**kwargs):
        cart_items=request.user.basket.all()
        order_total=sum([ci.course_object.price for ci in cart_items])
        order_instance=Order.objects.create(student=request.user,total=order_total)

        for ci in cart_items:
            order_instance.course_objects.add(ci.course_object)
            ci.delete()
        order_instance.save()
        if order_total>0:
            client = razorpay.Client(auth=(RZP_KEY_ID, RZP_KEY_SECRET))
            data = { "amount": int(order_total*100), "currency": "INR", "receipt": "order_rcptid_11" }
            payment = client.order.create(data=data)
            print(payment)

        return redirect("index")

class MycoursesView(View):
    def get(self,request,*args,**kwargs):
        purchased_courses=request.user.purchase.all()
        print(purchased_courses)
        return render(request,"mycourses.html",{"orders":purchased_courses})

# class CartEmptyView(View):
#     def get(self,request,*args,**kwargs):

# localhost:8000/student/courses/1/watch?module=2&lesson=5

class LessonDetailView(View):
    def get(self,request,*args,**kwargs):
        course_id=kwargs.get("pk")
        course_instance=Course.objects.get(id=course_id)
        #request.GET={"module":2,"lesson":5}
        query_params=request.GET
        module_id=query_params.get("module") if "module" in query_params else course_instance.modules.all().first().id
        module_instance=Module.objects.get(id=module_id,course_object=course_instance)

        lesson_id=query_params.get("lesson") if "lesson" in query_params else module_instance.lessons.all().first().id
        lesson_instance=Lesson.objects.get(id=lesson_id,module_object=module_instance)

        return render(request,"lesson_detail.html",{"course":course_instance,"lesson":lesson_instance})