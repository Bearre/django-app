from django import forms

class OfferForm(forms.Form):
    firstname = forms.CharField(initial="Имя",
                                required=True,
                                error_messages={'requierd':'Не введено имя'},
                                #widget=forms.TextInput(attrs={"class":"form-input"})
                                )
    lastname = forms.CharField()
    email = forms.EmailField()
