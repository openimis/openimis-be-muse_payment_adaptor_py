import logging
import os
from pathlib import Path

from cryptography.hazmat.primitives.serialization.pkcs12 import load_pkcs12
from django.apps import AppConfig
from django.utils.functional import classproperty

DEFAULT_CONFIG = {
    'certificates_path': 'certificates',  # Relative path from `openimis-be` where certificates are stored
    'certificate_name': 'certificate.pfx',  # Filename, relative path from certificates_path directory
    'certificate_password': str.encode('<certificate_password>'),
    'certificate_alias': str.encode('<certificate_alias>'),
    'gql_hf_bank_info_search_perms': [],
    'gql_hf_bank_info_create_perms': [],
    'gql_hf_bank_info_update_perms': [],
    'gql_hf_bank_info_delete_perms': [],
}

logger = logging.getLogger(__name__)


class MusePaymentAdaptorConfig(AppConfig):
    name = 'muse_payment_adaptor'

    certificates_path = None
    certificate_name = None
    certificate_password = None
    certificate_alias = None

    gql_hf_bank_info_search_perms = None
    gql_hf_bank_info_create_perms = None
    gql_hf_bank_info_update_perms = None
    gql_hf_bank_info_delete_perms = None

    __certificate = None

    @classproperty
    def certificate(cls):
        """Lazy loaded, cached values"""
        if getattr(cls, '__certificate', None) is None:
            cls.__certificate = cls.__load_certificate()
        return cls.__certificate

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
        self.__load_config(cfg)

    @classmethod
    def __load_config(cls, cfg):
        """
        Load all config fields that match current AppConfig class fields, all custom fields have to be loaded separately
        """
        for field in cfg:
            if hasattr(MusePaymentAdaptorConfig, field):
                setattr(MusePaymentAdaptorConfig, field, cfg[field])

    @classmethod
    def __load_certificate(cls):
        path = Path(cls.__get_path_from_assembly(MusePaymentAdaptorConfig.certificates_path)).joinpath(
            MusePaymentAdaptorConfig.certificate_name)
        certificate_data = cls.__load_certificate_data_as_binary(path)

        try:
            return load_pkcs12(data=certificate_data, password=cls.certificate_password)
        except BaseException as e:
            logger.error("Error while loading a certificate", exc_info=e)
            return None

    @classmethod
    def __load_certificate_data_as_binary(cls, path):
        try:
            with open(path, 'rb') as f:
                return f.read()
        except FileNotFoundError as e:
            print(e)
            logger.error("Certificate from path %s not found.", path, exc_info=e)
        except IsADirectoryError as e:
            logger.error(
                "Failed to log certificate from path %s. "
                "Path is marked as directory, is certificate filename provided?", path, exc_info=e)

    @classmethod
    def __get_path_from_assembly(cls, path):
        from django.conf import settings
        # Note: This functionality is reused across application (e.g. AI),
        # should be refactored after generic solution for loading assembly files is implemented.

        isabs = os.path.isabs(path)
        if not isabs:
            # openimis-be_py
            base = Path(settings.BASE_DIR).parent
            path = F'{base}/{path}'

        return path
