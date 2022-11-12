from django import forms
from django.forms import ModelForm
from .models import Concurrencia, Domicilio, Victima, Provincias, Caso, Documento, Contacto, Incidencia


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


class ConcurrenciaForm(ModelForm):
	class Meta:
		model = Concurrencia
		fields = ('lugar_concurrido', 'descripcion')
		labels = {
			'lugar_concurrido': '',
			'descripcion': '',	
		}
		widgets = {
			'lugar_concurrido': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Lugar concurrido'}),
			'descripcion': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nota'}),
		}
class IncidenciaForm(ModelForm):
	class Meta:
		model = Incidencia
		fields = ('fecha', 'nombre', 'descripcion')
		labels = {
			'fecha': '',
			'nombre': '',	
			'descripcion': '',
		}
		widgets = {
			'fecha': forms.DateInput(attrs={'class':'form-control', 'placeholder':'Fecha'}),
			'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}),
			'descripcion': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Descripcion'}),
		}


class AgresorForm(ModelForm): #En realidad son dos datos del caso que refieren al agresor
	class Meta:
		HIJOS_CHOICES =(
		("NC","NC"),
		("SI","SI"),
		("NO","NO"),
		)
		RELACIONES_CHOICES = (
			("FAMILIAR", "FAMILIAR"),
			("PAREJA", "PAREJA"),
			("EX_PAREJA", "EX_PAREJA"),
			("FAMILIAR_PAREJA", "FAMILIAR_PAREJA"),
			("FAMILIAR_EX_PAREJA", "FAMILIAR_EX_PAREJA"),
			("JEFE", "JEFE"),
			("VECINO", "VECINO"),
			("PROFESOR", "PROFESOR"),
			("PROPIETARIO", "PROPIETARIO"),
			("COMPAÑERO", "COMPAÑERO"),
			("AMIGO", "AMIGO"),
			("OTRO", "OTRO"),
		)
		model = Caso
		fields = ('relacion', 'hijos_en_comun') #+domicilio.
		labels = {
			'relacion': '',
			'hijos_en_comun': '',	
		}
		widgets = {
			'relacion': forms.Select(choices = RELACIONES_CHOICES ,attrs={'class':'form-control', 'placeholder':'Relacion'}),
			'hijos_en_comun': forms.Select(attrs={'class':'form-control', 'choices' : HIJOS_CHOICES, 'placeholder':'Hijos en Común'}),
		}

    
    


