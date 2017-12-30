from logging import getLogger

from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver

from . import models
from . import utils


logger = getLogger(__name__)

@receiver(post_save, sender=models.Country, dispatch_uid="country_changed")
def on_country_update(sender, **kwargs):  # @UnusedVariable
    logger.info('Country model updated')
    utils.create_onnew_include()
    
@receiver(post_save, sender=models.Category, dispatch_uid="category_changed")
def on_category_update(sender, **kwargs):  # @UnusedVariable
    logger.info('Category model updated')
    utils.create_onnew_include()
    
@receiver(post_save, sender=models.Solution, dispatch_uid="solution_changed")
def on_solution_update(sender, **kwargs):  # @UnusedVariable
    logger.info('Solution model updated')
    utils.create_onnew_include()
    
@receiver([post_save, post_delete], sender=models.AllSites, dispatch_uid="allsite_changed")
def on_allsite_update(sender, **kwargs):  # @UnusedVariable
    logger.info('AllSite model updated')
    utils.create_table_include()
    
    
