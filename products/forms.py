from django import forms


class ProductCreateForm(forms.Form):
    title = forms.CharField(min_length=8)
    description = forms.CharField(widget=forms.Textarea())
    price = forms.IntegerField()
    review_table = forms.BooleanField(widget=forms.CheckboxInput(attrs={'checked': True}))


class ReviewCreateForm(forms.Form):
    text = forms.CharField(min_length=3, label='Review')
