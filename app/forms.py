from django.forms import ModelForm
from .models import MediaBuying

class MediaBuyingForm(ModelForm):
    class Meta:
        model = MediaBuying
        fields = '__all__'