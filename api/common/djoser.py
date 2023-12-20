"""
Module for overriding, customizing the Djoser library
"""

import copy

from djoser.conf import default_settings, LazySettings, Settings

_all__ = ("extended_settings",)

extended_default_settings = copy.copy(default_settings)
extended_default_settings["PERMISSIONS"].update(
    {
        "current_user": ["rest_framework.permissions.IsAuthenticated"],
    }
)


class CustomSettings(Settings):
    def _load_default_settings(self):
        for setting_name, setting_value in extended_default_settings.items():
            if setting_name.isupper():
                setattr(self, setting_name, setting_value)


class CustomLazySettings(LazySettings):
    def _setup(self, explicit_overriden_settings=None):
        self._wrapped = CustomSettings(
            extended_default_settings, explicit_overriden_settings
        )


extended_settings = CustomLazySettings()
