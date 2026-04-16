from pathlib import Path

# ── Reproducibility ───────────────────────────────────────────
RANDOM_SEED = 42

# ── Disease class definitions ─────────────────────────────────
RICE_CLASSES = ["BrownSpot", "Healthy", "Hispa", "LeafBlast"]

# Coffee folders 0-3 map to the four disease categories below.
# Derived from RoCoLe-based dataset collected by UIT team.
# NOTE: verify exact biological mapping with the data collection team.
COFFEE_CLASSES = ["Bicho Mineiro", "Phoma", "Cercospora", "Coffee Rust"]

# Folder-name → display-name mappings (used for image loading)
RICE_FOLDER   = {cls: cls for cls in RICE_CLASSES}
COFFEE_FOLDER = {name: str(i) for i, name in enumerate(COFFEE_CLASSES)}

# ── Visualization palettes ────────────────────────────────────
PALETTE_RICE   = ["#D95F02", "#1B9E77", "#7570B3", "#E7298A"]
PALETTE_COFFEE = ["#A6761D", "#E6AB02", "#66A61E", "#E7298A"]