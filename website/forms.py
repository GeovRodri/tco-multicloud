from django import forms

FILTER_OPTIONS = (
    ('==', u'Igual'),
    ('>=', u'Maior ou Igual'),
    ('<=', u'Menor ou Igual'),
    ('!=', u'Diferente'),
)


class PesquisaForm(forms.Form):

    cpu_filter = forms.ChoiceField(
        label='CPU filtro',
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=FILTER_OPTIONS)

    cpu = forms.IntegerField(
        label='CPU (opcional)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPU'}),
        required=False)

    ram_filter = forms.ChoiceField(
        label='RAM filtro',
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=FILTER_OPTIONS)

    ram = forms.IntegerField(
        label='RAM (opcional)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RAM'}),
        required=False)

    hd_filter = forms.ChoiceField(
        label='HD filtro',
        widget=forms.Select(attrs={'class': 'form-control'}),
        choices=FILTER_OPTIONS)

    hd = forms.IntegerField(
        label='HD (opcional)',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'HD'}),
        required=False)
