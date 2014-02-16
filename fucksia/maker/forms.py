#Django imports
from django import forms
from django.forms import ModelForm

# Project imports
from fucksia.maker.models import Estudiante


class URLForm(forms.Form):
    materias_inscritas_URL = forms.URLField(
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'No, si no estas inscrito.'})
    )
    record_academico_URL = forms.URLField()
    horarios_URL = forms.URLField()


class EstudianteForm(ModelForm):
    nombre = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Nombre de Usuario'}))
    email = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Correo electronico'}))
    cod_estudiante = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'readonly':'readonly',
            'class':'form-control',
            'placeholder':'Codigo de estudiante'}))

    class Meta:
        model = Estudiante
        exclude = ('uid', 'avatar','social_network', 'is_config',)


class PensumForm(forms.Form):
    pensum_URL = forms.URLField()
