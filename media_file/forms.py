from django import forms
from .models import PostMedia

class PostMediaForm(forms.ModelForm):
    class Meta:
        model = PostMedia
        fields = ['video', 'image', 'stickers']
