import json
import os
import sys
from typing import Dict

from line import Line


def handler(event: Dict, context):
    _check_envs()

    print(event)

    body = json.loads(event["body"])
    line_message: Dict = body["line_message"]  # json dict string
    print(line_message)

    line = Line()
    line.push_message_ex(line_message)

    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {},
        "body": "ok. done.",
    }


def _check_envs():
    task_root = _check_env("LAMBDA_TASK_ROOT", is_check=False)
    home = _check_env("HOME", is_check=False)
    _check_env("LINE_CHANNEL_ACCESS_TOKEN")
    _check_env("LINE_SEND_ID_1")
    _check_env("LINE_SEND_GROUP_ID_1")

    if False:
        os.system(f"ls -al {task_root}")
        os.system(f"ls -al {home}")


def _check_env(key: str, is_check: bool = True) -> str:
    value = os.environ.get(key, "")
    if is_check:
        if not value:
            print(f"Not found environment variable: ({key} = {value})")
            sys.exit(1)
    print(f"env | {key}: {value}")
    return value
