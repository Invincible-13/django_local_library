import datetime
from django import forms
from .models import BookInstance
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# class RenewBookForm(forms.Form):
#     renewal_date = forms.DateField(help_text='Enter a date between now and 4 weeks (default 3).')

#     def clean_renewal_date(self):
#         data = self.cleaned_data['renewal_date']

#         if data < datetime.date.today() or data > datetime.date.today() + datetime.timedelta(weeks=4):
#             raise ValidationError(_('Invalid date'))

#         return data

class RenewBookModelForm(forms.ModelForm):
    def clean_due_back(self):
        data = self.cleaned_data['due_back']

        if data < datetime.date.today() or data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date'))

    class Meta:
        model = BookInstance
        #Override the defaults
        fields = ['due_back']
        labels = {'due_back' : _('New renewal date')}
        help_text = {'due_back' : _('Enter a date between now and 4 weeks')}

