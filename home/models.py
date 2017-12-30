from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator

class Category(models.Model):
    category = models.CharField(max_length=60,validators=[MinLengthValidator(3),], primary_key=True)
    listorder = models.SmallIntegerField(default=50)
    
    def __str__(self):
        return self.category 

class Country(models.Model):
    country = models.CharField(max_length=60, validators=[MinLengthValidator(3),], primary_key=True)
    code = models.CharField(max_length=3, validators=[MinLengthValidator(2),], unique=True)
    listorder = models.SmallIntegerField(default=50)
    
    def __str__(self):
        return self.country
    
class Solution(models.Model):
    solution = models.CharField(max_length=60, validators=[MinLengthValidator(3),], primary_key=True)
    listorder = models.SmallIntegerField(default=50)
    
    def __str__(self):
        return self.solution
    
class AllSites(models.Model):
    name = models.CharField(max_length=100, unique=True, validators=[MinLengthValidator(4),], verbose_name="Site name", help_text="site name")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    solution = models.ForeignKey(Solution, on_delete=models.CASCADE)
    
    testurl_direct = models.CharField   (max_length=255,
                                         validators=[MinLengthValidator(4),
                                        RegexValidator(regex=r'^https?:\/\/', message='site must start with http:// or https://')], 
                                        unique=True,  null=True, blank=True, 
                                        help_text="if not applicable, leave blank", verbose_name='Test direct URL')
    
    testurl_indirect = models.CharField (max_length=255,
                                        validators=[MinLengthValidator(4),
                                        RegexValidator(regex=r'^https?:\/\/', message='site must start with http:// or https://')], 
                                        unique=True, null=True, blank=True,  
                                        help_text="if not applicable, leave blank", verbose_name='Test indirect URL')
    
    systurl_direct = models.CharField   (max_length=255,
                                        validators=[MinLengthValidator(4),
                                        RegexValidator(regex=r'^https?:\/\/', message='site must start with http:// or https://')], 
                                        unique=True,  null=True, blank=True, 
                                        help_text="if not applicable, leave blank", verbose_name='Syst direct URL')
     
    systurl_indirect = models.CharField (max_length=255,
                                        validators=[MinLengthValidator(4),RegexValidator(regex=r'^https?:\/\/', message='site must start with http:// or https://')], 
                                        unique=True, null=True, blank=True,  
                                        help_text="if not applicable, leave blank", verbose_name='Syst indirect URL')
     
    produrl_direct = models.CharField   (max_length=255,
                                        validators=[MinLengthValidator(4),
                                        RegexValidator(regex=r'^https?:\/\/', message='site must start with http:// or https://')], 
                                        unique=True,   null=True, blank=True, help_text="if not applicable, leave blank", verbose_name='Prod direct URL')
    
    produrl_indirect = models.CharField (max_length=255,
                                        validators=[MinLengthValidator(4),
                                        RegexValidator(regex=r'^https?:\/\/', message='site must start with http:// or https://')], 
                                        unique=True, null=True, blank=True,  help_text="if not applicable, leave blank", verbose_name='Prod indirect URL')
    
    last_modified_by = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name

class UserRecentSite(models.Model):
    userid = models.CharField(max_length=30, db_index=True)
    site_id = models.ForeignKey(AllSites, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, db_index=True)
    
    class Meta:
        unique_together = (("userid", "site_id"),)
        
    def __str__(self):
        return ('{} : {}'.format(self.userid, self.site_id))
        