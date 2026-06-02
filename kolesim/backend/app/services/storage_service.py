import uuid

from botocore.config import Config
import boto3

from app.core.config import settings

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    endpoint_url=settings.S3_ENDPOINT,
    region_name=settings.S3_REGION,
    config=Config(signature_version="s3v4"),
)

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
MAX_BYTES = 10 * 1024 * 1024


def _validate_upload(file_bytes: bytes, content_type: str) -> None:
    if content_type not in ALLOWED_TYPES:
        raise ValueError("Недопустимый тип файла")
    if len(file_bytes) > MAX_BYTES:
        raise ValueError("Файл превышает 10 MB")


async def upload_file(file_bytes: bytes, content_type: str, folder: str = "media") -> str:
    _validate_upload(file_bytes, content_type)
    file_key = f"{folder}/{uuid.uuid4()}"
    s3_client.put_object(
        Bucket=settings.S3_BUCKET,
        Key=file_key,
        Body=file_bytes,
        ContentType=content_type,
        ACL="public-read",
    )
    return f"{settings.S3_ENDPOINT}/{settings.S3_BUCKET}/{file_key}"
