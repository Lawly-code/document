from datetime import datetime
from typing import Union

import aioboto3
import boto3
from pydantic import BaseModel, ConfigDict
from urllib.parse import urlparse
from aiohttp import ClientResponse

from config import settings


class S3Object(BaseModel):
    """
    A Pydantic model representing an S3 object.

    Attributes:
        body (bytes): The content of the S3 object.
        content_type (str): The MIME type of the S3 object.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    body: bytes
    content_type: str


class S3ObjectLocation(BaseModel):
    bucket: str
    key: str


class S3Client:
    """
    A client for interacting with S3.

    This client provides methods for getting and uploading objects to S3.
    """

    @staticmethod
    async def get_object(bucket: str, key: str) -> S3Object | None:
        """
        Get an object from S3.

        This method retrieves an object from S3 and returns it as an S3Object.

        Args:
            bucket (str): The name of the S3 bucket.
            key (str): The key of the S3 object.

        Returns:
            S3Object: The retrieved S3 object.
        """
        session = aioboto3.Session()
        async with session.resource(
            's3',
            endpoint_url=settings.s3_settings.endpoint_url,
            config=boto3.session.Config(signature_version='s3v4'),
            aws_access_key_id=settings.s3_settings.access_key,
            aws_secret_access_key=settings.s3_settings.secret_key,
        ) as s3:
            bucket = await s3.Bucket(bucket)
            obj = await bucket.Object(key)
            try:
                content: dict[
                    str, Union[str, ClientResponse, dict, datetime]
                ] = await obj.get()
            except s3.meta.client.exceptions.NoSuchKey:
                return None
            return S3Object(
                body=await content.get("Body").read(),
                content_type=content.get("ContentType"),
            )

    @staticmethod
    async def upload_object(
        bucket: str, key: str, data: bytes, content_type: str
    ) -> None:
        """
        Upload an object to S3.

        This method uploads an object to S3.

        Args:
            bucket (str): The name of the S3 bucket.
            key (str): The key of the S3 object.
            data (bytes): The content of the S3 object.
            content_type (str): The MIME type of the S3 object.
        """
        session = aioboto3.Session()
        async with session.resource(
            's3',
            endpoint_url=settings.s3_settings.endpoint_url,
            config=boto3.session.Config(signature_version='s3v4'),
            aws_access_key_id=settings.s3_settings.access_key,
            aws_secret_access_key=settings.s3_settings.secret_key,
        ) as s3:
            bucket = await s3.Bucket(bucket)
            await bucket.put_object(Key=key, Body=data, ContentType=content_type)

    @staticmethod
    async def delete_object(bucket: str, key: str) -> bool:
        """
        Delete an object from S3.

        This method deletes an object from S3.

        Args:
            bucket (str): The name of the S3 bucket.
            key (str): The key of the S3 object.
        """
        session = aioboto3.Session()
        async with session.resource(
            's3',
            endpoint_url=settings.s3_settings.endpoint_url,
            config=boto3.session.Config(signature_version='s3v4'),
            aws_access_key_id=settings.s3_settings.access_key,
            aws_secret_access_key=settings.s3_settings.secret_key,
        ) as s3:
            bucket = await s3.Bucket(bucket)
            try:
                await (await bucket.Object(key)).delete()
            except s3.meta.client.exceptions.NoSuchKey:
                return False
        return True

    @staticmethod
    def from_url(url: str) -> S3ObjectLocation:
        parsed_url = urlparse(url)
        path_parts = parsed_url.path.strip("/").split("/", 1)

        if len(path_parts) < 2:
            raise ValueError("URL не содержит бакет и key в правильном формате")

        bucket = path_parts[0]
        key = path_parts[1]

        return S3ObjectLocation(bucket=bucket, key=key)
