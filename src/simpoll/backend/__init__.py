from flask import Flask

from .endpoint_ping import endpoint_ping as ping
from .endpoint_question import endpoint_question as question


app = Flask(__name__)

# Register endpoints
app.register_blueprint(ping)
app.register_blueprint(question)
