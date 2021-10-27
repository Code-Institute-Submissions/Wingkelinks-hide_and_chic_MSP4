from django import forms
from .widgets import CustomClearableFileInput
from .models import Product, Category, ProductReview


class ProductForm(forms.ModelForm):
    """
    A form for product management by admin. 
    """

    class Meta:
        model = Product
        fields = '__all__'

    # Replace image field with field using widget
    image = forms.ImageField(label='Image', required=False, widget=CustomClearableFileInput)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'rounded'
            

class ReviewForm(forms.ModelForm):
    """
    A form for sumbitting product reviews and ratings. 
    """
    
    class Meta:
        model = ProductReview
        exclude = ('product', 'user', 'created')
