from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from . import form_widget


class StrippedCharField(forms.CharField):
    """Newforms CharField that strips trailing and leading spaces."""
    def clean(self, value):
        if value is not None:
            value = value.strip()
        return super(StrippedCharField, self).clean(value)
     
     
class Logon(forms.Form):
    uid = StrippedCharField(max_length=10, min_length=2, help_text='enter your user id', label='User')
    pwd = StrippedCharField(max_length=10, min_length=4, help_text='enter your password', label='Password', widget=forms.PasswordInput())
    
class Registration(forms.Form):
    attrs = {"pattern":"[a-z]+"}
    uid = StrippedCharField(validators=[RegexValidator(regex='^[a-z]+$',message='Smallcase without space are allowed'),], 
                          max_length=10, min_length=4, widget=form_widget.get_text_widget(attrs), 
                          help_text='enter id, smallcase without space', label='User')
    attrs["pattern"] = "[^\s]+"
    pwda = StrippedCharField(validators=[RegexValidator(regex='^[^\s]+$',message='Spaces are not allowed'),],
                           max_length=10, min_length=4, widget=form_widget.get_pwd_widget(attrs), 
                           help_text='enter your password', label="Enter Password")
    
    pwdb = StrippedCharField(validators=[RegexValidator(regex='^[^\s]+$',message='Spaces are not allowed'),],
                           max_length=10, min_length=4, widget=form_widget.get_pwd_widget(attrs), 
                           help_text='re-enter your password', label="Re-Enter Password")
    
    def clean(self):
        cleaned_data = super(Registration, self).clean();
        userid = cleaned_data.get('uid')
        pwda = cleaned_data.get('pwda')
        pwdb = cleaned_data.get('pwdb')
        form_error = False
        if (pwda != pwdb):
            self.add_error('pwdb', 'Password do not match')
            form_error = True
            
        #check if user already exist
        is_user_exist = User.objects.filter(username=userid).exists()
        if is_user_exist:
            self.add_error('uid', 'User already exist')
            form_error = True
            
        if form_error:
            raise forms.ValidationError('Please Correct below error', code='invalid')
        
class ChangePassword(forms.Form):
    attrs = {}
    attrs["pattern"] = "[^\s]+"
    cpwd = StrippedCharField(validators=[RegexValidator(regex='^[^\s]+$',message='Spaces are not allowed'),],
                           max_length=10, min_length=4, widget=form_widget.get_pwd_widget(attrs), 
                           help_text='enter your current password', label="Current Password")
    
    pwda = StrippedCharField(validators=[RegexValidator(regex='^[^\s]+$',message='Spaces are not allowed'),],
                           max_length=10, min_length=4, widget=form_widget.get_pwd_widget(attrs), 
                           help_text='enter your new password', label="Enter New Password")
    
    pwdb = StrippedCharField(validators=[RegexValidator(regex='^[^\s]+$',message='Spaces are not allowed'),],
                           max_length=10, min_length=4, widget=form_widget.get_pwd_widget(attrs), 
                           help_text='re-enter your new password', label="Re-Enter New Password")
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePassword, self).__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super(ChangePassword, self).clean();
        cpwd = cleaned_data.get('cpwd')
        pwda = cleaned_data.get('pwda')
        pwdb = cleaned_data.get('pwdb')
        form_error = False
        
        if (pwda != pwdb):
            self.add_error('pwdb', 'Password do not match')
            form_error = True
            
        #check if old password match
        if not self.user.check_password(cpwd):
            self.add_error('cpwd', 'Current password is wrong')
            form_error = True
            
        if form_error:
            raise forms.ValidationError('Please Correct below error', code='invalid')