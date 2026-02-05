from datetime import datetime
from pyexpat.errors import messages
from django.shortcuts import render,redirect # type: ignore
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from myapp import admin
from myapp.models import*
from .models import cart_table
from django.db.models import Q
from django.db.models import Avg





def login_get(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=authenticate(request,username=username,password=password)
        print(user)
        if user is not None:
            login(request,user)
            print("hhh")

            if user.groups.filter(name="admin").exists():
                print("kkkkkk")
                return JsonResponse({"status":"ok","lid":user.id,"type":"admin"})

            elif user.groups.filter(name='user').exists():
                print("kkk")
                return JsonResponse({"status":"ok","lid":user.id,"type":"user"})
        else:
            messages.warning(request,"invalid username or password")
            return JsonResponse({"status":"No"})
    
    else:
        return JsonResponse({"status":"No"})
    
    # registration

def registration_post(request):
    print(request.POST,"kkkkkkkkkkkkkkkkkkk")
    name=request.POST['name']
    phone=request.POST['phone']
    address=request.POST['address']
    email=request.POST['email']
    city=request.POST['city']
    pincode=request.POST['pincode']
    username=request.POST['username']
    password=request.POST['password']
    print(name,phone,email,address,city,pincode)
    user=User.objects.create(username=username,password=make_password(password),email=email,first_name=name)
    user.save()
    
    user.groups.add(Group.objects.get(name='user'))
    ob=user_table()
    ob.name=name
    ob.phone=phone
    ob.address=address
    ob.email=email
    ob.city=city
    ob.pincode=pincode
    ob.LOGIN=user
    ob.save()
    return JsonResponse({'message': 'Registered'})

# managecategory
def category_post(request):
    print(request.POST,"kkkkkkkkkkkkkkkkkkk")
    name=request.POST['name']
    category=request.POST['category']
    print(name,category)

    ob=category_table()
    ob.name=name
    ob.category=category
    
    ob.save()
    return JsonResponse({'message': 'Added'})

def view_category(request):
    ob=category_table.objects.all()
    l=[]
    for i in ob:
        l.append({
            "id":i.id,"name":i.name,"category":i.category})
    print(l,"ssss")
    return JsonResponse({"status":"ok","value":l})

def edit_category(request,id):
    print(request.POST,"kkkkkkkkkkkkkkkkkkk")
    name=request.POST['name']
    category=request.POST['category']
    print(name,"name")
    print(category,"category")

    ob=category_table.objects.get(id=id)
    ob.name=name
    ob.category=category
    ob.save()
    return JsonResponse({'status': True, 'message': 'Added successfully'})

def edit_category_get(request, id):
    ob = category_table.objects.get(id=id)

    data = {
        "id": ob.id,
       
        "name": ob.name,
        "category":ob.category
        
    }

    return JsonResponse({"status": "ok", "value": data})



def delete_category(request,id):
    ob=category_table.objects.get(id=id)
    ob.delete()
    return JsonResponse({'status':'ok'})

def notification_post(request):
    print(request.POST,"kkkkkkkkkkkkkkkkkkk")
    notification=request.POST['notification']
    date=request.POST['date']
    print(notification,date)

    ob=notification_table()
    ob.notification=notification
    ob.date=date
    
    ob.save()
    return JsonResponse({'message': 'Added'}) 

def view_notifications(request):
    ob=notification_table.objects.all()
    l=[]
    for i in ob:
        l.append({
            "id":i.id,"notification":i.notification,"date":i.date})
    print(l,"ssss")
    return JsonResponse({"status":"ok","value":l})

def products_post(request):
    print(request.POST,"kkkkkkkkkkkkkkkkkkk")
    
    name=request.POST['name']
    description=request.POST['description']
    price=request.POST['price']
    size=request.POST['size']
    color=request.POST['color']
    stock=request.POST['stock']
    date=request.POST['date']
    category=request.POST['category']
    image = request.FILES['image']
    print(name,description,price,size,color,stock,date,category)
    # pid=request.session['pid']

    ob=product_table()
    ob.name=name
    ob.description=description
    ob.price=price
    ob.size=size
    ob.color=color
    ob.stock=stock
    ob.date=date
    ob.CATEGORY=category_table.objects.get(id=category)
    ob.image=image
        
    ob.save()

    return JsonResponse({'status': True, 'message': 'Added successfully'}) 




def view_product(request):
    
    ob=product_table.objects.all()
    l=[]
    for i in ob:
        avg_rating = rating_table.objects.filter(
            PRODUCT=i.id
        ).aggregate(Avg('rating'))
        print(avg_rating,"aaaaaaaaaaaa")

        l.append({
            "id":i.id,
            "image":i.image.url,
            "name":i.name,
            "description":i.description,
            "price":i.price,
            "size":i.size,
            "color":i.color,
            "stock":i.stock,
            "date":i.date,
            # "rating":i.rating,
            "avg_rating":avg_rating['rating__avg'],
            "category":i.CATEGORY.name})
        print(l,"ssss")
    return JsonResponse({"status":"ok","value":l,
                         })

def delete_product(request,id):
    ob=product_table.objects.get(id=id)
    ob.delete()
    return JsonResponse({"status":"ok"})


def edit_product(request,id):
    print(request.POST,"kkkkkkkkkkkkkkkkkkk")
    # pid=request.POST['pid']
    name=request.POST['name']
    description=request.POST['description']
    price=request.POST['price']
    size=request.POST['size']
    color=request.POST['color']
    stock=request.POST['stock']
    date=request.POST['date']
    category=request.POST['category']
    # if 'image' in request.FILES:
    #         ob.image = request.FILES['image']
    print(name,description,price,size,color,stock,date,category)
    # pid=request.session['pid']
 
    ob=product_table.objects.get(id=id)
    ob.name=name
    ob.description=description
    ob.price=price
    ob.size=size
    ob.color=color
    ob.stock=stock
    ob.date=date
    ob.CATEGORY=category_table.objects.get(id=category)
    if 'image' in request.FILES:
            ob.image = request.FILES['image']
    # ob.image=image       
    ob.save()
    return JsonResponse({'status': True, 'message': 'Added successfully'}) 


def edit_get(request, id):
    ob = product_table.objects.get(id=id)

    data = {
        "id": ob.id,
        "image": ob.image.url if ob.image else "",
        "name": ob.name,
        "description": ob.description,
        "price": ob.price,
        "size": ob.size,
        "color": ob.color,
        "stock": ob.stock,
        "date": ob.date,
        # "category": ob.CATEGORY.id
        # "category": ob.CATEGORY.name
        "category": ob.CATEGORY.id
    }

    return JsonResponse({"status": "ok", "value": data})




def view_registered_user(request):
    ob=user_table.objects.all()
    l=[]
    for i in ob:
        l.append({
            "id":i.id,
            "name":i.name,
            "phone":i.phone,
            "address":i.address,
            "email":i.email,
            "city":i.city,
            "pincode":i.pincode,
            "login":i.LOGIN.id})
    print(l,"ssss")
    return JsonResponse({"status":"ok","value":l})

def view_all_products_user(request,category):
    print(category,"aaa")
    ob=product_table.objects.filter(CATEGORY__category=category)
    print(ob,"daaa")
    l=[]
    for i in ob:
        avg_rating = rating_table.objects.filter(
            PRODUCT=i.id
        ).aggregate(Avg('rating'))
        print(avg_rating,"aaaaaaaaaaaa")

        l.append({
            "id":i.id,
            "image":i.image.url,
            "name":i.name,
            "color":i.color,
            "rating":i.rating,
            "price":i.price,
            "description":i.description,
            "date":i.date,
            "stock":i.stock,
            "avg_rating":avg_rating['rating__avg'],
            "size":i.size,
            "category":i.CATEGORY.name

        })
    print(l,"ssss")
    return JsonResponse({"status":"ok","value":l})

# def add_cart_post(request):   
#     print(request.POST,"kkkkkkkkkkkkkkkkkkk")  
#     # quantity=request.POST['quantity']
#     lid=request.POST['lid']
#     pid=request.POST['pid']
#     # print(quantity)
#     ob=cart_table()
#     ob.USER=user_table.objects.get(LOGIN_id=lid)
#     ob.PRODUCT=product_table.objects.get(id=pid)
#     ob.quantity=1
#     ob.save()
    
#     return JsonResponse({'message': 'Added'})



def add_cart_post(request):
    lid = request.POST['lid']
    pid = request.POST['pid']
      
    user = user_table.objects.get(LOGIN_id=lid)
    product = product_table.objects.get(id=pid)

    if product.stock <= 0:
        return JsonResponse({'message': 'Out of stock'})

    cart_item = cart_table.objects.filter(USER=user, PRODUCT=product)
    if cart_item.exists():
        return JsonResponse({'message': 'Already Added'})
        
    ob=cart_table()
    ob.USER=user_table.objects.get(LOGIN_id=lid)
    ob.PRODUCT=product_table.objects.get(id=pid)
    ob.quantity=1
    ob.save()

    product.stock -= 1
    product.save()

    return JsonResponse({'message': 'Added'})



# def add_cart_post(request):
#     lid = request.POST['lid']
#     pid = request.POST['pid']
#     action = request.POST.get('action') 

#     user = user_table.objects.get(LOGIN_id=lid)
#     product = product_table.objects.get(id=pid)
#     cart_item = cart_table.objects.filter(USER=user, PRODUCT=product)
#     if cart_item.exists():

#         return JsonResponse({'message': 'Already Added'})

    
#     cart_item, created = cart_table.objects.get_or_create(USER=user, PRODUCT=product, defaults={'quantity': 1})
#     if not created:
#         if action == "increase":
#             if product.stock > 0:
#                 cart_item.quantity += 1
#                 product.stock -= 1
#             else:
#                 return JsonResponse({"status": "error", "message": "Out of stock"})
#         elif action == "decrease":
#             if cart_item.quantity > 1:
#                 cart_item.quantity -= 1
#                 product.stock += 1
#             else:
#                 return JsonResponse({"status": "error", "message": "Quantity cannot be less than 1"})

#     else:
#         if product.stock <= 0:
#             cart_item.delete()
#             return JsonResponse({"status": "error", "message": "Out of stock"})
#         product.stock -= 1

#     cart_item.save()
#     product.save()

#     return JsonResponse({"status": "success", "message": "Cart updated"})


   



def view_cart(request):
    lid=request.POST["lid"]
    carts = cart_table.objects.filter(USER__LOGIN_id=lid)  # ideally filter by logged-in user

    data = []
    for i in carts:
        data.append({
            "id": i.id,
            "user": i.USER.name,
            "product": i.PRODUCT.name,
            "price": i.PRODUCT.price,
            "image": i.PRODUCT.image.url if i.PRODUCT.image else "",
            "quantity": i.quantity,
            "total": i.total_price()
        })

    return JsonResponse({"status": "ok", "value": data})



def update_quantity(request, id):
    if request.method=="POST":
        ob=request.POST.get("action")
        cart=cart_table.objects.get(id=id)
        product=cart.PRODUCT  

        if ob=="increase":
            if product.stock >0:
                cart.quantity +=1
                product.stock -=1
            else:
                return JsonResponse({
                    "status":"error",
                    "message":"Out of stock"
                })
            
        elif ob=="decrease":
            if cart.quantity >1:
                cart.quantity -=1
                product.stock +=1
        cart.save()
        product.save()
        return JsonResponse({
            "status":"ok",
            "quantity":cart.quantity,
            "total":cart.total_price(),
            "stock":product.stock
        })
    return JsonResponse({"status":"invalid"})

def delete_cart(request,id):
    ob=cart_table.objects.get(id=id)
    product = ob.PRODUCT
    quantity = ob.quantity
    product.stock += quantity
    product.save()
    ob.delete()
    return JsonResponse({"status":"ok"})


def add_order_post(request):
    print(request.POST,"kkkkkkkkkkkkkkkkkkk")  
    lid=request.POST['lid']
    cartid=request.POST['cid']
    print("lid:", lid)
    print("cid:", cartid)

    cart=cart_table.objects.get(id=cartid)
    pid=cart.PRODUCT.id
    qty=cart.quantity
    productprice=product_table.objects.get(id=pid).price
    total=int(qty)*int(productprice)
    print(pid,qty,productprice,total)
    
    ob=order_table()
    ob.USER=user_table.objects.get(LOGIN_id=lid)
    ob.total_price=int(qty)*int(productprice)
    ob.status="PAID"
    ob.date=datetime.now().today()
    ob.save()

    obj=order_item_table()
    obj.ORDER=ob
    obj.PRODUCT=product_table.objects.get(id=pid)
    obj.quantity=qty
    obj.price=productprice
    obj.date=datetime.now().today()
    obj.save()

    cart.delete()

    return JsonResponse({'message': 'Added',
                        'status': ob.status
                         })

def view_order(request):
    lid=request.POST["lid"]
    order = order_table.objects.filter(USER__LOGIN_id=lid)  
    
    data = []
    for idx, i in enumerate(order, start=1):
    # for i in order:
        data.append({

            "id": i.id,
            "slno":idx,
            "date":i.date,
            "user": i.USER.name,
            "total_price": i.total_price,
            "status":i.status,           
        })
    print(data)
    return JsonResponse({"status": "ok", "value": data})
    
def view_order_more(request):
    # lid=request.POST["lid"]
    orderid=request.POST["orderid"]
    order = order_item_table.objects.filter(ORDER_id=orderid)
    # pid=request.POST["pid"]

    data = []
    for idx, i in enumerate(order, start=1):
        data.append({

            "id": i.id,
            "slno":idx,
            "date":i.date,
            "order":i.ORDER.id,
            "product":i.PRODUCT.name,
            "pid":i.PRODUCT.id,
            # "image": i.PRODUCT.image,
            "size":i.PRODUCT.size,
            "image": i.PRODUCT.image.url if i.PRODUCT.image else "",
            "quantity":i.quantity,
            "price": i.price           
        })
    print(data)
    return JsonResponse({"status": "ok", "value": data})

def admin_view_order(request):
    # lid=request.POST["lid"]
    order = order_table.objects.all()  # ideally filter by logged-in user
    data = []
    for idx, i in enumerate(order, start=1):
    # for i in order:
        data.append({

            "id": i.id,
            "slno":idx,
            "date":i.date,
            "user": i.USER.name,
            "total_price": i.total_price,
            "status":i.status,
          
        })
    print(data)
    return JsonResponse({"status": "ok", "value": data})

def admin_view_order_more(request):
    print(request.POST,"KKKKKKKKKKKKK")
    ordermoreid=request.POST["ordermoreid"]
    order = order_item_table.objects.filter(ORDER_id=ordermoreid)   
    data = []
    for idx, i in enumerate(order, start=1):
        data.append({

            "id": i.id,
            "slno":idx,
            "date":i.date,
            "order":i.ORDER.id,
            "image": i.PRODUCT.image.url if i.PRODUCT.image else "",
            "product":i.PRODUCT.name,
            "size":i.PRODUCT.size,
            "quantity":i.quantity,
            "price": i.price,
            
            
        })
    print(data)
    return JsonResponse({"status": "ok", "value": data})



# def add_rating(request):
#     try:
#         lid = request.POST.get('lid')
#         pid = request.POST.get('pid')
#         rating = request.POST.get('rating')
#         review = request.POST.get('review')
#         date = request.POST.get('date') or datetime.now().date()

#         user = user_table.objects.get(LOGIN_id=lid)
#         product = product_table.objects.get(id=pid)

#         ob = rating_table()
#         ob.USER = user
#         ob.PRODUCT = product
#         ob.rating = rating
#         ob.review = review
#         ob.date = date
#         ob.save()

#         return JsonResponse({'status': True, 'message': 'Rating added successfully'})

#     except user_table.DoesNotExist:
#         return JsonResponse({'status': False, 'message': 'User not found'})
#     except product_table.DoesNotExist:
#         return JsonResponse({'status': False, 'message': 'Product not found'})
#     except Exception as e:
#         return JsonResponse({'status': False, 'message': str(e)})


def add_rating(request):
  
    lid = request.POST.get('lid')
    pid = request.POST.get('pid')
    rating = request.POST.get('rating')
    review = request.POST.get('review')

    print(rating,review,pid,lid)

    user = user_table.objects.get(LOGIN_id=lid)
    product = product_table.objects.get(id=pid)

    ob = rating_table.objects.create(
        USER=user,
        PRODUCT=product,
        rating=int(rating),   
        review=review
    )

    return JsonResponse({
        'status': True,
        'message': 'Rating added successfully'
    })





