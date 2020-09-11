from django import forms


class GetCode(forms.Form):
    code = forms.CharField(widget=forms.Textarea, label="Code")
    stdin = forms.CharField(widget=forms.Textarea, required=False, label="Input for program")
    language = forms.ChoiceField(choices=(("python3", "python3"), ("c", "c")))
