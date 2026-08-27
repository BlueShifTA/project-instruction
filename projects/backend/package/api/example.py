import fastapi

import package.domain.models as pdm
import package.services.example as pse

router = fastapi.APIRouter(prefix="/example", tags=["example"])


@router.post("/echo", response_model=pdm.ExampleEchoResponse)
def echo(payload: pdm.ExampleEchoRequest) -> pdm.ExampleEchoResponse:
    return pse.echo_message(payload)
