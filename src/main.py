import time
import logging
import sys
from pathlib import Path

# Adjust path for internal module discovery
sys.path.append(str(Path(__file__).parent))

from collectors.manifest_reader import ManifestReader
from analyzers.graph_engine import GraphEngine
from publishers.map_exporter import MapExporter

logging.basicConfig(
    level=logging.INFO,
    format='🔱 [MAP_MIND] %(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("cartographer")

def main():
    # Production Paths for Magnus Opus AIOS
    FEDERATION_ROOT = "~/minds"
    OS_CACHE = "~/magnus-opus/OS/manifests/topology_cache.json"
    GDRIVE_MAP = "~/cloud/google-drive/artifacts/system_topology.json"

    collector = ManifestReader(FEDERATION_ROOT)
    analyzer = GraphEngine()
    publisher = MapExporter(OS_CACHE, GDRIVE_MAP)

    logger.info("The Cartographer is mapping the Federation...")

    last_hash = ""
    
    while True:
        try:
            # Step 1: Discover
            topology = collector.scan_minds()
            
            # Step 2: Analyze
            current_hash = analyzer.calculate_integrity(topology)
            
            # Step 3: Publish only if changed
            if current_hash != last_hash:
                stats = analyzer.map_substrate_distribution(topology)
                logger.info(f"Topological shift detected. Distribution: {stats}")
                publisher.publish(topology, current_hash)
                last_hash = current_hash
            
        except Exception as e:
            logger.error(f"Critical mapping failure: {e}")
            
        time.sleep(30) # High-frequency scan for boot phase

if __name__ == "__main__":
    main()
