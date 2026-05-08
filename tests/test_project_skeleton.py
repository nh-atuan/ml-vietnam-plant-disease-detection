from pathlib import Path

REQUIRED_PATHS = [
    Path("docs/PLAN.md"),
    Path("configs/training_defaults.yaml"),
    Path("configs/models/mobilenetv2.yaml"),
    Path("configs/models/resnet50.yaml"),
    Path("configs/models/swin_transformer.yaml"),
    Path("configs/models/dinov3.yaml"),
    Path("src/training/trainer.py"),
    Path("src/evaluation/evaluator.py"),
    Path("scripts/export_onnx.py"),
    Path("backend/Dockerfile"),
    Path("backend/app/main.py"),
    Path("backend/app/db/schema.sql"),
    Path("frontend/package.json"),
    Path("frontend/src/lib/api.ts"),
    Path("deployment/docker-compose.yml"),
]


def test_phase_skeleton_paths_exist() -> None:
    missing = [str(path) for path in REQUIRED_PATHS if not path.exists()]
    assert missing == []
