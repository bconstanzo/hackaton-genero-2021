from django import forms
from django.forms import ModelForm
from .models import Victima
from .models import Contacto


class PerfilForm(ModelForm):
	class Meta:
		model = Victima
		fields = ('domicilio', 'email', 'telefono')
		labels = {
			'domicilio': '',
			'email': '',
			'telefono': '',	
		}
		widgets = {
			'domicilio': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Domicilio'}),
			'email': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Mail'}),
			'telefono': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Telefono'}),
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


