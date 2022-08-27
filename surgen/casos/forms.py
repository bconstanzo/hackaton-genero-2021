from django import forms
from django.forms import ModelForm
from .models import Domicilio, Nota, Victima, Provincias
from .models import Contacto


class PerfilForm(ModelForm):
	class Meta:
		model = Victima
		fields = ('email', 'telefono')
		labels = {
			'email': '',
			'telefono': '',	
		}
		widgets = {
			'email': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Mail'}),
			'telefono': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Telefono'}),
		}


class DomicilioForm(ModelForm):
	
	provincia= forms.CharField(label='Provincia', widget=forms.Select(choices=Provincias.choices))
	class Meta:
		model = Domicilio
		fields = ('calle', 'altura', 'piso_depto', 'codigo_postal', 'localidad', 'provincia')
		labels = {
			'calle' :'',
			'altura':'', 
			'piso_depto':'', 
			'codigo_postal':'',
			'localidad':'',
			'provincia':'',
		}
		widgets = {
			'calle': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Calle'}),
			'altura': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Altura'}),
			'piso_depto': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Piso-Departamento'}),
			'codigo_postal': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Codigo postal'}),
			'localidad': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Localidad'}),
		}


class ContactoForm(ModelForm):
	class Meta:
		model = Contacto
		fields = ('nombre', 'email', 'telefono')
		labels = {
			'nombre': '',
            'email': '',
			'telefono': '',
				
		}
		widgets = {
			'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}),
            'email': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Mail'}),
			'telefono': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Telefono'}),
		}

class DateInput(forms.DateInput):
	input_type = 'date'
	date_effet = forms.DateField(widget=forms.DateInput(format='%Y-%m-%d'), label='Date effet')

class NotaForm(ModelForm):
	class Meta:
		model = Nota
		fields = ('fecha', 'descripcion')
		labels = {
			'fecha': '',
			'descripcion': '',	
		}
		widgets = {
			'fecha': forms.DateInput(
				format=('%Y-%m-%d'),
				attrs={'class': 'form-control', 
				'placeholder': 'Fecha',
				'type': 'date'
				}),
			'descripcion': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nota'}),
		}

