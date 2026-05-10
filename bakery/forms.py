from django import forms


class CustomerDetailsForm(forms.Form):
    name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={'placeholder': 'Your name'}),
    )
    phone_no = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': 'Phone number'}),
    )
    delivery_option = forms.ChoiceField(
        choices=[('no', 'No'), ('yes', 'Yes')],
        widget=forms.RadioSelect,
        label='Do you want home delivery?',
    )
    address = forms.CharField(
        max_length=70,
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Address', 'rows': 3}),
    )
