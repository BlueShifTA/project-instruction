from __future__ import annotations

from package.domain.models import ExampleEchoRequest, ExampleEchoResponse


def echo_message(payload: ExampleEchoRequest) -> ExampleEchoResponse:
    return ExampleEchoResponse(message=payload.message, length=len(payload.message))
