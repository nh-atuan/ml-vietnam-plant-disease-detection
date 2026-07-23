"""
Storage Service — MinIO object storage.
"""
from datetime import timedelta
import io
import os
import uuid
from minio import Minio


class StorageService:
    """MinIO storage service cho lưu trữ ảnh."""

    def __init__(self, endpoint: str, access_key: str, secret_key: str, bucket: str, secure: bool = False):
        """Khởi tạo MinIO client và tự động tạo bucket nếu chưa tồn tại."""
        self.client = Minio(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        self.bucket = bucket
        
        # Tạo bucket nếu chưa có
        try:
            if not self.client.bucket_exists(self.bucket):
                self.client.make_bucket(self.bucket)
        except Exception as e:
            # Ghi nhận lỗi nhưng không crash ngay khi khởi tạo (đề phòng MinIO chưa sẵn sàng)
            print(f"Warning: Failed to verify/create MinIO bucket '{self.bucket}': {e}")

    def upload_image(self, image_bytes: bytes, filename: str, content_type: str = "image/jpeg") -> str:
        """
        Upload ảnh lên MinIO, trả về object key duy nhất.
        """
        # Tránh xung đột tên file bằng cách gán uuid
        ext = os.path.splitext(filename)[1] or ".jpg"
        object_key = f"{uuid.uuid4()}{ext}"
        
        data = io.BytesIO(image_bytes)
        self.client.put_object(
            bucket_name=self.bucket,
            object_name=object_key,
            data=data,
            length=len(image_bytes),
            content_type=content_type
        )
        return object_key

    def get_url(self, object_key: str, expires_hours: int = 24) -> str:
        """
        Lấy presigned URL để client (Frontend) có thể tải trực tiếp từ MinIO.
        """
        return self.client.presigned_get_object(
            bucket_name=self.bucket,
            object_name=object_key,
            expires=timedelta(hours=expires_hours)
        )
