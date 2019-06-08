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
            "limit": 5
        }

        request = requests.post('http://157.230.128.104:8080/', json=request_body)
        print(request.json())
        return render(self.request, 'listagem.html', {'machines': request.json()})
