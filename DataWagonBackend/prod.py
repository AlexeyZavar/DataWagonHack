import signal
import sys

from gevent import signal_handler
from gevent.pywsgi import WSGIServer

from app import app

http_server = WSGIServer(("0.0.0.0", 5000), app)


def shutdown():
    http_server.stop(2)
    sys.exit(signal.SIGTERM)


signal_handler(signal.SIGTERM, shutdown)
signal_handler(signal.SIGINT, shutdown)

http_server.serve_forever()
