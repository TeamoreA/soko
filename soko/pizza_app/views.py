import random
import string
import inflect
from soko.pizza_app import models
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from soko.pizza_app import serializers
from helpers.renderers import DefaultRenderer

class OrderList(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        order_list = request.data.get("orders")

        if order_list:
            resp_list = []
            total = 0
            for order in order_list:
                tp = 0
                order_details = order.split("-")
                pizza_size = order_details[0].strip()
                size = models.Size.objects.get(size=pizza_size).pk
                pizza = models.Pizza.objects.get(size=size)

                letters = string.ascii_letters
                uid = "".join(random.choice(letters) for i in range(10))
                order = models.Order.objects.create(
                    uid=uid, buyer=request.user, pizza=pizza)
                toppings = order_details[1].split(",")
                for topping in toppings:
                    tp_data = topping.strip()
                    topping_dt = models.Topping.objects.get(name=tp_data)
                    order.topping.add(topping_dt)
                    cats = models.Category.objects.filter(topping__name=tp_data)
                    tp += int(cats.get(size=size).price)
                order_tot = int(pizza.price) + tp
                total += order_tot
                p = inflect.engine()
                resp_list.append(f'1 {pizza_size} , {p.number_to_words(len(toppings))} Topping Pizza - {order_details[1]}: KES {order_tot}')
                request_data = {"uid": uid, "buyer": request.user, "pizza": pizza.pk}
                serializer = serializers.OrderSerializer(data=request_data)
                serializer.is_valid(raise_exception=True)
            amounts = [f'Subtotal: KES {total}', f'VAT: KES {0.16*total}']
            resp_list.extend(amounts)
            resp = {'status': 'success', 'data':{'orders':resp_list, 'buyer':request.user.username, 'uid':uid}}
            return Response(data=resp, status=201)
        return Response(data={"status": "error"}, status=400)
