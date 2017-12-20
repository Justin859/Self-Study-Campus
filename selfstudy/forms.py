from django import forms

class SubmitEmailChat(forms.Form):
    client_email = forms.EmailField(max_length=255)
    client_name = forms.CharField(max_length=255)

class ChatSend(forms.Form):
    client_message = forms.CharField(max_length=255)