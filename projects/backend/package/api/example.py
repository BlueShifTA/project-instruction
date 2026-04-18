from fastapi import APIRouter

from package.domain.models import ExampleEchoRequest, ExampleEchoResponse
from package.services.example import echo_message

router = APIRouter(prefix="/example", tags=["example"])


@router.post("/echo", response_model=ExampleEchoResponse)
def echo(payload: ExampleEchoRequest) -> ExampleEchoResponse:
    return echo_message(payload)
