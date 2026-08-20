"""Small dependency-light helpers shared by application components."""

from __future__ import annotations

import hashlib
import json
from datetime import date, datetime
from decimal import Decimal
from typing import Any


def stable_payload_hash(payload: Any) -> str:
    """Return a deterministic SHA-256 digest for cache keys and audit references."""

    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def json_safe(value: Any) -> Any:
    """Convert common scientific Python scalar values into JSON-compatible values."""

    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    if hasattr(value, "item"):
        return value.item()
    if isinstance(value, dict):
        return {str(key): json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(item) for item in value]
    return value


def clamp(value: float, minimum: float, maximum: float) -> float:
    """Clamp a scalar to an inclusive range and reject invalid bounds."""

    if minimum > maximum:
        raise ValueError("minimum cannot be greater than maximum")
    return max(minimum, min(maximum, value))
