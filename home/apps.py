import logging

from django.apps import AppConfig


logger = logging.getLogger(__name__)
class HomeConfig(AppConfig):
    name = 'home'
    def ready(self):
        from . import signals  # @UnusedImport
        logger.debug('signal imported from ready function')
        from . import utils 
        logger.debug('signal imported from ready function')
        #generate static html page
        logger.info('executing one off create_table_include')
        utils.create_table_include()
        logger.info('executing one off create_onnew_include')
        utils.create_onnew_include()
