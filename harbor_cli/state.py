from __future__ import annotations

import asyncio
from typing import Awaitable
from typing import TypeVar

from harborapi import HarborAsyncClient
from harborapi.exceptions import StatusError
from pydantic import BaseModel
from pydantic import Field

from .config import HarborCLIConfig
from .exceptions import handle_status_error

T = TypeVar("T")


class State(BaseModel):
    """Class used to manage the state of the program.

    It is used as a singleton shared between all commands.
    Unlike a context object, the state object is not passed to each
    command, but is instead accessed via the global state variable.
    """

    config: HarborCLIConfig = Field(default_factory=HarborCLIConfig)
    client: HarborAsyncClient = None  # type: ignore # will be patched by the callback
    verbose: bool = False
    loop: asyncio.AbstractEventLoop = Field(default_factory=asyncio.get_event_loop)

    class Config:
        keep_untouched = (asyncio.AbstractEventLoop,)
        arbitrary_types_allowed = True  # HarborAsyncClient
        validate_assignments = True
        extra = "allow"

    def run(
        self,
        coro: Awaitable[T],
        no_handle: type[Exception] | tuple[type[Exception], ...] | None = None,
    ) -> T:
        """Run a coroutine in the event loop.

        Parameters
        ----------
        coro : Awaitable[T]
            The coroutine to run.
        no_handle : type[Exception] | tuple[type[Exception], ...]
            A single exception type or a tuple of exception types that
            should not be passed to the default exception handler.
            Exceptions of this type will be raised as-is.
        """
        try:
            resp = self.loop.run_until_complete(coro)
        except StatusError as e:
            if no_handle and isinstance(e, no_handle):
                raise
            handle_status_error(e)
        return resp


state = State()