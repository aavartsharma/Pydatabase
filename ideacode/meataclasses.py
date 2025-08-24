# metaclass_boilerplate.py
from typing import Any, Dict, Tuple

class BaseMeta(type):
    """
    A minimal, reusable metaclass template.

    Lifecycle:
      - __prepare__  -> get class namespace (dict-like) before class body executes
      - __new__      -> create the class object
      - __init__     -> finalize the class (after it's created)
      - __call__     -> control instance creation (when you do MyClass(...))
    """

    @classmethod
    def __prepare__(mcls, name: str, bases: Tuple[type, ...], **kwargs) -> Dict[str, Any]:
        print("")
        # Return the namespace dict that the class body writes into.
        # You can return an OrderedDict or custom mapping if you need ordering or hooks.
        return {}

    def __new__(mcls, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any], **kwargs):
        # Read/modify the class namespace before the class is actually created
        # Example: inject a common attribute or method
        namespace.setdefault("_meta_options", kwargs)
        namespace.setdefault("common_attr", "available_on_all_subclasses")
        cls = super().__new__(mcls, name, bases, namespace)
        return cls

    def __init__(cls, name: str, bases: Tuple[type, ...], namespace: Dict[str, Any], **kwargs):
        # Final adjustments after class is created
        super().__init__(name, bases, namespace)
        # Example: simple validation
        required = cls._meta_options.get("require_methods", [])
        for meth in required:
            if not callable(getattr(cls, meth, None)):
                raise TypeError(f"{cls.__name__} must define method: {meth}")

    def __call__(cls, *args, **kwargs):
        # Control instance creation (you can implement singletons, pools, etc.)
        # Example: simple logging
        return super().__call__(*args, **kwargs)

class Base(metaclass=BaseMeta):
    pass

# Pass options to the metaclass via class definition kwargs
class Service(Base, require_methods=["run"]):
    def run(self):
        print("running!")

s = Service()
print(Service.common_attr)       # "available_on_all_subclasses"
print(Service._meta_options)     # {'require_methods': ['run']}
