from django import forms

from .models import PartnerCampaign


class PartnerCampaignCreateForm(forms.ModelForm):
    class Meta:
        model = PartnerCampaign
        fields = [
            'name',
            'email',
            'url',
        ]


class PartnerCampaignLookupForm(forms.Form):
    slug = forms.CharField()
    email = forms.CharField()
