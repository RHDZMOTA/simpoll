import time
import json
from typing import Any, Optional

from .settings import (
    get_logger,
    SIMPOLL_DEFAULT_HELLO_WORLD,
)


logger = get_logger(name=__name__)


class CLI:

    def __init__(self):
        self.start = time.time()

    def display(self, output: Any):
        output_string = output if isinstance(output, str) else json.dumps(output, indent=4, default=str)
        print(f"Result ({round(time.time() - self.start, 4)} seconds):\n\n {output_string}")

    def hello(self, world: Optional[str] = None):
        world = world or SIMPOLL_DEFAULT_HELLO_WORLD
        self.display(f"Hello, {world}!")
