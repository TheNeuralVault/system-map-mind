import json
import os
from pathlib import Path
from typing import Dict, Any

class MapExporter:
    """Synchronizes the system map to OS Core and Memory Organ (GDrive)."""
    def __init__(self, local_cache: str, drive_path: str):
        self.local_cache = Path(local_cache).expanduser().resolve()
        self.drive_path = Path(drive_path).expanduser().resolve()

    def publish(self, topology: Dict[str, Any], integrity_hash: str):
        payload = {
            "version": "1.0",
            "integrity_hash": integrity_hash,
            "topology": topology
        }
        
        # Write to OS Core Cache (Atomic write pattern)
        temp_path = self.local_cache.with_suffix(".tmp")
        with open(temp_path, 'w') as f:
            json.dump(payload, f, indent=2)
        os.replace(temp_path, self.local_cache)

        # Write to GDrive if substrate is mounted
        try:
            if self.drive_path.parent.exists():
                with open(self.drive_path, 'w') as f:
                    json.dump(payload, f, indent=2)
        except Exception:
            pass
