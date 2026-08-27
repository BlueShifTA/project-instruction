import package.domain.models as pdm


def echo_message(payload: pdm.ExampleEchoRequest) -> pdm.ExampleEchoResponse:
    return pdm.ExampleEchoResponse(message=payload.message, length=len(payload.message))
