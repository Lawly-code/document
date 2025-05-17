from pathlib import Path
from repositories.s3_repository import S3Object


TEMPLATE_PATH = Path(__file__).parent.parent / "data" / "template.docx"

with open(TEMPLATE_PATH, "rb") as f:
    LOCAL_TEMPLATE_BYTES = f.read()

LOCAL_TEMPLATE_OBJ = S3Object(
    body=LOCAL_TEMPLATE_BYTES,
    content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
)
