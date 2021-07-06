from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import logging
from .parsers import *
from .constants import SITE_LIST
from threading import Thread

logger = logging.getLogger(__name__)


class ProductListView(APIView):
    def get(self, request):
        search = request.GET.get('search')
        address = request.GET.get('address')
        if search is None or address is None:
            return Response({"Введите запрос для поиска в формате address/?search=[запрос]&address=[адрес]"})
        result = ProductListView.parse(search, address)
        return Response({
            "data": {
                "Утконос": {
                    "Лук репчатый 400 г": "200 Р",
                    "Лук зеленый 200 г": "180 Р",
                    "Лук порей": "100 Р",
                    "Чипсы Lay's с луком": "110 Р",
                    "Чипсы Pringle's со сметаной и ": "200 Р",
                    "Лук репчатый 40 г": "200 Р",
                    "Лук зеленый 20 г": "180 Р",
                    "Лук поре": "100 Р",
                    "Чипсы Lays с луком": "110 Р",
                    "Чипсы Pringle's со сметаной и луком": "200 Р",

                }
            }
        })

    @staticmethod
    def parse(search, address):
        result = {}
        threads = []
        for i in range(len(SITE_LIST)):
            req = f"{SITE_LIST[i]}{search}"
            page = requests.get(req)
            if "vprok.ru" in req:
                threads.append(Thread(target=PerekrestokParser.parse_perekrestok, args=(req, address, result)))
            elif "utkonos.ru" in req:
                threads.append(Thread(target=UtkonosParser.parse_utkonos, args=(page, result)))
            elif "lavka.yandex.ru" in req:
                threads.append(Thread(target=LavkaParser.parse_lavka, args=(req, address, result)))
            elif "delivery.metro-cc.ru/" in f"{req}":
                threads.append(Thread(target=MetroParser.parse_metro, args=(req, address, result)))
            threads[i].start()

        for thread in threads:
            thread.join()

        return result


def index(request):
    return render(
        request,
        'index.html',
    )

