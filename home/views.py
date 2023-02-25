

# Create your views here.
from django.shortcuts import render, redirect, HttpResponse
from django.views.decorators.cache import never_cache
from .models import Users as u, admin, product as p, category as c, cart as car, cart_list as cl, Address as a, orders as o, order_list as ol, payment as pay, banner, coupon
from django.core.paginator import Paginator                                
from .forms import ProductForm,AddBanner
import datetime
import random
from random import randint
import calendar
from django.db.models import Count, Q, F
from django.db.models.functions import ExtractYear, ExtractMonth
import requests
from requests import request
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib import messages
import pyotp
from django.core.mail import send_mail
from datetime import datetime
from random import randint
import json
from django.http.response import JsonResponse
import openpyxl
from openpyxl import Workbook
import pytz
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import StringIO

# Create your views here.

# //--User Functions --//

def page_not_found(request,exception):
    return render(request, 'user/404.html',status=404)

def user_login(request):
    if 'email' in request.session:
        return render(request, 'user/homepage.html')
    else:    
        return render(request, "user/userlogin.html")
    
def login(request):
    if 'email' in request.session:
        return render(request, 'user/homepage.html',)
        
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user=u.objects.filter(email=email,password=password).count()
        if user==1:
            userok=u.objects.get(email=email,password=password)
            if userok.status == 'Active':
                request.session['email']=userok.email
                request.session['uid']=userok.userid
                return redirect('homepage')
            elif userok.status == 'Blocked':
                messages.error(request,'You are Blocked!')
                return redirect('/user_login')
            else:
                messages.error(request,'E-mail Not Verified!')
                return redirect('/user_login')
        else:
            messages.error(request,'Invalid Username/Password')
            return redirect('/user_login')
    else:
        return redirect('/user_login')
    
def userprofile(request):
    id=request.session["uid"]
    data=u.objects.get(userid=id)
    adds = a.objects.filter(uid = data.userid)
    return render(request,'user/userprofile.html', {'data': data, 'adds':adds})

@never_cache   
def homepage(request):
    if 'email' in request.session:
        if 'search' in request.GET:
            search = request.GET['search']
            prod = p.objects.filter(pname__icontains = search)
            cat=c.objects.all()
            ban=banner.objects.all()
            paginator = Paginator(prod, 8)
            page = request.GET.get('page')
            details = paginator.get_page(page)
            return render(request,'user/homepage.html',{'details': details, 'cat': cat, 'ban': ban, 'keyword' : search})
        else:
            prod=p.objects.all()
            cat=c.objects.all()
            ban=banner.objects.all()
            paginator = Paginator(prod, 8)
            page = request.GET.get('page')
            details = paginator.get_page(page)
            return render(request,'user/homepage.html',{'details': details, 'cat': cat, 'ban': ban}) 
    else:
        return render(request,'user/userlogin.html')
    
def user_signup(request):
    if 'email' in request.session:
        return render(request, 'user/homepage.html')
    elif request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password == confirm_password:    
            user=u.objects.create(name=name,email=email,password=password)
            user.save()
            secret=pyotp.random_base32()
            totp=pyotp.TOTP(secret,interval=300)
            otp=totp.now()
            recipient_list=user.email
            print(user.email)
            send_mail('Bookies','Your one time password for bookies is '+str(otp)+'.OTP will expire within 5 minutes','bookiess.com@gmail.com', [recipient_list],fail_silently=True)
            response= redirect(f'otp_verification/{user.userid}/{secret}')
            response.set_cookie("can_otp_enter",True,max_age=500)
            return response
        else:
            messages.error(request,'Password is not matching')
            return redirect('/user_signup')
    else:
        return render(request,"user/usersignup.html")
    
def otp_verification(request,userid,secret):
    if request.POST:
        totp=pyotp.TOTP(secret,interval=300)
        print(totp.now())
        try:
            user=u.objects.get(userid=userid)
        except u.DoesNotExist:
            messages.error(request,'user not found')
            return redirect('user_signup')
        code=request.POST['1']+request.POST['2']+request.POST['3']+request.POST['4']+request.POST['5']+request.POST['6']
        if request.COOKIES.get('can_otp_enter')!=None:
            if (totp.verify(code)):
                if(user.status == 'Inactive'):
                    user.status = 'Active'
                    user.save()
                    response=redirect('user_login')
                    response.set_cookie('verified',True)
                    messages.success(request,'Verification Success')
                    return response
                else:
                    messages.error(request,'wrong otp')
                    return render(request,'user/otp.html')
            else:
                messages.error(request,'Something Went Wrong')
                return render(request,'user/otp.html')
        else:
            messages.error(request,'OTP expired')
            return render(request,'user/otp.html')
    else:
        return render(request,'user/otp.html')
    
    
def user_logout(request):
    if 'email' in request.session:
        del request.session['email']
    return redirect('landingpage')

def landingpage(request):
    if 'email' in request.session:
        return redirect('homepage')
    else:
        ban=banner.objects.all()
        if 'search' in request.GET:
            search=request.GET['search']
            details=p.objects.filter(pname__icontains=search)
            return render(request,'user/landingpage.html',{'details': details,'keyword': search,'ban': ban})
            
        else:
            details=p.objects.all()
            cat=c.objects.all()
            return render(request,'user/landingpage.html',{'details': details, 'cat': cat,'ban': ban})
        

def productpage(request):
        cat=c.objects.all()
        if 'search' in request.GET:
            search=request.GET['search']
            prod=p.objects.filter(pname__icontains=search)
            paginator = Paginator(prod, 8)
            page = request.GET.get('page')
            details = paginator.get_page(page)
            return render(request,'user/productpage.html',{'details': details,'cat': cat, 'keyword': search})
        
        elif 'filter' in request.POST:
            min = request.POST['min']
            max = request.POST['max']
            if not max:
                prod = p.objects.filter(price__gte=min)
                paginator = Paginator(prod, 8)
                page = request.GET.get('page')
                details = paginator.get_page(page)
                return render(request, 'user/productpage.html', {'details': details, 'cat': cat, 'min': min})
            
            elif not min:
                prod = p.objects.filter(price__lte=max)
                paginator = Paginator(prod, 8)
                page = request.GET.get('page')
                details = paginator.get_page(page)
                return render(request, 'user/productpage.html', {'details': details, 'cat': cat, 'max': max})
            
            else:
                prod = p.objects.filter(price__gte=min, price__lte=max).all()
                paginator = Paginator(prod, 8)
                page = request.GET.get('page')
                details = paginator.get_page(page)
                return render(request, 'user/productpage.html', {'details': details, 'cat': cat, "min": min, "max": max})
            
        else:
            prod=p.objects.all()
            cat=c.objects.all()
            paginator = Paginator(prod, 8)
            page = request.GET.get('page')
            details = paginator.get_page(page)
            return render(request,'user/productpage.html',{'details': details, 'cat': cat})
       
def cat_sort(request):
        
    cat = c.objects.all()
    cat_id = request.GET['cat_id']
    pro = p.objects.filter(cid=cat_id).all()
    return render(request, 'user/category.html', {'cat': cat, 'pro': pro})       

def product_details(request):
    pid=request.GET["pid"]
    details=p.objects.get(productid=pid)
    print(details.image)
    return render(request,"user/productdetails.html",{'details':details})

def checkout(request):
    usid = request.session.get("uid")
    if not usid:
        return redirect("user_login")

    user = u.objects.filter(userid=usid).first()
    if not user:
        return redirect("user_signup")

    cart = car.objects.filter(uid=user).first()
    if not cart:
        return redirect("homepage")
    
    cart_items = cl.objects.filter(ctid=cart)
    address = a.objects.filter(uid=user)
    total_amount = 0
    for item in cart_items:
        product = item.pid
        quantity = item.quantity
        total_amount += product.price * quantity

    if 'coupcode' in request.GET:
        coupcode = request.GET['coupcode']
        comp = coupon.objects.get(coupname = coupcode)
        coup = None
        if comp:
            coup = coupcode
            cprice = int(comp.price)
            total_amount -= cprice
            
        else:
            messages.warning(request, 'Invalid Coupon Code')
            return render(request,"user/checkout.html")
        context = {
        "cart_items": cart_items,
        "address": address,
        "total_amount": total_amount,
        "coup": coup,
        "cprice" : cprice,
       
        }
        car.objects.filter(uid=user).update(total = total_amount)
        return render(request,"user/checkout.html", context)
    else:
        context = {
        "cart_items": cart_items,
        "address": address,
        "total_amount": total_amount,
       
        }
        car.objects.filter(uid=user).update(total = total_amount)
        return render(request,"user/checkout.html", context)
    


def add_to_cart(request):
    uid = request.session.get("uid")
    if not uid:
        return redirect("login")

    user = u.objects.filter(userid=uid).first()
    if not user:
        return redirect("login")

    pid = request.GET.get("pid")
    product = p.objects.filter(productid=pid).first()
    if not product:
        return redirect("home")
 
    cart, created = car.objects.get_or_create(uid=user)
    cart_item, created = cl.objects.get_or_create(pid=product, ctid=cart)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item.quantity = 1
        cart_item.save()

    return redirect("cart")

def cart(request):
    uid = request.session.get("uid")
    if not uid:
        return redirect("user_login")

    user = u.objects.filter(userid=uid).first()
    if not user:
        return redirect("user_signup")

    cart = car.objects.filter(uid=user).first()
    if not cart:
        return redirect("homepage")

    cart_items = cl.objects.filter(ctid=cart)
    context = {
        "cart_items": cart_items,
    }
    return render(request, "user/cart.html", context)


def delete_cart_items(request):
    clid=request.GET["clid"]
    cl.objects.filter(cartlistid=clid).delete()
    return redirect("cart")


def add_address(request):
    user_id = request.session.get("uid")
    if not user_id:
        return redirect("user_login")

    user = u.objects.filter(userid=user_id).first()
    if not user:
        return redirect("user_login")
    
    if request.method == 'POST':
        hname = request.POST.get("add_hname", "")
        hnum = request.POST.get("add_hnum", "")
        street = request.POST.get("add_street", "")
        district = request.POST.get("add_district", "")
        state = request.POST.get("add_state", "")
        pincode = request.POST.get("add_pincode", "")

        if not all([hname, hnum, street, district, state, pincode]):
            messages.error(request, "All fields are required")
            return redirect("checkout")

        a.objects.create(hname=hname, hno=hnum, street=street,district=district, state=state,pincode=pincode, uid=user)
        messages.success(request, "Address added successfully")
        return redirect("checkout")
    else:
        return render(request, "user/checkout.html")


def cash_on_delivery(request):
    user_id = request.session.get('uid')
    # data=u.objects.get(userid=user_id)
    total_amount = request.GET['total_amount']
    if not user_id:
        return redirect('user_login')

    order_id = randint(1000, 9999)
    order_lid = randint(1000,9999)
    cart = car.objects.filter(uid=user_id).first()
    items = cl.objects.filter(ctid=cart)
    address = a.objects.filter(uid=user_id).first()
    order = o.objects.create(order_id=order_id,amount=total_amount, aid=address)
    datas = o.objects.get(order_id=order_id)
    pay.objects.create(oid=datas)

    for item in items:
        datap=item.pid
        dataq=item.quantity
        dataa=item.total_price

        ol.objects.create(oid=order,uid = cart.uid, pid=datap, quantity=dataq, total_price = dataa, order_lid = order_lid)
        stoc = p.objects.get(productid=item.pid.productid)
        stocc = int(stoc.stock) - int(dataq)
        p.objects.filter(productid = datap.productid).update(stock=stocc)
    items.delete()
    return render(request, 'user/ordersuccessfull.html')

def cancel_order(request):
    order_id = request.GET['olid']
    ol.objects.filter(orderlistid = order_id).update(status = 'Cancelled')
    return redirect('order_management')

def user_order_cancel(request):
    order_id = request.GET['olid']
    ol.objects.filter(orderlistid = order_id).update(status = 'Cancelled')
    return redirect('order_history')


def cart_item_increment(request):

    if request.method == 'POST':
        pid = request.POST['product_id']

    user = u.objects.get(email=request.session['email'])
    cart = car.objects.get(uid = user.userid)
    cart_item = cl.objects.get(Q(pid=pid) & Q(ctid=cart.cartid))
    product = p.objects.get(productid=pid)
    if int(product.stock) - int(cart_item.quantity) > 0:
        cart_item.quantity += 1
    cart_item.total_price = product.price * cart_item.quantity
    cart_item.save()
    
    # cart_list = cl.objects.filter(ctid=cart.cartid)
    # total = 0
    # for item in cart_list:
    #     total += item.total_price
    return JsonResponse({'quantity': cart_item.quantity,'total_price':cart_item.total_price })


def cart_item_decrement(request):

    if request.method == 'POST':
        pid = request.POST['product_id']
        user = u.objects.get(email=request.session['email'])
        cart = car.objects.get(uid = user.userid)
        cart_item = cl.objects.get(Q(pid=pid) & Q(ctid=cart.cartid))
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            pass
        product = p.objects.get(productid=pid)
        cart_item.total_price = product.price * cart_item.quantity
        cart_item.save()
        
        # cart_list = cl.objects.filter(ctid=cart.cartid)
        # total = 0
        # for item in cart_list:
        #     total += item.total_price
        return JsonResponse({'quantity': cart_item.quantity,'total_price':cart_item.total_price })


# User Side
def order_history(request):
    user_id = request.session.get('uid')
    if not user_id:
        return redirect('user_login')
    else:
        ord = ol.objects.filter(uid=user_id)
        orr = []
        for order in ord:
            orr.append(o.objects.get(orderid=order.oid.orderid))
        paginator = Paginator(ord, 6)
        page = request.GET.get('page')
        orders = paginator.get_page(page)

        return render(request, 'user/orderhistory.html',{"orders":orders,'orr':order})

def update_password(request):
    user_id = request.session.get('uid')
    if not user_id:
        messages.error(request,'Login required')
        return redirect('user_login')
    else:
        data=u.objects.get(userid=user_id)
        op=data.password
        if request.method == 'POST':
            old_password=request.POST['old_password']
            new_password=request.POST['new_password']
            confirm_password=request.POST['confirm_password']
            if old_password == op:
                if new_password == confirm_password:    
                    u.objects.filter(userid=data.userid).update(password=new_password)
                    messages.success(request, 'Password Updated Successfully.')
                    return redirect('userprofile')
                else:
                    messages.error(request, 'Passsowrd must be same')
                    return redirect('userprofile')
            else:
                messages.error(request, 'Wrong Password')
                return redirect('userprofile')
        else:
            messages.error(request, 'Unexpected error occured.')
            return redirect('userprofile')

def update_email(request):
    user_id = request.session.get('uid')
    if not user_id:
        messages.error(request,'Login required')
        return redirect('user_login')
    else:
        data=u.objects.get(userid=user_id)
        if request.method == 'POST':
            new_email=request.POST['new_email']
            u.objects.filter(userid=data.userid).update(tempmail=new_email)
            secret=pyotp.random_base32()
            totp=pyotp.TOTP(secret,interval=300)
            otp=totp.now()
            recipient_list=data.tempmail
            send_mail('Bookies','Your one time password for bookies is '+str(otp)+'.OTP will expire within 5 minutes','bookiess.com@gmail.com', [recipient_list],fail_silently=True)
            response= redirect(f'email_verification/{data.userid}/{secret}')
            response.set_cookie("ca_otp_enter",True,max_age=500)
            return response
            # messages.success(request, 'E-mail Updated Successfully')
            # return redirect('userprofile')
        else:
            messages.error(request, 'Unexpected error occured.')
            return redirect('userprofile')
        
def email_verification(request,userid,secret):
    if request.POST:
        totp=pyotp.TOTP(secret,interval=300)
        try:
            user=u.objects.get(userid=userid)
        except u.DoesNotExist:
            messages.error(request,'Login Required')
            return redirect('user_login')
        code=request.POST['1']+request.POST['2']+request.POST['3']+request.POST['4']+request.POST['5']+request.POST['6']
        if request.COOKIES.get('ca_otp_enter')!=None:
            if (totp.verify(code)):
                if (user.tempmail):
                    user.email = user.tempmail
                    user.save()
                    response=redirect('userprofile')
                    response.set_cookie('verified',True)
                    messages.success(request,'Email Updation Successfull.')
                    return response
                else:
                    messages.error(request,'wrong otp')
                    return render(request,'user/otp.html')
            else:
                messages.error(request,'something went wrong')
                return render(request,'user/otp.html')
        else:
            messages.error(request,'OTP expired')
            return render(request,'user/otp.html')
    else:
        return render(request,'user/otp.html')

def paypal(request):
    user_id = request.session.get('uid')
    data = u.objects.get(userid = user_id)
    cart = car.objects.get(uid = data.userid)


    if not user_id:
        return redirect('user_login')
    else:
        order_id = randint(1000,9999)
        order_lid = randint(1000,9999)
        items = cl.objects.filter(ctid = cart.cartid)
        address = a.objects.filter(uid = user_id).first()
        order = o.objects.create(order_id = order_id, amount=cart.total, aid = address)
        datas = o.objects.get(order_id=order_id)
        date = datetime.now().date()
        pay.objects.create(oid=datas, mode = 'PayPal')
        for item in items:
            datap=item.pid
            dataq=item.quantity
            dataa=item.total_price
            ol.objects.create(oid=order,uid = cart.uid, pid=datap, quantity=dataq, total_price=dataa,order_date = date, order_lid=order_lid)
        items.delete()
        return render(request, 'user/ordersuccessfull.html')

def return_order(request):
    olid = request.GET['olid']
    ol.objects.filter(orderlistid=olid).update(return_order = True, status = 'Return Initiated')
    return redirect('order_history')



def invoice(request):

    order_id=request.GET['oid']
    data=o.objects.get(orderid=order_id)
    items=ol.objects.filter(oid=data).all()
    template = get_template('user/invoice.html')
    context = {'data':data,'items':items}
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Invoice.pdf"'

    pdf = pisa.CreatePDF(html, response)
    if not pdf.err:
        return response
    return HttpResponse('Error generating PDF: %s' % pdf.err, status=500)

# def delete_address(request):
#     aid = request.GET['aid']
#     a.objects.filter(addressid = aid).delete()
#     messages.warning(request,'Address deleted')
#     return render(request, 'user/userprofile.html')

# //-- Admin Functions --//
    
def admin_home(request):
    if 'mail' in request.session:
        orders_months=ol.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count('orderlistid')).values('month','count')
        months=[]
        total_orders=[]
        for i in orders_months:
            months.append(calendar.month_name[i['month']])
            total_orders.append(i['count'])
        order=ol.objects.order_by('order_date')[:2]
        context={
            'total_orders':total_orders,
            'months':months,
            'order':order,
        }
        return render(request,'admin/adminhome.html',{'context':context})
    
    else:
        return redirect('admin_login')
    
def salesreport(request):
    if request.POST:
        fromdate = request.POST['fromdate']
        fromdt = datetime.strptime(fromdate, '%Y-%m-%d').date()
        todate = request.POST['todate']
        todt = datetime.strptime(todate, '%Y-%m-%d').date()
        currentdate = datetime.today().date()
        if (currentdate >= fromdt) and (currentdate >= todt) and (fromdt < todt):
            if 'pdf' in request.POST:
                data = ol.objects.filter(order_date__range=[fromdate, todate])
                print(data)
                template_path = 'admin/report.html'
                context = {'data': data,
                           'fromdate': fromdate, 'todate': todate}
                # Create a Django response object, and specify content_type as pdf
                response = HttpResponse(content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="salesreport.pdf"'
                # find the template and render it.
                template = get_template(template_path)
                html = template.render(context)

                # create a pdf
                pisa_status = pisa.CreatePDF(
                    html, dest=response)
                # if error then show some funny view
                if pisa_status.err:
                    return HttpResponse('We had some errors <pre>' + html + '</pre>')
                return response
            elif 'excel' in request.POST:
                orders = ol.objects.filter(order_date__range=[fromdt, todt]).order_by('order_date')
                response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
                response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
                wb = openpyxl.Workbook()
                ws = wb.active
                ws.append(['Order Id', 'User' , 'Order Status' , 'Order Total' , 'Order Date',])
                for order in orders:
                    date = order.order_date.astimezone(pytz.utc).replace(tzinfo=None)
                    ws.append([order.order_lid,order.uid.email,order.status, order.total_price,date,])
                file_name = "sales_report.xlsx"
                wb.save(file_name)
                with open(file_name, "rb") as f:
                    response = HttpResponse(f.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                    response["Content-Disposition"] = f"attachment; filename={file_name}"
                    return response

            else:
                messages.error(request, 'Invalid request detected')
                return redirect('admin_home')
        else:
            messages.warning(request, 'Please provide the date in a valid format')
            return redirect('admin_home')
    else:
        return redirect('admin_home')

@never_cache
def admin_login(request):
    if 'mail' in request.session:
        return redirect('admin_home')
    if request.method == 'POST':
        mail = request.POST['mail']
        password = request.POST['password']
        ad=admin.objects.filter(mail=mail,password=password).count()
        if ad==1 :
            adminok=admin.objects.get(mail=mail,password=password)
            request.session['mail']=adminok.mail
            return redirect('admin_home')
        else:
            messages.error(request,'Invalid Username/Password')
            return redirect('/admin_login')
    else:
        return render(request,"admin/adminlogin.html")
    
@never_cache
def user_management(request):
    if 'mail' in request.session:
        if 'search' in request.GET:
            search=request.GET['search']
            users=u.objects.filter(email__icontains=search)
            paginator = Paginator(users, 5)
            page = request.GET.get('page')
            details = paginator.get_page(page)
            return render(request,'admin/usermanagement.html',{'details': details,'keyword':search})
        else:
            use=u.objects.all()
            paginator = Paginator(use, 5)
            page = request.GET.get('page')
            details = paginator.get_page(page)
            return render(request,'admin/usermanagement.html',{'details': details})
    else:
        return render(request,'admin/adminlogin.html')
    
def block_user(request):
    uid=request.GET["uid"]
    u.objects.filter(userid=uid).update(status = 'Blocked')
    return redirect("user_management")

def unblock_user(request):
    uid=request.GET['uid']
    u.objects.filter(userid=uid).update(status = "Active")
    return redirect("user_management")

def delete_user(request):

    uid=request.GET["uid"]
    u.objects.filter(userid=uid).delete()
    return redirect("user_management")

@never_cache
def product_management(request):
    if 'mail' in request.session:
        if 'search' in request.GET:
            search=request.GET['search']
            prods=p.objects.filter(pname__icontains=search)
            paginator = Paginator(prods, 3)
            page = request.GET.get('page')
            details = paginator.get_page(page)
            return render(request,'admin/productmanage.html',{'details': details, 'keyword': search})
        else:
            prods=p.objects.all()
            paginator = Paginator(prods, 3)
            page = request.GET.get('page')
            details = paginator.get_page(page)
            return render(request,'admin/productmanage.html',{'details': details})
    else:
        return render(request,'admin/adminlogin.html')

def delete_product(request):

    pid=request.GET["pid"]
    p.objects.filter(productid=pid).delete()
    return redirect("product_management")

def update_product(request):
    if 'mail' in request.session:
        pid=request.GET["pid"]
        data=p.objects.get(productid=pid)
        cat=c.objects.all()
        if request.method == 'POST':
            product_form = ProductForm(request.POST, request.FILES, instance = data)
            if product_form.is_valid():
                product_form.save()
                return redirect('product_management')
            else:
                messages.error(request, 'Something Went Wrong')
                return redirect('product_management')
               
        else:
            product_form = ProductForm(instance = data)
            return render(request, 'admin/updateproduct.html',{'form': product_form, 'productid': pid})

    else:
        return redirect('admin_login')
    
def addproduct(request):
    product_form = ProductForm()
    if request.method == 'POST':
        product_form = ProductForm(request.POST or None, request.FILES )
        main_image=request.POST.get('image')
        if product_form.is_valid():
            name = product_form.cleaned_data['pname']
            category = product_form.cleaned_data['cid']
            main_image = product_form.cleaned_data['image']
            description = product_form.cleaned_data['description']
            price = product_form.cleaned_data['price']
            stock = product_form.cleaned_data['stock']
            author = product_form.cleaned_data['author']
            publisher = product_form.cleaned_data['publisher']
            p.objects.create(pname=name, cid=category, image=main_image, description=description, price=price, stock=stock,author=author,publisher=publisher)
            messages.success(request, "Product Added Successfully")
            return redirect('product_management')
        else:
            messages.error(request,"Something went wrong!")


    context ={
        'form': product_form,
    }

    return render(request,"admin/addproduct.html", context)

@never_cache
def category_management(request):
    if 'mail' in request.session:
        if 'search' in request.GET:
            search=request.GET['search']
            items=c.objects.filter(cname__icontains=search)
            paginator = Paginator(items, 5)
            page = request.GET.get('page')
            cat = paginator.get_page(page)
            return render(request,'admin/categorymanage.html',{'cat': cat, 'keyword': search})
        else:
            items=c.objects.all()
            paginator = Paginator(items, 5)
            page = request.GET.get('page')
            cat = paginator.get_page(page)
            return render(request,'admin/categorymanage.html',{'cat': cat})
    else:
        return redirect('admin_login')
    
def add_category(request):
    if 'mail' in request.session:
        return render(request,"admin/addcategtory.html")
    else:
        return redirect('admin_login')

def addcategory(request):
    if 'mail' in request.session:
        if request.method=='POST':
            add_cname=request.POST.get("add_cname")
            cat = c.objects.filter(categoryname=add_cname).count()
            if cat > 0:
                messages.error(request, "Category already exist")
                return redirect('category_management')
            else:
                i=c()
                i.cname=add_cname
                i.save()

                return redirect('category_management')
        else:
                messages.error(request, "Something went wrong. Try again later")
                return redirect('category_management')

    else:
        return render(request,'admin/admin_login.html')

def delete_category(request):
    cid=request.GET["cid"]
    c.objects.filter(categoryid=cid).delete()
    return redirect("category_management")

def update_category(request):
    if 'mail' in request.session:
        cid=request.GET["cid"]
        cat=c.objects.get(categoryid=cid)
        return render(request,"admin/updatecategory.html",{'cat':cat})
    else:
        return redirect('admin_login')
    
def updatecategory(request):

    ucid=request.POST['ucid']
    add_cname=request.POST["add_cname"]
    c.objects.filter(categoryid=ucid).update(cname=add_cname)
    messages.success(request, 'Updated!!!')
    return redirect('category_management')

@never_cache
def admin_logout(request):
    if 'mail' in request.session:
        del request.session['mail']
        return redirect('admin_login')
    else:
        return redirect('admin_login')
    
def order_management(request):
    if 'mail' in request.session:
        if 'search' in request.GET:
            search=request.GET['search']
            orders=ol.objects.filter(order_lid__contains=search)
            paginator = Paginator(orders, 5)
            page = request.GET.get('page')
            order = paginator.get_page(page)
            return render(request,'admin/ordermanagement.html',{'orders': order, 'keyword': search})
        else:
            orders=ol.objects.all()
            paginator = Paginator(orders, 5)
            page = request.GET.get('page')
            order = paginator.get_page(page)
            return render(request,'admin/ordermanagement.html',{'orders': order})
    else:
        return redirect('admin_login')


# Admin Side
def order_details(request):
    orid = request.GET['orid']
    orr = o.objects.filter(orderid=orid)
    o_li = ol.objects.filter(oid=orid)
    return render(request,'admin/orderview.html', {"o_li":o_li , 'orr':orr})




def status(request):

    if request.method == 'POST':
        request_body = request.body.decode('utf-8')
        data = json.loads(request_body)
        orrid = data['orderlistid']
        sta =  data['status']
        ol.objects.filter(orderlistid = orrid).update(status = sta )
        dat = ol.objects.get(orderlistid = orrid)
        return JsonResponse({'status': dat.status})




def banner_management(request):
    if 'search' in request.GET:
            search = request.GET['search']
            ban = banner.objects.filter(name__contains=search)
            return render(request,'admin/bannermanagement.html',{'ban': ban, 'keyword': search})
    else:
        ban = banner.objects.all()
        return render(request,'admin/bannermanagement.html',{'ban':ban})



def add_banner(request):
    form = AddBanner(request.POST or None,request.FILES )
    if request.method == 'POST':
        if form.is_valid():
            form.save()

            return redirect('banner_management')
    return render(request,'admin/addbanner.html',{'form':form})


def delete_banner(request):
    banner_id = request.GET['banner_id']
    print(banner_id)
    banner.objects.filter(bannerid=banner_id).delete()
    return redirect ('banner_management')

def coupon_management(request):
    if 'mail' in request.session:
        coup = coupon.objects.all()
        return render(request, 'admin/coupon.html',{'coup': coup})
    else:
        return render(request, 'admin/adminlogin.html')

def addcoupon(request):
        if 'mail' in request.session:
            if request.method=='POST':
                add_coupname=request.POST.get("add_coupname")
                add_price=request.POST.get("add_price")
                coupon.objects.create(coupname = add_coupname,price = add_price)
                return redirect('coupon_management')
            else:
                return render(request,'admin/admin_login.html')
        else:
            return redirect('login')

def delete_coupon(request):
    coupon_id = request.GET['coupid']
    coupon.objects.filter(couponid=coupon_id).delete()
    return redirect ('coupon_management')

def product_offer(request):
    if request.POST:
        pid = request.POST['pid']
        offer = request.POST['offer']
        pro = p.objects.get(productid = pid)
        price = pro.price
        disc = int(price)*int(offer)/100
        offerprice = int(price)-int(disc)
        p.objects.filter(productid = pid).update(offer = offer , offerprice = offerprice)
        return redirect('product_management')
    else:
        messages.error(request,'Something Went Wrong')
        return redirect('product_management')
    
def category_offer(request):
    if request.POST:
        cid = request.POST['cid']
        offer = request.POST['offer']
        c.objects.filter(categoryid = cid).update(offer = offer)
        pros = p.objects.filter(cid = cid)
        for pro in pros:
            print (pro)
            datap = pro.productid
            datac = pro.cid.offer
            datapr = pro.price
            datao = int (datapr)-(int(datapr)*int(datac)/100)
            p.objects.filter(productid = datap).update(offerprice = datao, offer = offer)
            print(datapr)
            print(datao)
            print(datac)
        return redirect('category_management')
    else:
         messages.error(request,'Something Went Wrong')
         return redirect('category_management')






