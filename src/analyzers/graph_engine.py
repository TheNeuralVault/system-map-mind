import hashlib
import json
from typing import Dict, Any

class GraphEngine:
    """Performs topological analysis and integrity checks on the Federation."""
    
    @staticmethod
    def calculate_integrity(topology: Dict[str, Any]) -> str:
        topo_string = json.dumps(topology, sort_keys=True)
        return hashlib.sha256(topo_string.encode()).hexdigest()

    @staticmethod
    def map_substrate_distribution(topology: Dict[str, Any]) -> Dict[str, int]:
        stats = {"TERMUX": 0, "OCI": 0, "GITHUB": 0, "GDRIVE": 0}
        for data in topology.values():
            sub = data.get("substrate", "UNKNOWN")
            if sub in stats:
                stats[sub] += 1
        return stats
