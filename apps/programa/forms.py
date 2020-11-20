from django import forms
from django.core.exceptions import ValidationError
from django.forms import DateInput

from .models import Programa, AsignacionBeneficio


class ProgramaForm(forms.ModelForm):
    class Meta:
        model = Programa
        fields = ('nombre', 'tipo_asistencias', 'requisitos', 'fecha_inicio', 'fecha_fin')

        widgets = {
            'requisitos': forms.ClearableFileInput(),
            'fecha_inicio': DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'fecha_fin': DateInput(format='%y-%m-%d', attrs={'type': 'date'})
        }

    def clean_requisitos(self):
        requisitos = self.cleaned_data['requisitos']
        if requisitos:
            extension = requisitos.name.rsplit('.', 1)[1].lower()
            if extension != 'pdf':
                raise ValidationError('El archivo seleccionado no tiene el formato PDF.')
        return requisitos

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = self.cleaned_data['fecha_inicio']
        fecha_fin = self.cleaned_data['fecha_fin']
        # Verifica que la fecha de inicio sea anterior a fecha fin.
        if fecha_fin and fecha_inicio > fecha_fin:
            raise ValidationError(
                {'fecha_inicio': 'La Fecha de Inicio no puede ser posterior que la fecha fin'},
                code='invalido'
            )
        return cleaned_data

class BeneficioForm(forms.ModelForm):
    class Meta:
        model = AsignacionBeneficio
        fields = '__all__'

    # Funcion para comprobar que la fecha de asignacion no sea mayor a la fecha actual
    def clean_fecha(self):

        fecha_entrega = self.cleaned_data.get('fecha_entrega')
        cantidad = self.cleaned_data.get('cantidad')
        
        if fecha_entrega > datetime.today:
            raise ValidationError('La fecha de asignacion no puede ser mayor a la fecha actual')

        return fecha_entrega

    # Funcion para comprobar que la cantidad no sea menor a 1
    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')

        if cantidad < 1:
            raise ValidationError('La cantidad no puede ser menor a 1')

        return cantidad