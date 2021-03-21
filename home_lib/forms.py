from django import forms
from .models import Book, Wishlist
from django.contrib import messages
from django.core.validators import RegexValidator


class BaseBookCreateForm(forms.ModelForm):
    class Meta:
        model = None
        fields = ['title', 'author', 'year', 'language']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter the title of the book'}),
            'author': forms.TextInput(attrs={'placeholder': 'Enter the author of the book'}),
            'year': forms.TextInput(attrs={'placeholder': 'Enter the year of publication'}),
        }

    def clean(self):

        # Don't allow insertion of duplicate books.
        try:
            if self.Meta.model.objects.filter(title__icontains=self.cleaned_data.get('title'),
                                   author__icontains=self.cleaned_data.get('author'),
                                   year__icontains=self.cleaned_data.get('year'),
                                   language__icontains=self.cleaned_data.get('language')).exists():
                # This error will not be shown in the form,
                # BookCreateView's form_invalid() method handles messages.
                raise forms.ValidationError('Book already exists', code='exists')
        except ValueError:
            pass
        return super().clean()


class BookCreateForm(BaseBookCreateForm):

    def __init__(self, *args, **kwargs):
        super(BookCreateForm, self).__init__(*args, **kwargs)

    class Meta(BaseBookCreateForm.Meta):
        model = Book
        fields = BaseBookCreateForm.Meta.fields


# class BookCreateForm(forms.ModelForm):
#
#     class Meta:
#         model = Book
#         fields = ['title', 'author', 'year', 'language']
#         widgets = {
#             'title': forms.TextInput(attrs={'placeholder': 'Enter the title of the book'}),
#             'author': forms.TextInput(attrs={'placeholder': 'Enter the author of the book'}),
#             'year': forms.TextInput(attrs={'placeholder': 'Enter the year of publication'}),
#         }
#
#     def clean(self):
#         # Don't allow insertion of duplicate books.
#         try:
#             if Book.objects.filter(title__icontains=self.cleaned_data.get('title'),
#                                    author__icontains=self.cleaned_data.get('author'),
#                                    year__icontains=self.cleaned_data.get('year'),
#                                    language__icontains=self.cleaned_data.get('language')).exists():
#                 # This error will not be shown in the form,
#                 # BookCreateView's form_invalid() method handles messages.
#                 raise forms.ValidationError('Book already exists', code='exists')
#         except ValueError as e:
#             raise forms.ValidationError(e)


class BookWishlistForm(BaseBookCreateForm):

    def __init__(self, *args, **kwargs):
        super(BookWishlistForm, self).__init__(*args, **kwargs)

    class Meta(BaseBookCreateForm.Meta):
        model = Wishlist
        fields = BaseBookCreateForm.Meta.fields


# class BookWishlistForm(forms.ModelForm):
#     class Meta:
#         model = Wishlist
#         fields = ['title', 'author', 'year', 'language']
#         widgets = {
#             'title': forms.TextInput(attrs={'placeholder': 'Enter the title of the book'}),
#             'author': forms.TextInput(attrs={'placeholder': 'Enter the author of the book'}),
#             'year': forms.TextInput(attrs={'placeholder': 'Enter the year of publication'}),
#         }
#
#
#     def clean(self):
#         # Don't allow insertion of duplicate books.
#         #if Wishlist.objects.filter(title=self.cleaned_data.get('title')).exists():
#         if Wishlist.objects.filter(title=self.cleaned_data.get('title'),
#                                    author=self.cleaned_data.get('author'),
#                                    year=self.cleaned_data.get('year'),
#                                    language=self.cleaned_data.get('language')).exists():
#
#             raise forms.ValidationError('This book already exists in the database!')


class BookSearchForm(BookCreateForm):
    def __init__(self, *args, **kwargs):
        super(BookSearchForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['author'].required = False
        self.fields['year'].required = False
        self.fields['language'].required = False

    def clean(self):
        pass


class BookMarkReadForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['read_timestamp']
        widgets = {
            'read_timestamp': forms.DateTimeInput(attrs={'class': 'input', 'type': 'date'})
        }


class BookIsbnForm(forms.Form):
    isbn13 = forms.CharField(max_length=13, min_length=13, validators=[RegexValidator(r'^\d{1,10}$')])