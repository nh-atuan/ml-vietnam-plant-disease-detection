# Reproducibility
RANDOM_SEED = 42

# Disease class definitions
RICE_CLASSES = ["BrownSpot", "Healthy", "Hispa", "LeafBlast"]

COFFEE_CLASSES = ["LeafMiner", "PowderyMildew", "Rust", "AlgalLeafSpot"]

# Folder-name -> display-name mappings
RICE_FOLDER = {cls: cls for cls in RICE_CLASSES}
COFFEE_FOLDER = {name: str(i) for i, name in enumerate(COFFEE_CLASSES)}

# Visualization palettes
PALETTE_RICE = ["#D95F02", "#1B9E77", "#7570B3", "#E7298A"]
PALETTE_COFFEE = ["#A6761D", "#E6AB02", "#66A61E", "#E7298A"]
