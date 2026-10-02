from __future__ import annotations

import hashlib
from pathlib import Path
import yaml
from .models import SOP


def load_sops(path: Path) -> tuple[list[SOP], str]:
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()[:10]
    data = yaml.safe_load(raw) or {}
    sops = [SOP.model_validate(item) for item in data.get("sops", [])]
    if len(sops) < 10:
        raise ValueError(f"Expected at least 10 SOPs, found {len(sops)}")
    if len({s.id for s in sops}) != len(sops):
        raise ValueError("SOP IDs must be unique")
    return sops, digest
