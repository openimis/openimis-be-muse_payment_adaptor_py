import os
from pathlib import Path

from django.apps import AppConfig
from django.utils.functional import classproperty

DEFAULT_CONFIG = {
    'certificates_path': 'certificates',  # Relative path from `openimis-be` where certificates are stored
    'digital_signature': 'digital_signature.cert',  # Filename, relative path from certificates_path directory
    'gql_hf_bank_info_search_perms': [],
    'gql_hf_bank_info_create_perms': [],
    'gql_hf_bank_info_update_perms': [],
    'gql_hf_bank_info_delete_perms': [],
}


class MusePaymentAdaptorConfig(AppConfig):
    name = 'muse_payment_adaptor'

    certificates_path = 'certificates'
    digital_signature = 'digital_signature.cert'

    gql_hf_bank_info_search_perms = None
    gql_hf_bank_info_create_perms = None
    gql_hf_bank_info_update_perms = None
    gql_hf_bank_info_delete_perms = None

    @classproperty
    def certificates(self):
        """Lazy loaded, cached values"""
        if getattr(self, '__certificates', None) is None:
            my_data = self.__load_certificates()
            self.__certificates = my_data
        return self.__certificates

    def ready(self):
        """
        This module requires obligatory EO number. It overwrites default settings.
        If preexisting setting for phone is added, and it's different from 'M' - mandatory - error is raised.
        """
        from core.apps import CoreConfig
        from core.models import ModuleConfiguration

        if CoreConfig.fields_controls_eo.get('phone') not in (None, 'M'):
            raise ValueError("Instance has already predefined control for user's phone number. "
                             "This module require mandatory EO phone number.")
        else:
            CoreConfig.fields_controls_eo['phone'] = 'M'

        cfg = ModuleConfiguration.get_or_default(self.name, DEFAULT_CONFIG)
        self.__load_config_config(cfg)

    @classmethod
    def __load_config_config(cls, cfg):
        """
        Load all config fields that match current AppConfig class fields, all custom fields have to be loaded separately
        """
        for field in cfg:
            if hasattr(MusePaymentAdaptorConfig, field):
                setattr(MusePaymentAdaptorConfig, field, cfg[field])

    @classmethod
    def __load_certificates(cls):
        cert_dir = MusePaymentAdaptorConfig.certificates_path
        return {
            'digital_signature':
                cls._load_from_assembly_file(F'{cert_dir}/{MusePaymentAdaptorConfig.digital_signature}')
        }

    @classmethod
    def _load_from_assembly_file(cls, path):
        import logging
        from django.conf import settings
        # Note: This functionality is reused across application (e.g. AI),
        # should be refactored after generic solution for loading assembly files is implemented.

        isabs = os.path.isabs(path)
        if not isabs:
            # openimis-be_py
            base = Path(settings.BASE_DIR).parent
            path = F'{base}/{path}'

        try:
            with open(path, 'r') as f:
                return "".join(f.readlines())
        except FileNotFoundError as e:
            print(e)
            logging.error("Certificate from path %s not found. Details: %s", path, e)
        except IsADirectoryError as e:
            logging.error(
                "Failed to log certificate from path %s. "
                "Path is marked as directory, is certificate filename provided?", path
            )
