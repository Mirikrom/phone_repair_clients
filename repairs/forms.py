from django import forms
from .models import RepairOrder


class RepairOrderForm(forms.ModelForm):
    """Buyurtma qo'shish formasi - faqat telefon modeli majburiy"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client_phone'].required = False
        if self.instance and self.instance.pk and self.instance.client_phone:
            phone = self.instance.client_phone
            if phone.startswith('+998'):
                self.initial['client_phone'] = phone[4:].lstrip()
    
    def clean_client_phone(self):
        value = self.cleaned_data.get('client_phone', '').strip()
        if value:
            digits = ''.join(c for c in value if c.isdigit())
            if digits:
                return '+998' + digits
        return value
    
    class Meta:
        model = RepairOrder
        fields = [
            'phone_model',
            'client_name',
            'client_phone',
            'required_parts',
            'zapchast_olib_kelish_kerak',
            'repair_cost',
            'deposit_amount',
            'screen_type',
            'laminat',
            'ready_deadline',
            'ready_deadline_uncertain',
            'notes',
            'remind_at'
        ]
        widgets = {
            'phone_model': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'client_name': forms.TextInput(attrs={'class': 'form-control'}),
            'client_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'required_parts': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
            'zapchast_olib_kelish_kerak': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'repair_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'deposit_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'screen_type': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'laminat': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'ready_deadline': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'ready_deadline_uncertain': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'remind_at': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
        labels = {
            'phone_model': 'Telefon modeli *',
            'client_name': 'Mijoz ismi',
            'client_phone': 'Klent telefon raqami',
            'required_parts': 'Qo\'yilish kerak bo\'lgan zapchast',
            'zapchast_olib_kelish_kerak': 'Zapchast olib kelish kerak',
            'repair_cost': 'Tuzalish narxi (so\'m)',
            'deposit_amount': 'Zaklad summasi (so\'m)',
            'screen_type': 'Ekran turi',
            'laminat': 'Laminat',
            'ready_deadline': 'Tayyor bo\'lish muddati',
            'ready_deadline_uncertain': 'Hali tuzattirishi aniq emas',
            'notes': 'Qo\'shimcha eslatmalar',
            'remind_at': 'Eslatish (sana/vaqt)',
        }
