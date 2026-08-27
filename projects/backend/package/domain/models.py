import pydantic


class ExampleEchoRequest(pydantic.BaseModel):
    message: str = pydantic.Field(min_length=1, max_length=500)


class ExampleEchoResponse(pydantic.BaseModel):
    message: str
    length: int
