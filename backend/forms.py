from django.forms import ModelForm
from .models import Congratulation


class ProphetForm(ModelForm):
    class Meta:
        model = Congratulation
        fields = ['number']
        labels = {
            'number': ''
        }