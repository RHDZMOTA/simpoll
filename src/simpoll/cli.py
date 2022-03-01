import os
import sys
import time
import json
import textwrap
from typing import Any, Optional

from .utils import temp_file
from .settings import (
    get_logger,
    SIMPOLL_DEFAULT_HELLO_WORLD,
    SIMPOLL_FLASK_HOST,
    SIMPOLL_FLASK_PORT,
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

    def frontend(self):
        import importlib

        # Create temporal path
        temp_file_path = temp_file(
            suffix=".py",
            content=textwrap.dedent(
                """
                from simpoll.frontend.main import main


                if __name__ == "__main__":
                    main()
                """
            )
        )
        try:
            streamlit_cli = importlib.import_module("streamlit.cli")
            sys.argv = ["streamlit", "run", temp_file_path]
            streamlit_cli.main()
        except Exception as e:
            logger.error(e)
        finally:
            if os.path.isfile(temp_file_path):
                os.remove(temp_file_path)
                logger.warning("Temporary file correctly deleted: %s", temp_file_path)

    def backend(
            self,
            host: Optional[str] = None,
            port: Optional[str] = None,
            debug: bool = False,
            production: bool = False,
    ):
        # Default values
        host = host or SIMPOLL_FLASK_HOST
        port = port or SIMPOLL_FLASK_PORT
        # Ge server & flask application
        from simpoll.backend import app
        if not production:
            return app.run(
                host=host,
                port=port,
                debug=debug,
            )
        from waitress import serve
        return serve(
            app,
            host=host,
            port=port,
        )
