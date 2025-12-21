"""
Test Fixture: Insecure Deserialization Vulnerable Patterns (Python)

This file contains 3+ insecure deserialization patterns that MUST be detected by
SEC-005 rule (devforgeai/ast-grep/rules/python/security/insecure-deserialization.yml).

Expected detections: ≥3 violations
Rule ID: SEC-005
Severity: CRITICAL
"""

import pickle
import yaml


# Pattern 1: pickle.loads() without validation
def load_user_session_unsafe(session_data: bytes) -> dict:
    """VULNERABLE: pickle.loads() allows arbitrary code execution"""

    # SEC-005 should detect pickle.loads()
    session = pickle.loads(session_data)

    return session


# Pattern 2: pickle.load() from file
def load_cache_from_file_unsafe(cache_file: str):
    """VULNERABLE: pickle.load() from untrusted file"""

    # SEC-005 should detect pickle.load()
    with open(cache_file, 'rb') as f:
        cache_data = pickle.load(f)

    return cache_data


# Pattern 3: yaml.load() without Loader parameter
def load_config_unsafe(config_yaml: str) -> dict:
    """VULNERABLE: yaml.load() without Loader allows code execution"""

    # SEC-005 should detect yaml.load() without Loader
    config = yaml.load(config_yaml)

    return config


# Pattern 4: yaml.unsafe_load() explicit usage
def load_template_unsafe(template_yaml: str) -> dict:
    """VULNERABLE: yaml.unsafe_load() allows code execution"""

    # SEC-005 should detect yaml.unsafe_load()
    template = yaml.unsafe_load(template_yaml)

    return template


# Pattern 5: Nested pickle deserialization
class CacheManager:
    """VULNERABLE: Pickle-based cache"""

    def get(self, key: str) -> any:
        """VULNERABLE: pickle.loads() in cache retrieval"""
        import redis

        r = redis.Redis()
        serialized = r.get(key)

        if serialized:
            # SEC-005 should detect pickle.loads()
            return pickle.loads(serialized)

        return None

    def set(self, key: str, value: any):
        """VULNERABLE: pickle.dumps() in cache storage"""
        import redis

        r = redis.Redis()
        serialized = pickle.dumps(value)
        r.set(key, serialized)


# Pattern 6: yaml.load() with FullLoader (still vulnerable to DoS)
def load_config_with_loader(config_yaml: str) -> dict:
    """VULNERABLE: yaml.load() with FullLoader has DoS risks"""

    # SEC-005 should detect yaml.load() even with FullLoader
    config = yaml.load(config_yaml, Loader=yaml.FullLoader)

    return config
