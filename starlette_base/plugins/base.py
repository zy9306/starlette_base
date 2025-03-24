import logging


class PluginManager:
    def __init__(self, app):
        self.app = app

    def register_plugins(self, plugins):
        if not hasattr(self.app, "registered_plugins"):
            setattr(self.app, "registered_plugins", {})

        for plugin_name in plugins:
            if plugin_name not in self.app.registered_plugins:
                module = self._import_plugin(plugin_name)
                if hasattr(module, "register"):
                    module.register(self.app)
                    logging.warning(f"--- register plugin: {plugin_name}")
                    self.app.registered_plugins[plugin_name] = module

    def _import_plugin(self, plugin_name):
        import importlib

        return importlib.import_module(f"..plugins.{plugin_name}", __package__)
