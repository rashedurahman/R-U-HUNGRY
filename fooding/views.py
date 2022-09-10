import json
from watson import search as watson
from django.contrib import messages
from fooding.models import Cart, Order, Review
from seller.models import Menu, Restaurant
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
# Create your views here.
def homePage(request):
    restaurants = Restaurant.objects.filter(type='restaurant', )[:8]
    homechefs = Restaurant.objects.filter(type='home', )[:8]
    context = {
        'restaurants' : restaurants,
        'homechefs': homechefs,
    }
    # landing page
    return render(request, 'fooding/index.html', context)


def searchPage(request):
    # Search result
    searchText = request.GET.get('q')

    restaurants = watson.filter(Restaurant, searchText).filter(type='restaurant')
    homechefs = watson.filter(Restaurant, searchText).filter(type='home')
    foods = watson.filter(Menu, searchText).filter(is_available=True)

    context = {
        'restaurants' : restaurants,
        'homechefs': homechefs,
        'foods' : foods,
    } 

    return render(request, 'fooding/search.html', context)

def notificationsPage(request):
    # can give review 
    # can see notifications 
    return render(request, '')

@login_required
def cartPage(request):
    context ={
        'items' : Cart.objects.all(),
    }
    if Cart.objects.all().count() > 0:
        context['rid'] = Cart.objects.all()[0].restaurant.id

    return render(request, 'fooding/cart.html', context)

@login_required
def deleteCartItem(request, id):
    Cart.objects.get(id=id).delete()
    messages.success(request, "Item Removed from Cart.")
    return redirect('carts')

@login_required
def addToCart(request, rid, iid):
    path = "/restaurants/menu/" + str(rid)
    # print(path)
    try:
        restaurant = Restaurant.objects.get(id=rid)
        item = Menu.objects.get(id=iid)
        for i in Cart.objects.filter(user_id=request.user.id):
            if i.restaurant.name != restaurant.name:
                i.delete()
                Cart.objects.create(restaurant=restaurant, item=item, user_id=request.user.id, quantity=1, total_price=item.price)
                messages.success(request, "Item Added to Cart. Go to cart page to update quantity. Previous items cleared from cart from another restaurant.")
                return redirect(path)
            elif i.restaurant.name == restaurant.name and i.item.name == item.name:
                i.quantity = i.quantity + 1
                i.total_price = i.total_price + i.item.price
                i.save()
                messages.success(request, "Quantity Increased in Cart")
                return redirect(path)

        Cart.objects.create(restaurant=restaurant, item=item, user_id=request.user.id, quantity=1, total_price=item.price)
        messages.success(request, "Item Added to Cart. Go to cart page to update quantity.")
        return redirect(path)
    except:
        return HttpResponse("Invalid Operation")
    
@login_required
def compliteOrder(request):
    if request.method == 'POST':
        
        data = request.POST.get('senddata')
        print(data)
        obj = json.loads(data)
        print(obj)
      
        for i in obj:
            restaurant = Restaurant.objects.get(id=int(i['rid']))
            cart = Cart.objects.get(id=int(i['productId']))
            item = Menu.objects.get(id=cart.item.id)
            total_price = int(i['price'])
            quantity = total_price/item.price
            Order.objects.create(restaurant = restaurant,
                                    user_id = request.user.id,
                                    item = item,
                                    quantity = quantity,
                                    total_price = total_price)
            cart.delete()
        
        messages.success(request, "Order Placed Successfully")
   
        return JsonResponse({'status':200})
        
 
def reviewPage(request):
    # see all reviews 
    return render(request, 'fooding/review.html', {'revs':Review.objects.all().order_by('-id')}) 

def restaurantReviewPage(request,id):
    # see all reviews 
    return render(request, 'fooding/review.html', {'revs':Review.objects.filter(restaurant_id=id).order_by('-id')}) 

def restaurantPage(request):
    restaurants = Restaurant.objects.filter(type='restaurant', )
    homechefs = Restaurant.objects.filter(type='home', )
    context = {
        'restaurants' : restaurants,
        'homechefs': homechefs,
    } 
    return render(request, 'fooding/restaurent.html', context) 

def menuPage(request, id):
    try:
        x = Restaurant.objects.get(id=id)
        restaurant = Menu.objects.filter(retaurant_id=id, is_available=True)
        context = {
            'restaurantInfo' : x,
            'menuInfo' : restaurant
        }    
        return render(request, 'fooding/menu.html', context) 
    except:
        return HttpResponse("Restaurant Not Found")

    

def createGeneralOrder(request):
    return render(request, 'dashboard/generalUser/addOrder.html')

@login_required
def allGeneralOrder(request):
    if request.user.userdetail.is_admin:
        orders = Order.objects.all().order_by('-id')
        all_count = orders.count()
        delivered_count = Order.objects.filter(status="Delivered").count()
        pending_count = Order.objects.filter(status="Pending").count()
    else:
        orders = Order.objects.filter(user_id=request.user.id).order_by('-id')
        all_count = orders.count()
        delivered_count = Order.objects.filter(user_id=request.user.id,status="Delivered").count()
        pending_count = Order.objects.filter(user_id=request.user.id,status="Pending").count()
    return render(request, 'dashboard/generalUser/allOrder.html', {'orders':orders, 'all_count':all_count, 'delivered_count':delivered_count, 'pending_count':pending_count })



@login_required
def user_give_review(request, id):
    item = Menu.objects.get(id=id)
    res = Restaurant.objects.get(id=item.retaurant.id)
    if Order.objects.filter(item=item, user_id=request.user.id, total_price__gte=200, is_reviewed=False, status="Delivered").exists():
        if request.method == 'POST':
            # print(request.POST['mess'])
            Review.objects.create(restaurant=res, item=item, user_id=request.user.id, review=request.POST['mess'])
            Order.objects.filter(item=item, user_id=request.user.id, total_price__gte=200, is_reviewed=False, status="Delivered").update(is_reviewed=True)
            messages.success(request, "Thanks for your review.")
            return redirect('allGeneralOrder')
        return render(request, 'fooding/give_review.html',{'item':item,})
    else:
        return HttpResponse("Invalid Request")