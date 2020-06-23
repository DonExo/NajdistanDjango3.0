from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Listing

help_texts = [
    _('Make sure you pick a meaningful title that will best describe your property. Title can NOT be updated later!'),
    _('Property title can NOT be updated.'),
    _('Add any images that you think might spark an interest in your potential buyers! Allowed formats: .JPG, .JPEG, .PNG.'),
    _('If property is for sell - type overall selling price. <br/> If property is for rent - type monthly rent cost.')
]


class ListingCreateForm(forms.ModelForm):
    title = forms.CharField(label='Property title', help_text=help_texts[0])
    images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), help_text=help_texts[2])
    price = forms.DecimalField(help_text=help_texts[3])

    class Meta:
        model = Listing
        exclude = ('user', 'slug', 'address', 'times_visited', 'soft_deleted', 'is_approved',
                   'is_available', 'rejection_reason', 'available_from', 'rental_period')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2, "cols": 15})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 10:
            raise forms.ValidationError("Add brief summary with at least 10 characters!")
        return title

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 15:
            raise forms.ValidationError("Add description for the property with at least 15 characters!")
        return description

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].empty_label = None


class ListingUpdateForm(ListingCreateForm):
    title = forms.CharField(label='Property title', help_text=help_texts[1], disabled=True)
    images = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'multiple': True}), help_text=help_texts[2])
