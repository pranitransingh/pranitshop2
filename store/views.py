from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from .models import Product
from .models import Category
from .models import Customer
from .models import Order

from django.contrib.auth.hashers import make_password  ,   check_password
from django.views import View

from store.middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator




#INDEX PAGE
class Index(View):
    def post(self,request):
        product=request.POST.get('product')
        remove=request.POST.get('remove')
        cart=request.session.get('cart')
        if cart:
            quantity=cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]=quantity - 1
                else:
                    cart[product]=quantity + 1

            else:
                cart[product]=1
        else:
            cart={}
            cart[product]=1

        
        request.session["cart"]=cart
        print(request.session['cart'])
        return redirect('homepage')
        
    def get(self,request): 
        cart=request.session.get('cart')
        if not cart:
            request.session['cart']={}
        product = None
        
        categories = Category.get_all_categories() 

        category_id=request.GET.get('category')
        if category_id:
            product=Product.get_all_product_by_categoryid(category_id)
            
        else:
            product=Product.get_all_product()
            

        data={'products': product , 'categories': categories}
        print('you are :',request.session.get('email'))

        
        return render(request,'store/index.html',data )
  
   
#SIGNUP !!   
class Signup(View):
    def get(self,request):
        return render(request,'store/signup_page.html')
    def post(self,request):
        postData=request.POST
        
        email=postData.get('email')
        password=postData.get('password')
        first_name=postData.get('firstname')
        last_name=postData.get('lastname')
        phone=postData.get('phone')

        #validations 
        customer=Customer(first_name=first_name,
                                last_name=last_name,
                                phone=phone,
                                email=email,
                                password=password)
        value={
            'first_name':first_name,
            'last_name':last_name,
            'phone':phone,
            'email':email
        }
        error_message=None

        if(not first_name):
            error_message='Enter First Name'
        elif len(first_name) < 4:
            error_message='First Name should be more tha 4 letters'
        elif not last_name :
            error_message='Enter Last name'
        elif not phone:
            error_message="Enter Phone Number"
        elif len(phone) <10:
            error_message="Phone NUmber should atlest 10 chars"
        elif not email:
            error_message="Plese Enter your Email "
        elif len (password)<4:
            error_message="Password Should Be more than 4 chars"
        elif customer.isExist():
            error_message="Existing Email Entered"
        
        #savings
        if not error_message:
            print(email,password,first_name,last_name,phone)

            
            customer.password=make_password(customer.password)
            customer.Register()
            return redirect('homepage')
        else:
            data={
                'error':error_message,
                'values':value
            }
            return render (request,'store/signup_page.html',data)

#LOGIN
class Login(View):
    return_url=None
    def get(self,request):  
        Login.return_url=request.GET.get('return_url')  
        return render(request,'store/login_page.html')
    def post(self,request):
        email=request.POST.get('email')
        password=request.POST.get('password')
        customer=Customer.get_customer_by_email(email)
        error_message=None
        if customer:
            flag=check_password(password,customer.password)
            if flag:
                request.session['customer']= customer.id
                
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                    
                else:
                    Login.return_url=None
                    return redirect('homepage')
            else:
                error_message="Email or Password Invalid"
        else:
            error_message="Email or Password Invalid"
        
        print(email,password)
        return render(request,'store/login_page.html',{'error':error_message})

def logout(request):
    request.session.clear()
    return redirect ('login')

#Cart 
class Cart(View):
    
    def get(self,request):   
        ids=list(request.session.get('cart').keys())
        products=Product.get_product_by_id(ids)
        print(products)
        return render(request,'store/cart.html', {'products':products})

#checkout
class CheckOut(View):
    
    def post(self,request):   
        address= request.POST.get('address')
        phone= request.POST.get('phone')
        customer=request.session.get('customer')
        cart=request.session.get('cart')
        products= Product.get_product_by_id(list(cart.keys()))
        print(address,phone,customer,cart,products)

        for product in products:
            order=Order(customer=Customer(id=customer),
                        product=product,
                        price=product.price,
                        address=address,
                        phone=phone,
                        quantity=cart.get(str(product.id)))

            print(order.placeorder())
        request.session['cart']={}
        
        return redirect('cart')


#ORDERS

class OrderView(View):
    
    def get(self,request):   
        customer=request.session.get('customer')
        orders=Order.get_orders_by_customer(customer)
        print(orders)
        return render(request,'store/orders.html',{'orders': orders})
        

        
 
    



        