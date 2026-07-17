import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
GENERATOR_PATH = REPO_ROOT / "scripts" / "generate_excalidraw.py"


def load_generator():
    spec = importlib.util.spec_from_file_location("generate_excalidraw", GENERATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ArchitectureDiagramGeneratorTest(unittest.TestCase):
    def test_generate_all_is_deterministic_and_matches_the_approved_contract(self):
        generator = load_generator()

        with tempfile.TemporaryDirectory() as first_dir, tempfile.TemporaryDirectory() as second_dir:
            first_paths = generator.generate_all(Path(first_dir))
            second_paths = generator.generate_all(Path(second_dir))

            self.assertEqual(
                [path.name for path in first_paths],
                ["architecture_diagram.excalidraw", "deployment_architecture_diagram.excalidraw"],
            )
            self.assertEqual(
                [path.read_bytes() for path in first_paths],
                [path.read_bytes() for path in second_paths],
            )

            application = json.loads(first_paths[0].read_text(encoding="utf-8"))
            deployment = json.loads(first_paths[1].read_text(encoding="utf-8"))

        application_text = self._diagram_text(application)
        deployment_text = self._diagram_text(deployment)
        combined_text = f"{application_text}\n{deployment_text}"

        for required in (
            "YOLO26-seg quantized",
            "diseases.json",
            "/api/v1/predict",
            "/api/v1/knowledge",
            "/api/v1/auth",
            "/api/v1/history",
        ):
            self.assertIn(required, application_text)

        for required in ("GCP VM", "k3s", "Traefik", "GitHub Actions", "GHCR", "Helm"):
            self.assertIn(required, deployment_text)

        for forbidden in ("RAG", "Vector DB", "YOLOv8"):
            self.assertNotIn(forbidden, combined_text)

        self.assertIn("dịch vụ đã triển khai", deployment_text)
        self.assertNotIn("Redis cache đang hoạt động", deployment_text)

        for diagram in (application, deployment):
            self.assertEqual(diagram["type"], "excalidraw")
            self.assertEqual(diagram["version"], 2)
            ids = [element["id"] for element in diagram["elements"]]
            self.assertEqual(len(ids), len(set(ids)))
            for element in diagram["elements"]:
                self.assertEqual(element["roughness"], 0, element["id"])
                self.assertEqual(element["opacity"], 100, element["id"])
                if element["type"] == "text":
                    self.assertEqual(element["fontFamily"], 3, element["id"])

    @staticmethod
    def _diagram_text(diagram):
        return "\n".join(
            element["text"] for element in diagram["elements"] if element["type"] == "text"
        )


if __name__ == "__main__":
    unittest.main()
