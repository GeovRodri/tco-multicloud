import requests
from django.shortcuts import render
from django.views.generic import FormView
from website.forms import PesquisaForm


class Pesquisa(FormView):
    template_name = 'index.html'
    form_class = PesquisaForm

    def form_valid(self, form):
        data = form.data

        request_body = {
            "select": {
                'alibaba': ['CPU', 'SSD Cloud Disk', 'pricing.price', 'Memory'],
                'aws': ['vcpu', 'storage', 'pricing.', 'memory'],
                'azure': ['vCPU', 'Temporary storage', 'pricing.Pay as you go', 'RAM'],
                'google': ['Virtual CPUs', 'null', 'pricing.Price (USD)', 'Memory']
            },
            "labels": ['cpu', 'hd', 'pricing', 'ram'],
            "filters": [],
            "limit": data['limit']
        }

        if data['cpu'] is not None and data['cpu'] != '':
            request_body['filters'].append(
                {"field": "cpu", "comparator": data['cpu_filter'], "value": data['cpu']}
            )

        if data['hd'] is not None and data['hd'] != '':
            request_body['filters'].append(
                {"field": "hd", "comparator": data['hd_filter'], "value": data['hd']}
            )

        if data['ram'] is not None and data['ram'] != '':
            request_body['filters'].append(
                {"field": "ram", "comparator": data['ram_filter'], "value": data['ram']}
            )

        request = requests.post('http://157.230.128.104:8080/', json=request_body)
        print(request.json())
        return render(self.request, 'listagem.html', {'machines': request.json()})
