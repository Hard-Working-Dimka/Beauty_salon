from django import forms

from Salons.models import Review


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['phone_number', 'description', 'name']

    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'contacts__form_iunput',
            'placeholder': 'Введите имя'
        })
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'contacts__form_iunput',
            'placeholder': '+7(999)999--99-99'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'contacts__form_textarea',
            'placeholder': 'Ваш вопрос (необязательно)'
        }),
        required=False
    )