from typing import Any, Generic, TypeVar

T = TypeVar("T")


class AttrProxy(Generic[T]):
    def __init__(self, plugin: Any, attr_name: str):
        self._plugin = plugin
        self._attr_name = attr_name

    def __getattr__(self, name):
        target = getattr(self._plugin, self._attr_name)
        return getattr(target, name)

    def __dir__(self):
        try:
            target = getattr(self._plugin, self._attr_name)
            return dir(target)
        except Exception:
            return []
