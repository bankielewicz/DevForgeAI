"""
Test Fixture: Insecure Deserialization Safe Patterns (Python)

This file contains SAFE deserialization patterns that should NOT trigger false positives
for SEC-005 rule.

Expected detections: 0 violations (no false positives)
Rule ID: SEC-005
Severity: CRITICAL
"""

import json
import yaml
from typing import Any, Dict
from pydantic import BaseModel, ValidationError


# Safe Pattern 1: JSON deserialization (safe by default)
def load_user_session_safe(session_json: str) -> dict:
    """SAFE: JSON deserialization is safe (no code execution)"""

    # SAFE - JSON doesn't allow code execution
    session = json.loads(session_json)

    return session


# Safe Pattern 2: yaml.safe_load() instead of yaml.load()
def load_config_safe(config_yaml: str) -> dict:
    """SAFE: yaml.safe_load() prevents code execution"""

    # SAFE - yaml.safe_load() only allows basic types
    config = yaml.safe_load(config_yaml)

    return config


# Safe Pattern 3: Schema validation after deserialization
class UserSession(BaseModel):
    """SAFE: Pydantic model for validation"""
    user_id: int
    username: str
    roles: list[str]


def load_session_with_validation(session_json: str) -> UserSession:
    """SAFE: Schema validation after JSON load"""

    # SAFE - JSON + schema validation
    data = json.loads(session_json)

    try:
        session = UserSession(**data)
    except ValidationError as e:
        raise ValueError(f"Invalid session data: {e}")

    return session


# Safe Pattern 4: Restricted unpickler (custom implementation)
import pickle
import io


class RestrictedUnpickler(pickle.Unpickler):
    """SAFE: Restricted pickle unpickler with whitelist"""

    def find_class(self, module: str, name: str):
        """Override to only allow safe classes"""

        # Whitelist of allowed modules/classes
        safe_modules = {
            'builtins': {'dict', 'list', 'tuple', 'set', 'frozenset'},
            'collections': {'OrderedDict', 'defaultdict'},
        }

        if module in safe_modules and name in safe_modules[module]:
            return super().find_class(module, name)

        raise pickle.UnpicklingError(
            f"Forbidden class: {module}.{name}"
        )


def restricted_pickle_load(data: bytes) -> Any:
    """SAFE: Pickle with restricted class loading"""

    # SAFE - restricts allowed classes
    return RestrictedUnpickler(io.BytesIO(data)).load()


# Safe Pattern 5: Message pack (safer alternative to pickle)
def load_cache_with_msgpack(cache_data: bytes) -> dict:
    """SAFE: MessagePack as safer alternative"""
    import msgpack

    # SAFE - MessagePack doesn't execute code
    cache = msgpack.unpackb(cache_data, raw=False)

    return cache


# Safe Pattern 6: TOML configuration (safe)
def load_config_toml(config_toml: str) -> dict:
    """SAFE: TOML parsing is safe"""
    import tomli

    # SAFE - TOML doesn't allow code execution
    config = tomli.loads(config_toml)

    return config


# Safe Pattern 7: Protobuf (type-safe serialization)
class CacheManagerSafe:
    """SAFE: JSON-based cache instead of pickle"""

    def get(self, key: str) -> Any:
        """SAFE: JSON deserialization"""
        import redis

        r = redis.Redis()
        serialized = r.get(key)

        if serialized:
            # SAFE - JSON instead of pickle
            return json.loads(serialized.decode('utf-8'))

        return None

    def set(self, key: str, value: Any):
        """SAFE: JSON serialization"""
        import redis

        r = redis.Redis()
        serialized = json.dumps(value)
        r.set(key, serialized)
