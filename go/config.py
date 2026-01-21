
DEFAULT_IMPORT_PATH = "github.com/hazelcast/hazelcast-go-client"


class Config:

    def __init__(self, base_import_path="", include_methods=None, include_types=None, mapping=None, override_imports=None, types=None):
        self.base_import_path = base_import_path or DEFAULT_IMPORT_PATH
        self.include_methods = include_methods or []
        self.include_types = include_types or []
        self.mapping = mapping or {}
        self.override_imports = override_imports or {}
        self.types = types or {}

    @classmethod
    def from_json(cls, d: dict):
        keys = [
            "base_import_path",
            "include_methods",
            "include_types",
            "mapping",
            "override_imports",
            "types"
        ]
        return cls(**{k: d.get(k) for k in keys})