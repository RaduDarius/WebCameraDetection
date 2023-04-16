from django import forms

class HomeForm(forms.Form):
    alarmActive = forms.BooleanField(label="AlarmOn", required=False)