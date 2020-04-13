from django import forms

from .models import Listing


class ListingCreateForm(forms.ModelForm):

    class Meta:
        model = Listing
        fields = ('title', 'description', 'listing_type', 'home_type', 'city', 'zip_code', 'quadrature', 'rooms', 'bedrooms', 'floor', 'heating', 'price', 'cover_image')
        # @TODO: Add all necessary values

    def clean_title(self):
        title = self.cleaned_data['title']
        if title.startswith('a'):
            raise forms.ValidationError("Ne mojt so A da pocvit ;) ")
        return title


class ListingUpdateForm(ListingCreateForm):
    title = forms.CharField(disabled=True)


# class ImageUploadForm(forms.Form):
#     images = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    # def clean(self):
    #     print("clean()")
    #     super().clean()
    #     images = self.cleaned_data.get('images')
    #     print(images)
    #     # return
    #     return images

    # def clean_images(self):
    #     print("clean_images")
    #     files = self.files.getlist('images')
    #     import imghdr
    #     for file in files:
    #         print(imghdr.what(file.name))
    #         # print(file.name, type(file), dir(file))
    #
    #     # print(files)
    #     return files
