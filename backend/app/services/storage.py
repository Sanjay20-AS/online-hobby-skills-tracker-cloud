from pathlib import Path
import uuid, boto3
from app.core.config import settings

class StorageService:
    def __init__(self):
        self.cloud = bool(settings.s3_endpoint_url and settings.s3_access_key and settings.s3_secret_key)
        self.local_dir = Path("uploads")
        self.local_dir.mkdir(exist_ok=True)

    def save(self, content: bytes, original_name: str, content_type: str):
        ext = Path(original_name).suffix.lower()
        name = f"{uuid.uuid4().hex}{ext}"
        if self.cloud:
            client=boto3.client(
                "s3", endpoint_url=settings.s3_endpoint_url,
                aws_access_key_id=settings.s3_access_key,
                aws_secret_access_key=settings.s3_secret_key,
                region_name=settings.s3_region)
            client.put_object(Bucket=settings.s3_bucket, Key=name, Body=content, ContentType=content_type)
            return name, f"{settings.s3_endpoint_url}/{settings.s3_bucket}/{name}"
        path=self.local_dir/name
        path.write_bytes(content)
        return name, f"/uploads/{name}"

storage=StorageService()
