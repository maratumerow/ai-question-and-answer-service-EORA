import logging

from fastapi import APIRouter, Depends

from src.application.dto.requests import LoadSourcesRequest
from src.application.dto.responses import LoadSourcesResponse
from src.application.use_cases import LoadSourcesUseCase
from src.presentation.dependencies import get_load_sources_use_case

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/load",
    response_model=LoadSourcesResponse,
)
async def load_sources(
    request: LoadSourcesRequest,
    use_case: LoadSourcesUseCase = Depends(get_load_sources_use_case),
) -> LoadSourcesResponse:
    """Load sources from URLs."""

    logger.info("Starting with %d URLs", len(request.urls))

    response = await use_case.execute(request.urls)

    logger.info(
        "Loaded %d sources, failed: %d",
        response.loaded_count,
        response.failed_count,
    )

    return response
