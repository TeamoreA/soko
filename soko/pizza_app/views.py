import random
import string
import inflect

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from soko.pizza_app import serializers
from soko.pizza_app import models

class OrderList(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        order_list = request.data.get("orders")

        if order_list:
            resp_list = []
            total = 0
            for order in order_list:
                # loop though the orders list and process them individually
                tp = 0
                order_details = order.split("-")
                pizza_size = order_details[0].strip()
                size = get_object_or_404(models.Size, size=pizza_size).pk
                pizza = get_object_or_404(models.Pizza, size=size)

                letters = string.ascii_letters
                # assign each order a unique id
                uid = "".join(random.choice(letters) for i in range(10))
                serializer = serializers.OrderSerializer(
                    data={"uid": uid, "buyer": request.user.pk, "pizza": pizza.pk})
                serializer.is_valid(raise_exception=True)
                order = models.Order.objects.create(
                    uid=uid, buyer=request.user, pizza=pizza)
                toppings = order_details[1].split(",")
                for topping in toppings:
                    # loop through the toppings of a specific pizza and compute their totals
                    tp_data = topping.strip()
                    topping_dt = get_object_or_404(models.Topping, name=tp_data)
                    order.topping.add(topping_dt)
                    cats = models.Category.objects.filter(topping__name=tp_data)
                    tp += int(cats.get(size=size).price)
                order_tot = int(pizza.price) + tp
                total += order_tot
                # format the individual output orders string and the subtotals
                p = inflect.engine()
                resp_list.append(
                    f'1 {pizza_size} , {p.number_to_words(len(toppings))} Topping Pizza - {order_details[1]}: KES {order_tot}')
            vat = round(0.16*total, 2)
            resp_list.extend([f'Subtotal: KES {total}', f'VAT: KES {vat}', f'Total: KES {int(total+vat)}'])
            return Response(
                data={'status': 'success', 'data':{'orders':resp_list, 'buyer':request.user.username, 'uid':uid}},
                status=201)
        return Response(data={"status": "error"}, status=400)
