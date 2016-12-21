import json
from typing import Optional, Tuple

from flask import request, abort

from webhookforwarder import app
from webhookforwarder.config import Config, IconType
from webhookforwarder.constants import INCOMING, OUTGOING
from webhookforwarder.network import post_json
from webhookforwarder.request import Request

try:
    from webhookforwarder.settings import forward_configs
except ImportError:
    forward_configs = []


def find_forward_config(identity: str) -> Optional[Config]:
    result = list(c for c in forward_configs if c.identity == identity)
    if len(result) == 1:
        return result[0]
    else:
        return None


def generate_forward_payload(req: Request, config: Config) -> str:
    text = config.forward_func(req)
    body = {INCOMING.USER_NAME: req.user_name, INCOMING.TEXT: text}
    if req.user_id in config.icon_dict:
        (icon_type, icon_value) = config.icon_dict[req.user_id]
        if icon_type == IconType.emoji:
            body[INCOMING.ICON_EMOJI] = icon_value
        else:
            body[INCOMING.ICON_URL] = icon_value
    return json.dumps(body)


def generate_response_payload(req: Request, config: Config) -> str:
    if not config.response_func:
        return ''
    payload = {OUTGOING.TEXT: config.response_func(req)}
    if config.response_name_func:
        payload[INCOMING.USER_NAME] = config.response_name_func(req)
    return json.dumps(payload)


@app.route('/webhook-forwarder', methods=['POST'])
def forwarder() -> Tuple[str, int]:
    request_ = Request.generate_request(request.form)
    config = find_forward_config(request_.identity)
    if not config:  # There is no configuration
        abort(400)
    elif config.token != request_.token:
        abort(400)
    elif config.user_ids and request_.user_id not in config.user_ids:
        # The message isn't needed to forward because of user_id restriction
        abort(400)

    forward_payload = generate_forward_payload(request_, config)
    post_json(forward_payload, config.forward_to)

    response = generate_response_payload(request_, config)
    return response, 200 if request else 204
