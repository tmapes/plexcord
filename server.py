import json
from pprint import pprint

from flask import Flask, request

from services import WebhookHandlerService


def create_http_server(webhook_handler_service: WebhookHandlerService) -> Flask:
    app = Flask(__name__)

    @app.post("/hooks")
    def hello_world():
        if not request.form.get('payload'):
            print('missing payload')
            return '', 400
        try:
            webhook = json.loads(request.form.get('payload'))
            webhook_handler_service.process_hook(webhook)
            return '', 202
        except json.JSONDecodeError as e:
            pprint(e)
            return '', 500

    return app


if __name__ == '__main__':
    raise RuntimeError("DO NOT RUN ME")
