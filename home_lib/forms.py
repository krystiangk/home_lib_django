from django import forms
from .models import Book, Wishlist


class BookCreateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'year', 'language']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter the title of the book', 'class': 'input'}),
            'author': forms.TextInput(attrs={'placeholder': 'Enter the author of the book', 'class': 'input'}),
            'year': forms.TextInput(attrs={'placeholder': 'Enter the year of publication', 'class': 'input'}),
        }

    def __init__(self, *args, **kwargs):
        super(BookCreateForm, self).__init__(*args, **kwargs)
        self.fields['language'].widget.attrs.update({'class': 'input'})

    def clean(self):
        # Don't allow insertion of duplicate books.
        # if Book.objects.filter(title__iexact=self.cleaned_data.get('title'),
        #                            author__iexact=self.cleaned_data.get('author'),
        #                            year__iexact=self.cleaned_data.get('year'),
        #                            language__iexact=self.cleaned_data.get('language')).exists():
        if Book.objects.filter(title__icontains=self.cleaned_data.get('title'),
                               author__icontains=self.cleaned_data.get('author'),
                               year__icontains=self.cleaned_data.get('year'),
                               language__icontains=self.cleaned_data.get('language')).exists():
            raise forms.ValidationError('This book already exists in the database!')


class BookSearchForm(BookCreateForm, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(BookSearchForm, self).__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['author'].required = False
        self.fields['year'].required = False
        self.fields['language'].required = False


class BookMarkReadForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['read_timestamp']
        widgets = {
            'read_timestamp': forms.DateTimeInput(attrs={'class': 'input', 'type': 'date'})
        }


class BookWishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['title', 'author', 'year', 'language']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter the title of the book', 'class': 'input'}),
            'author': forms.TextInput(attrs={'placeholder': 'Enter the author of the book', 'class': 'input'}),
            'year': forms.TextInput(attrs={'placeholder': 'Enter the year of publication', 'class': 'input'}),
        }

    def __init__(self, *args, **kwargs):
        super(BookWishlistForm, self).__init__(*args, **kwargs)
        self.fields['language'].widget.attrs.update({'class': 'input'})

    def clean(self):
        # Don't allow insertion of duplicate books.
        #if Wishlist.objects.filter(title=self.cleaned_data.get('title')).exists():
        if Wishlist.objects.filter(title=self.cleaned_data.get('title'),
                                   author=self.cleaned_data.get('author'),
                                   year=self.cleaned_data.get('year'),
                                   language=self.cleaned_data.get('language')).exists():

            raise forms.ValidationError('This book already exists in the database!')