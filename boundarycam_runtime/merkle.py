from __future__ import annotations
import hashlib
from typing import Iterable, List

def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def merkle_root(leaves: Iterable[str]) -> str:
    layer: List[str] = list(leaves)
    if not layer:
        return sha256_text("BOUNDARYCAM_EMPTY_MERKLE_TREE")
    for item in layer:
        if len(item) != 64:
            raise ValueError("invalid merkle leaf hash")
    while len(layer) > 1:
        if len(layer) % 2:
            layer.append(layer[-1])
        layer = [sha256_text(a + b) for a, b in zip(layer[0::2], layer[1::2])]
    return layer[0]
