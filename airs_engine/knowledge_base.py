"""
AIRS Knowledge Base Interface Module
Provides structured access to regulatory sources, standards, and evidence tags.
"""

import json
import os
from typing import Dict, Any, List, Optional

class KnowledgeBase:
    _registry: Optional[Dict[str, Any]] = None

    @classmethod
    def load_registry(cls) -> Dict[str, Any]:
        if cls._registry is None:
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "knowledge", "kb_registry.json")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    cls._registry = json.load(f)
            else:
                cls._registry = {"regulatory_references": []}
        return cls._registry

    @classmethod
    def get_reference(cls, ref_id: str) -> Optional[Dict[str, Any]]:
        reg = cls.load_registry()
        for ref in reg.get("regulatory_references", []):
            if ref.get("id") == ref_id:
                return ref
        return None

    @classmethod
    def list_references_by_level(cls, level: str) -> List[Dict[str, Any]]:
        reg = cls.load_registry()
        return [ref for ref in reg.get("regulatory_references", []) if ref.get("level") == level]
