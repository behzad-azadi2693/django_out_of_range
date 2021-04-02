from django import forms

class PhoneLoginForm(forms.Form):
    number = forms.CharField(max_length=11, widget=forms.TextInput(attrs=({'class':'form-control'}))

    def clean_number(self):
        number = Profile.objects.filter(phoe=self.cleaned_data['number'])
        if not number.exists():
            raise forms.ValidationError('this phone number dose not exists')
        return self.cleaned_data['number']
        

class VerifyForm(forms.Form):
    code = forms.CharField(max_length=11, widget=forms.TextInput(attrs=({'class':'form-control'}))

