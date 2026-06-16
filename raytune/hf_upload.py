import os

from huggingface_hub import create_repo, upload_folder


def upload_folder_to_hf(hf_repo_id: str, artifacts_dir: str, target_domain: str):
    token = os.environ.get("HF_TOKEN")
    if not token:
        raise RuntimeError("Set HF_TOKEN before uploading to HuggingFace Hub.")
    if hf_repo_id.startswith("<team-or-user>"):
        raise RuntimeError("Set HF_REPO_ID to the real HuggingFace repo id before upload.")
    create_repo(
        repo_id=hf_repo_id,
        repo_type="model",
        private=False,
        exist_ok=True,
        token=token,
    )
    upload_folder(
        repo_id=hf_repo_id,
        repo_type="model",
        folder_path=str(artifacts_dir),
        commit_message=f"Add YOLO26-seg Phase 3 {target_domain} artifacts",
        token=token,
    )
    print(f"Uploaded artifacts to https://huggingface.co/{hf_repo_id}")
