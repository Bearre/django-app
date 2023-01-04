from django.http import *
from django.shortcuts import render
from OFFER.forms import OfferForm

# Create your views here.

def index(request):
    data = {"header": "Параметр header",
            "message": "Сообщение"}
    return render(request, "index.html", context=data)


def offer(request):
    """ Страница с вводом данных """

    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        mobile_phone_number = request.POST.get("mobilephone")

        output =f"<h2>Пользователь</h2><h3>Имя - {firstname}, Фамилия - {lastname}</hЗ><h3> Email - {email}</hЗ>"
        return HttpResponse(output)
    else:
         offerform = OfferForm()
         return render(request, "offer.html", {"form": offerform})
