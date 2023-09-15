from django.forms import ModelForm
from .models import Feeding

# custom class inheriting from the ModelForm class
# (that gives us all the nice built in methods etc)
class FeedingForm(ModelForm):
    # a nested class Meta - declares the model and fields
    class Meta:
        model = Feeding
        fields = ['date', 'meal']