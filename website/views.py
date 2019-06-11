import requests
from django.shortcuts import render
from django.views.generic import FormView
from website.forms import PesquisaForm
from website.sparql_query import SparqlQuery


class Pesquisa(FormView):
    template_name = 'index.html'
    form_class = PesquisaForm

    def form_valid(self, form):
        data = form.data
        sparql_query = SparqlQuery()
        ontology = sparql_query.search()

        request_body = {
            "select": ontology,
            "labels": ['cpu', 'hd', 'pricing', 'ram'],
            "filters": [],
            "limit": data['limit']
        }

        if data['cpu'] is not None and data['cpu'] != '':
            request_body['filters'].append(
                {"field": "cpu", "comparator": data['cpu_filter'], "value": int(data['cpu'])}
            )

        if data['hd'] is not None and data['hd'] != '':
            request_body['filters'].append(
                {"field": "hd", "comparator": data['hd_filter'], "value": int(data['hd'])}
            )

        if data['ram'] is not None and data['ram'] != '':
            request_body['filters'].append(
                {"field": "ram", "comparator": data['ram_filter'], "value": int(data['ram'])}
            )

        request = requests.post('http://157.230.128.104:8080/', json=request_body)
        machines = request.json()

        ''' Adicionar o item que corresponde a maquina fisica '''
        machines.append(
            {
                'type': 'Maquina Física',
                'cloud': 'Maquina Física',
                'cpu': 3,
                'hd': '2 TB',
                'ram': '2 GB',
                'pricing': {
                    'region': 'Goiania',
                    'price': 0.002669
                }
            }
        )

        return render(self.request, 'listagem.html', {'machines': machines})
