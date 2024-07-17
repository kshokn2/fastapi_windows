# fastapi
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from enum import Enum

class TestRouter(str, Enum):
    add = "add"
    remove = "remove"

test_router = APIRouter(prefix="/test") # prefix="/"

# example url : http://ip:port/test/add
@test_router.get("/{source}")
async def myfunc(source: TestRouter):
    """
    functions in this router
    """

    if source.value == "add":
        val = "func1"
        """
        simple function about add operation
        """
    elif source.value == "remove":
        val = "func2"
        """
        simple function about remove operation
        """
    else:
        val = "other_func"

    result = {"result": True, "value": val}

    return JSONResponse(conetent=result)