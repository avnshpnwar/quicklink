from django import forms
from django.forms import ModelForm

from .models import AllSites
import logging

logger = logging.getLogger(__name__)

class AddSite(ModelForm):
    name = forms.CharField(label='Site Name', min_length=4, max_length=100)
    testurl_direct =    forms.CharField(
                            label="Test Direct URL", 
                            required = False,
                            widget = forms.TextInput(attrs = {'pattern': '^https?:\/\/[^\s]*', 'title':'URL must start with http:// or https://',}),
                            min_length=10, max_length=255,
                            help_text = 'if not applicable, leave blank',
                        )
    testurl_indirect =  forms.CharField(
                            label="Test Indirect URL", 
                            required = False,
                            widget = forms.TextInput(attrs = {'pattern': '^https?:\/\/[^\s]*', 'title':'URL must start with http:// or https://',}),
                            min_length=10, max_length=255,
                            help_text = 'if not applicable, leave blank',
                        )
    
    systurl_direct =    forms.CharField(
                            label="Syst Direct URL", 
                            required = False,
                            widget = forms.TextInput(attrs = {'pattern': '^https?:\/\/[^\s]*', 'title':'URL must start with http:// or https://',}),
                            min_length=10, max_length=255,
                            help_text = 'if not applicable, leave blank',
                        )
    
    systurl_indirect =  forms.CharField(
                            label="Syst Indirect URL", 
                            required = False,
                            widget = forms.TextInput(attrs = {'pattern': '^https?:\/\/[^\s]*', 'title':'URL must start with http:// or https://',}),
                            min_length=10, max_length=255,
                            help_text = 'if not applicable, leave blank',
                        )
    
    produrl_direct =    forms.CharField(
                            label="Prod Direct URL", 
                            required = False,
                            widget = forms.TextInput(attrs = {'pattern': '^https?:\/\/[^\s]*', 'title':'URL must start with http:// or https://',}),
                            min_length=10, max_length=255,
                            help_text = 'if not applicable, leave blank',
                        )
    
    produrl_indirect =  forms.CharField(
                            label="Prod Indirect URL", 
                            required = False,
                            widget = forms.TextInput(attrs = {'pattern': '^https?:\/\/[^\s]*', 'title':'URL must start with http:// or https://',}),
                            min_length=10, max_length=255,
                            help_text = 'if not applicable, leave blank',
                        )
    class Meta:
        model=AllSites
        fields = ['name', 'category', 'country', 'solution', 'testurl_direct', 'testurl_indirect',
                  'systurl_direct', 'systurl_indirect', 'produrl_direct', 'produrl_indirect']  
    
    def clean(self):
        cleaned_data = super().clean()
        strip_them = ('name', 'testurl_direct','testurl_indirect', 'systurl_direct', 'systurl_indirect', 'produrl_direct', 'produrl_indirect' )
        for item in cleaned_data:
            if item in strip_them and cleaned_data[item] is not None:
                cleaned_data[item] = cleaned_data[item].strip()
                if cleaned_data[item] == '':
                    # we have null and blank=true in our model, i know bad code, but it is required
                    # below code will convert spaces into None for these fields
                    logger.debug('{} making None'.format(item))
                    cleaned_data[item] = None
        
class BatchUploadForm(forms.Form):
    file = forms.FileField(label = 'Select File to Upload')
    update_existing = forms.BooleanField(label = 'Update if site already exist', required=False)