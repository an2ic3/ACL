from django import forms
from .models import Service


class TicketForm(forms.Form):
    subject = forms.CharField(max_length=128, widget=forms.TextInput(attrs={
        'placeholder': 'Subject',
        'class': 'form-control',
    }), required=True)

    service = forms.ChoiceField(
        widget=forms.Select(attrs={
            'placeholder': 'Service',
            'class': 'form-control',
        }),
        choices=[(p.id, p.name) for p in Service.objects.all()],
        required=True
    )

    description = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Description',
        'class': 'form-control',
    }), required=True)

    priority = forms.ChoiceField(
        widget=forms.Select(attrs={
            'placeholder': 'Priority',
            'class': 'form-control',
        }),
        choices=[
            (1, "Low"),
            (2, "Normal"),
            (3, "High")
        ],
        required=True
    )

    discord_notifications = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        'disabled': True,
    }), required=False)
