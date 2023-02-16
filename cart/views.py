from django.shortcuts import render

# Create your views here.
from django.views import View
from django.shortcuts import render,redirect
from .models import user



# Create your views here.



class AddToCartView(View):
    def get(self, request):
        uid = request.session.get("uid")
        if not uid:
            return redirect("login")

        use = user.objects.filter(userid=uid).first()
        if not use:
            return redirect("login")

        pid = request.GET.get("pid")
        pro = product.objects.filter(productid=pid).first()
        if not pro:
            return redirect("home")
     
        car, created = cart.objects.get_or_create(uid=use)
        cart_item, created = cartlist.objects.get_or_create(pid=pro, ctid=car)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart_item.quantity = 1
            cart_item.save()

        return redirect("cart")


class CartView(View):
    def get(self, request):
        uid = request.session.get("uid")
        if not uid:
            return redirect("user_login")

        use = user.objects.filter(userid=uid).first()
        if not use:
            return redirect("user_signup")

        car = cart.objects.filter(uid=use).first()
        if not car:
            return redirect("homepage")

        cart_items = cartlist.objects.filter(ctid=car)
        context = {
            "cart_items": cart_items,
        }
        return render(request, "user/cart.html", context)

