"""
Skip tracking functionality.

Tracks when users skip feedback and triggers suggestions after 3+ consecutive skips.
"""

import yaml
from pathlib import Path
from typing import Optional, Callable


# ============================================================================
# CONFIG FILE I/O (Private)
# ============================================================================

def _get_config_file(config_dir: Optional[Path] = None) -> Path:
    """
    Get feedback config file path.

    Args:
        config_dir: Config directory (default: .devforgeai/config)

    Returns:
        Path to feedback-preferences.yaml (per STORY-009 specification)
    """
    if config_dir is None:
        config_dir = Path.cwd() / '.devforgeai' / 'config'

    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / 'feedback-preferences.yaml'


def _load_config(config_file: Path) -> dict:
    """
    Load config from YAML file.

    Args:
        config_file: Path to config file

    Returns:
        Config dictionary (defaults to empty skip_counts if missing)
    """
    if not config_file.exists():
        return {'skip_counts': {}}

    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)

    return config or {'skip_counts': {}}


def _save_config(config: dict, config_file: Path) -> None:
    """
    Save config to YAML file.

    Args:
        config: Config dictionary
        config_file: Path to config file
    """
    with open(config_file, 'w') as f:
        yaml.safe_dump(config, f, default_flow_style=False)


def _apply_config_modification(config_file: Path, modifier_fn: Callable[[dict], dict]) -> None:
    """
    Apply modification to config atomically (DRY helper).

    Encapsulates read-modify-write pattern to reduce duplication.

    Args:
        config_file: Path to config file
        modifier_fn: Function that receives config dict and returns modified dict
    """
    config = _load_config(config_file)
    modified_config = modifier_fn(config)
    _save_config(modified_config, config_file)


# ============================================================================
# SKIP COUNTER OPERATIONS (Public)
# ============================================================================

def increment_skip(user_id: str, config_dir: Optional[Path] = None) -> int:
    """
    Increment skip count for user.

    Args:
        user_id: User ID
        config_dir: Config directory

    Returns:
        New skip count
    """
    config_file = _get_config_file(config_dir)

    def modify_config(config):
        if 'skip_counts' not in config:
            config['skip_counts'] = {}

        current_count = config['skip_counts'].get(user_id, 0)
        new_count = current_count + 1
        config['skip_counts'][user_id] = new_count
        return config

    _apply_config_modification(config_file, modify_config)

    # Reload to get updated count
    config = _load_config(config_file)
    return config['skip_counts'][user_id]


def get_skip_count(user_id: str, config_dir: Optional[Path] = None) -> int:
    """
    Get current skip count for user.

    Args:
        user_id: User ID
        config_dir: Config directory

    Returns:
        Current skip count
    """
    config_file = _get_config_file(config_dir)
    config = _load_config(config_file)
    return config.get('skip_counts', {}).get(user_id, 0)


def reset_skip_count(user_id: str, config_dir: Optional[Path] = None) -> None:
    """
    Reset skip count for user to 0.

    Args:
        user_id: User ID
        config_dir: Config directory
    """
    config_file = _get_config_file(config_dir)

    def modify_config(config):
        if 'skip_counts' not in config:
            config['skip_counts'] = {}

        config['skip_counts'][user_id] = 0
        return config

    _apply_config_modification(config_file, modify_config)


def check_skip_threshold(user_id: str, threshold: int = 3, config_dir: Optional[Path] = None) -> bool:
    """
    Check if user has reached skip threshold.

    Args:
        user_id: User ID
        threshold: Skip threshold (default: 3)
        config_dir: Config directory

    Returns:
        True if threshold reached, False otherwise
    """
    count = get_skip_count(user_id, config_dir)
    return count >= threshold

