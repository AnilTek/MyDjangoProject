from django import forms

class CarForm (forms.Form):
    model = forms.CharField(max_length=30)
    year = forms.IntegerField(label='Year',min_value=1930,max_value=2023)
    millage = forms.IntegerField(label='millage',min_value=0,max_value=1500000)
    tax = forms.IntegerField(label='tax',min_value=0,max_value=100000)
    mpg = forms.IntegerField(label='mpg',min_value=1,max_value=250)
    engineSize = forms.FloatField(label='engineSize',min_value=1,max_value=8)

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year is not None and not (1930 <= year <= 2023):
            raise forms.ValidationError("Please enter a value between 1930 and 2023 for Year.")
        return year

    def clean_millage(self):
        millage = self.cleaned_data.get('millage')
        if millage is not None and not (0 <= millage <= 1500000):
            raise forms.ValidationError("Please enter a value between 0 and 1500000 for Millage.")
        return millage

    def clean_tax(self):
        tax = self.cleaned_data.get('tax')
        if tax is not None and not (0 <= tax <= 100000):
            raise forms.ValidationError("Please enter a value between 0 and 100000 for Tax.")
        return tax

    def clean_mpg(self):
        mpg = self.cleaned_data.get('mpg')
        if mpg is not None and not (1 <= mpg <= 250):
            raise forms.ValidationError("Please enter a value between 1 and 250 for MPG.")
        return mpg

    def clean_engineSize(self):
        engineSize = self.cleaned_data.get('engineSize')
        if engineSize is not None and not (1 <= engineSize <= 8):
            raise forms.ValidationError("Please enter a value between 1 and 8 for Engine Size.")
        return engineSize

class LoanForm(forms.Form):
    number_of_dependents= forms.IntegerField(label='number_of_dependents')
    anual_income= forms.IntegerField(label='anual_income')
    loan_ammount= forms.IntegerField(label='loan_ammount')
    loan_term= forms.IntegerField(label='loan_term')
    cibil_score= forms.IntegerField(label='cibil_score')
    residental_assets_value= forms.IntegerField(label='residental_assets_value')
    commercial_assets_value= forms.IntegerField(label='commercial_assets_value')
    luxury_assets_value= forms.IntegerField(label='luxury_assets_value')
    bank_asset_value= forms.IntegerField(label='bank_asset_value')


