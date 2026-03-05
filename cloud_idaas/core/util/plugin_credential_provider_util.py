import logging
from importlib.metadata import entry_points
from typing import Optional

from cloud_idaas.core.constants import PluginConstants
from cloud_idaas.core.exceptions import ConfigException
from cloud_idaas.core.provider.plugin_credential_provider import PluginCredentialProvider
from cloud_idaas.core.util.string_util import StringUtil

logger = logging.getLogger(__name__)


class PluginCredentialProviderUtil:
    _plugin_credential_provider_dict: Optional[dict[str, PluginCredentialProvider]] = None

    @classmethod
    def _init_plugin_credential_provider_dict(cls):
        if cls._plugin_credential_provider_dict:
            return
        cls._plugin_credential_provider_dict = {}
        eps = entry_points().get(PluginConstants.PLUGIN_GROUP_NAME, [])
        for ep in eps:
            try:
                # load plugin class
                plugin_cls = ep.load()

                if not issubclass(plugin_cls, PluginCredentialProvider):
                    logger.warning(f"Plugin {ep.name} does not implement PluginCredentialProvider, skipping")
                    continue

                plugin = plugin_cls()

                cls._plugin_credential_provider_dict[ep.name] = plugin
                logger.info(f"Loaded plugin {ep.name}")
            except Exception as e:
                logger.error(f"Failed to load plugin {ep.name}: {e}")

    @classmethod
    def get_plugin_credential_provider(cls, plugin_name: str) -> PluginCredentialProvider:
        if cls._plugin_credential_provider_dict is None:
            cls._init_plugin_credential_provider_dict()
        if StringUtil.is_blank(plugin_name):
            raise ConfigException(error_message="plugin_name can not be empty.")

        plugin_credential_provider = cls._plugin_credential_provider_dict.get(plugin_name)
        if not plugin_credential_provider:
            raise ConfigException(error_message=f"Plugin {plugin_name} not found")

        return plugin_credential_provider
