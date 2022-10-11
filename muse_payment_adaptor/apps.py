from django.apps import AppConfig


class MusePaymentAdaptorConfig(AppConfig):
    name = 'muse_payment_adaptor'

    def ready(self):
        """
        This module requires obligatory EO number. It overwrites default settings.
        If preexisting setting for phone is added, and it's different from 'M' - mandatory - error is raised.
        """
        from core.apps import CoreConfig
        if CoreConfig.fields_controls_eo.get('phone') not in (None, 'M'):
            raise ValueError("Instance has already predefined control for user's phone number. "
                             "This module require mandatory EO phone number.")
        else:
            CoreConfig.fields_controls_eo['phone'] = 'M'
