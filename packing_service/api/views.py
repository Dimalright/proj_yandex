import csv
from random import choice

import requests
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from .utils.csv_utils import read_csv_file
from .utils.csv_utils1 import read_csv_file1
from .utils.parse_order_id import get_orderkey


class OrdersView(APIView):
    """
    Класс представления для получения информации о заказе.
    """

    file_path = 'data/data.csv'
    sku_file_path = 'data/sku.csv'
    sku_cargotypes_file_path = 'data/sku_cargotypes.csv'


    def get(self, request):
        """
        Метод GET для получения информации о заказе.
        """
        barcodes = request.GET.getlist('barcode')
        filtered_data = read_csv_file(
            self.file_path,
            self.sku_file_path,
            self.sku_cargotypes_file_path,
            choice(get_orderkey())
        )

        if filtered_data:
            return Response(filtered_data)
        else:
            return Response({'error': 'Заказ не найден'})

    def post(self, request):
        """
        Метод POST для получения информации о заказе с передачей баркодов.
        """
        order_number = request.data.get('orderkey')
        barcodes = request.data.get('barcodes')
        # print(order_number, barcodes)

        # Здесь можно обработать полученные баркоды и выполнить необходимую логику

        return Response({'message': 'POST-запрос успешно обработан.'})




class PackageView(APIView):
    def get(self, request, orderkey):
        order_list = list(csv.reader(open('data/data.csv')))
        sku_list = list(csv.reader(open('data/sku.csv')))
        cargotypes = list(csv.reader(open('data/sku_cargotypes.csv')))

        order = []
        sku = []

        flag = 0

        for el in order_list:
            if flag == 0:
                flag = 1
                continue
            if el[2] == orderkey:
                order.append(el)
                sku.append(el[12])

        count_weight_dict = dict()

        for el in sku:
            count_weight_dict[el] = {'count': 0}

        for el in order:
            count_weight_dict[el[12]]['count'] += 1
            count_weight_dict[el[12]]['weight'] = el[11]

        items_list = []

        for el in sku:
            temp_dict = {}
            for row in sku_list:
                if row[1] == el:
                    temp_dict['sku'] = el
                    temp_dict['size1'] = row[2]
                    temp_dict['size2'] = row[3]
                    temp_dict['size3'] = row[4]
                    temp_dict['type'] = []
            for row in cargotypes:
                if row[1] == el:
                    temp_dict.setdefault('type', []).append(row[2])
            temp_dict['count'] = count_weight_dict[el]['count']
            temp_dict['weight'] = count_weight_dict[el]['weight']
            items_list.append(temp_dict)

        request_dict = {
            'orderId': orderkey,
            'items': items_list
        }

        result = requests.get('http://localhost:8001/pack', json=request_dict)

        data = result.json()
        return JsonResponse(data)