from fastapi import APIRouter
from modules import documents, templates

router = APIRouter()

router.include_router(templates.router)
router.include_router(documents.router)
