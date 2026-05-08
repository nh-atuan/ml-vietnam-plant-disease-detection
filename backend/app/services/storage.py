"""
Storage Service — MinIO object storage.

Phụ trách: Đàm Tiến Đạt
Phase 5, Task 5.2

TODO:
- [ ] Kết nối MinIO
- [ ] Upload ảnh gốc
- [ ] Generate presigned URL
"""


class StorageService:
    """MinIO storage service cho lưu trữ ảnh."""

    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket: str):
        # TODO: Khởi tạo MinIO client
        raise NotImplementedError

    def upload_image(self, image_bytes: bytes, filename: str) -> str:
        """Upload ảnh, trả về object key."""
        # TODO: Implement
        raise NotImplementedError

    def get_url(self, object_key: str) -> str:
        """Lấy presigned URL."""
        # TODO: Implement
        raise NotImplementedError
