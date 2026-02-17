import os
import json
import logging
from pathlib import Path
from typing import Dict, Any

class ManifestReader:
    """Discovers and parses manifest.json files across the Federation."""
    def __init__(self, federation_root: str):
        self.root = Path(federation_root).expanduser().resolve()
        self.logger = logging.getLogger("cartographer.collector")

    def scan_minds(self) -> Dict[str, Any]:
        topology = {}
        self.logger.info(f"Scanning federation at {self.root}")
        
        if not self.root.exists():
            return {}

        for mind_dir in self.root.iterdir():
            if mind_dir.is_dir():
                manifest_path = mind_dir / "manifest.json"
                mind_config_path = mind_dir / "mind.json"
                
                if manifest_path.exists() and mind_config_path.exists():
                    try:
                        with open(manifest_path, 'r') as f:
                            manifest = json.load(f)
                        with open(mind_config_path, 'r') as f:
                            identity = json.load(f)
                            
                        topology[identity['name']] = {
                            "id": identity['mind_id'],
                            "version": identity.get('version', '0.0.0'),
                            "substrate": identity['substrate_affinity'],
                            "endpoints": manifest.get('endpoints', {}),
                            "capabilities": manifest.get('capabilities', []),
                            "path": str(mind_dir.absolute())
                        }
                    except Exception as e:
                        self.logger.error(f"Failed to index {mind_dir.name}: {e}")
        return topology
