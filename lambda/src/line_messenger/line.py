import json
import os
from typing import Dict, List

import requests


class Line:
    def __init__(self) -> None:
        # id = os.environ["LINE_SEND_ID_1"]
        id: str = os.environ["LINE_SEND_GROUP_ID_1"]
        self._send_ids: List[str] = [id]

    def push_message_ex(self, message: Dict) -> None:
        for id in self._send_ids:
            payload = {
                "to": id,
                "messages": [message],
            }
            try:
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer {{{0}}}".format(
                        os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
                    ),
                }
                requests.post(
                    "https://api.line.me/v2/bot/message/push",
                    data=json.dumps(payload),
                    headers=headers,
                )
            except requests.exceptions.RequestException as e:
                print("request failed: {}".format(e))
