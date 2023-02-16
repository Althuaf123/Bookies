from django import forms
from django.forms import ModelForm
from .models import product,banner


class ProductForm(forms.ModelForm):
    image = forms.FileField()
    class Meta:
        model = product
        fields = ['pname','cid','image','description','stock','price','publisher','author']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'required': True})
        }
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class AddBanner(forms.ModelForm):


    image = forms.ImageField(label=('Image'),required=False, error_messages={'invalid':('image field only')},widget=forms.FileInput(attrs={'class':'form-control'}))
    class Meta:
        model = banner
        fields = ('name','image')
        widgets = {
            'image':forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(AddBanner, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'