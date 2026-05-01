"""
S3兼容存储实现
支持任意S3兼容的云存储服务
"""
import os
import re
from pathlib import Path
from typing import Optional, Any, Dict, List, TypedDict, Iterable
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError
from boto3.s3.transfer import TransferConfig
import logging

logger = logging.getLogger(__name__)

# 允许的文件名字符集
FILE_NAME_ALLOWED_RE = re.compile(r"^[A-Za-z0-9._\-/]+$")


class ListFilesResult(TypedDict):
    keys: List[str]
    is_truncated: bool
    next_continuation_token: Optional[str]


class S3SyncStorage:
    """S3兼容存储实现"""

    def __init__(
        self,
        *,
        endpoint_url: Optional[str] = None,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        bucket_name: str = "",
        region: str = "us-east-1",
    ):
        # 从环境变量或参数获取配置
        self.endpoint_url = (
            os.getenv("S3_ENDPOINT_URL")
            or os.getenv("AWS_S3_ENDPOINT_URL")
            or endpoint_url
            or ""
        )
        self.access_key = (
            access_key
            or os.getenv("AWS_ACCESS_KEY_ID")
            or os.getenv("S3_ACCESS_KEY_ID")
            or ""
        )
        self.secret_key = (
            secret_key
            or os.getenv("AWS_SECRET_ACCESS_KEY")
            or os.getenv("S3_SECRET_ACCESS_KEY")
            or ""
        )
        self.bucket_name = (
            bucket_name
            or os.getenv("S3_BUCKET_NAME")
            or os.getenv("AWS_BUCKET_NAME")
            or ""
        )
        self.region = region or os.getenv("AWS_REGION", "us-east-1")
        self._client = None

    def _get_client(self):
        if self._client is None:
            kwargs: Dict[str, Any] = {
                "region_name": self.region,
            }
            
            # 配置endpoint（用于兼容S3兼容存储如MinIO、阿里云OSS等）
            if self.endpoint_url:
                kwargs["endpoint_url"] = self.endpoint_url
            
            # 配置凭证
            if self.access_key and self.secret_key:
                kwargs["aws_access_key_id"] = self.access_key
                kwargs["aws_secret_access_key"] = self.secret_key
            
            self._client = boto3.client("s3", **kwargs)
        
        return self._client

    def _generate_object_key(self, *, original_name: str) -> str:
        suffix = Path(original_name).suffix.lower()
        stem = Path(original_name).stem
        uniq = uuid4().hex[:8]
        return f"{stem}_{uniq}{suffix}"

    def _extract_logid(self, e: Exception) -> Optional[str]:
        if isinstance(e, ClientError):
            headers = (e.response or {}).get("ResponseMetadata", {}).get("HTTPHeaders", {})
            return headers.get("x-tt-logid")
        return None

    def _error_msg(self, msg: str, e: Exception) -> str:
        logid = self._extract_logid(e)
        if logid:
            return f"{msg}: {e} (x-tt-logid: {logid})"
        return f"{msg}: {e}"

    def _resolve_bucket(self, bucket: Optional[str]) -> str:
        target_bucket = bucket or self.bucket_name
        if not target_bucket:
            raise ValueError("未配置bucket：请传入bucket或设置S3_BUCKET_NAME")
        return target_bucket

    def _validate_file_name(self, name: str) -> None:
        """校验文件名"""
        msg = "file name invalid: 文件名需满足以下规范："
        
        if not name or not name.strip():
            raise ValueError(msg + "（原因：文件名为空）")
        
        if len(name.encode("utf-8")) > 1024:
            raise ValueError(msg + "（原因：长度超过1024字节）")
        
        if name.startswith("/") or name.endswith("/"):
            raise ValueError(msg + "（原因：以/开头或结尾）")
        
        if "//" in name:
            raise ValueError(msg + "（原因：包含连续的//）")
        
        if not FILE_NAME_ALLOWED_RE.match(name):
            bad = re.findall(r"[^A-Za-z0-9._\-/]", name)
            example = bad[0] if bad else "非法字符"
            raise ValueError(msg + f"（原因：包含非法字符，例如：{example}）")

    def upload_file(
        self,
        *,
        file_content: bytes,
        file_name: str,
        content_type: str = "application/octet-stream",
        bucket: Optional[str] = None,
    ) -> str:
        self._validate_file_name(file_name)
        
        try:
            client = self._get_client()
            object_key = self._generate_object_key(original_name=file_name)
            target_bucket = self._resolve_bucket(bucket)
            
            client.put_object(
                Bucket=target_bucket,
                Key=object_key,
                Body=file_content,
                ContentType=content_type,
            )
            return object_key
        except Exception as e:
            logger.error(self._error_msg("Error uploading file to S3", e))
            raise e

    def delete_file(self, *, file_key: str, bucket: Optional[str] = None) -> bool:
        try:
            client = self._get_client()
            target_bucket = self._resolve_bucket(bucket)
            client.delete_object(Bucket=target_bucket, Key=file_key)
            return True
        except Exception as e:
            logger.error(self._error_msg("Error deleting file from S3", e))
            raise e

    def file_exists(self, *, file_key: str, bucket: Optional[str] = None) -> bool:
        try:
            client = self._get_client()
            target_bucket = self._resolve_bucket(bucket)
            client.head_object(Bucket=target_bucket, Key=file_key)
            return True
        except ClientError as e:
            code = (e.response or {}).get("Error", {}).get("Code", "")
            if code in {"404", "NoSuchKey", "NotFound"}:
                return False
            logger.error(self._error_msg("Error checking file existence", e))
            return False
        except Exception as e:
            logger.error(self._error_msg("Error checking file existence", e))
            return False

    def read_file(self, *, file_key: str, bucket: Optional[str] = None) -> bytes:
        try:
            client = self._get_client()
            target_bucket = self._resolve_bucket(bucket)
            resp = client.get_object(Bucket=target_bucket, Key=file_key)
            body = resp.get("Body")
            if body is None:
                raise RuntimeError("S3 get_object returned no Body")
            try:
                return body.read()
            finally:
                try:
                    body.close()
                except Exception:
                    pass
        except Exception as e:
            logger.error(self._error_msg("Error reading file from S3", e))
            raise e

    def list_files(
        self,
        *,
        prefix: Optional[str] = None,
        bucket: Optional[str] = None,
        max_keys: int = 1000,
        continuation_token: Optional[str] = None,
    ) -> ListFilesResult:
        try:
            client = self._get_client()
            target_bucket = self._resolve_bucket(bucket)
            
            if max_keys <= 0 or max_keys > 1000:
                raise ValueError("max_keys必须在1到1000之间")
            
            kwargs: Dict[str, Any] = {
                "Bucket": target_bucket,
                "MaxKeys": max_keys,
                "Prefix": prefix or "",
                "ContinuationToken": continuation_token,
            }
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            
            resp = client.list_objects_v2(**kwargs)
            contents = resp.get("Contents", []) or []
            keys = [item.get("Key") for item in contents if isinstance(item, dict) and item.get("Key")]
            
            return {
                "keys": keys,
                "is_truncated": bool(resp.get("IsTruncated")),
                "next_continuation_token": resp.get("NextContinuationToken"),
            }
        except Exception as e:
            logger.error(self._error_msg("Error listing files in S3", e))
            raise e

    def generate_presigned_url(self, *, key: str, bucket: Optional[str] = None, expire_time: int = 1800) -> str:
        try:
            client = self._get_client()
            target_bucket = self._resolve_bucket(bucket)
            
            url = client.generate_presigned_url(
                "get_object",
                Params={"Bucket": target_bucket, "Key": key},
                ExpiresIn=expire_time,
            )
            return url
        except Exception as e:
            raise RuntimeError(f"生成签名URL失败: {e}")

    def stream_upload_file(
        self,
        *,
        fileobj,
        file_name: str,
        content_type: str = "application/octet-stream",
        bucket: Optional[str] = None,
    ) -> str:
        try:
            client = self._get_client()
            target_bucket = self._resolve_bucket(bucket)
            key = self._generate_object_key(original_name=file_name)
            
            extra_args = {"ContentType": content_type} if content_type else {}
            
            config = TransferConfig(
                multipart_chunksize=5 * 1024 * 1024,  # 5MB
                multipart_threshold=5 * 1024 * 1024,
            )
            
            client.upload_fileobj(
                Fileobj=fileobj,
                Bucket=target_bucket,
                Key=key,
                ExtraArgs=extra_args,
                Config=config,
            )
            return key
        except Exception as e:
            logger.error(self._error_msg("Error streaming upload to S3", e))
            raise e

    def upload_from_url(self, *, url: str, bucket: Optional[str] = None, timeout: int = 30) -> str:
        import urllib.request as urllib_request
        from urllib.parse import urlparse, unquote
        
        try:
            request = urllib_request.Request(url)
            with urllib_request.urlopen(request, timeout=timeout) as resp:
                parsed = urlparse(url)
                file_name = Path(unquote(parsed.path)).name or "file"
                content_type = resp.headers.get("Content-Type", "application/octet-stream")
                
                return self.stream_upload_file(
                    fileobj=resp,
                    file_name=file_name,
                    content_type=content_type,
                    bucket=bucket,
                )
        except Exception as e:
            logger.error(self._error_msg("Error uploading from URL to S3", e))
            raise e
