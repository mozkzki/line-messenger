import json
from typing import Dict

import pytest
from index import handler


@pytest.fixture()
def apigw_event() -> Dict:
    """Generates API GW Event"""

    return {
        "body": None,
        "resource": "/{proxy+}",
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012",
            "identity": {
                "apiKey": "",
                "userArn": "",
                "cognitoAuthenticationType": "",
                "caller": "",
                "userAgent": "Custom User Agent String",
                "user": "",
                "cognitoIdentityPoolId": "",
                "cognitoIdentityId": "",
                "cognitoAuthenticationProvider": "",
                "sourceIp": "127.0.0.1",
                "accountId": "",
            },
            "stage": "prod",
        },
        "queryStringParameters": {"foo": "bar"},
        "headers": {
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch",
        },
        "pathParameters": {"proxy": "/examplepath"},
        "httpMethod": "POST",
        "stageVariables": {"baz": "qux"},
        "path": "/examplepath",
    }


def test_handler_text_message(apigw_event: Dict) -> None:
    apigw_event["body"] = json.dumps(
        {"line_message": {"type": "text", "text": "Hello World!!!!!!!!!!!!!!"}}
    )

    ret = handler(apigw_event, "")
    assert ret["statusCode"] == 200
    assert ret["body"] == "done."


def test_handler_template_message(apigw_event: Dict) -> None:
    apigw_event["body"] = json.dumps(
        {
            "line_message": {
                "type": "template",
                "altText": "alt text",
                "template": {
                    "type": "buttons",
                    "thumbnailImageUrl": "https://upload.wikimedia.org/wikipedia/commons/d/d9/Test.png",  # noqa
                    "imageAspectRatio": "rectangle",
                    "imageSize": "cover",
                    "imageBackgroundColor": "#FFFFFF",
                    "title": "タイトルです。",
                    "text": "内容です。",
                    "actions": [
                        {"type": "uri", "label": "YouTubeへ", "uri": "https://www.youtube.com/"}
                    ],
                },
            }
        }
    )

    ret = handler(apigw_event, "")
    assert ret["statusCode"] == 200
    assert ret["body"] == "done."
