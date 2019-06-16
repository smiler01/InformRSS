# coding: utf-8
import urllib.request
import json

import logger


class SlackInform(object):

    def __init__(self, webhook_url):
        self.WEBHOOK_URL = webhook_url
        self.METHOD = "POST"
        self.HEADERS = {'Content-Type': 'application/json; charset=utf-8'}
        self.COLOR_LIST = ["danger", "warning", "", "good", "hex"]

        self.log = logger.Logger(target_file_path=__name__)

    def format_app_review_attachments(self, app_name, review):

        updated = review["updated"]
        username = review["username"]
        title = review["title"]
        summary = review["summary"]
        rating = review["rating"]
        version = review["version"]

        attachments = {
            "attachments": [
                {
                    "fallback": "This is rss reviews attachments",
                    "color": self.COLOR_LIST[int(rating)-1],
                    "pretext": "{}の新着レビューです！！".format(app_name),
                    "fields": [
                        {
                            "title": "User",
                            "value": username
                        },
                        {
                            "title": "Title",
                            "value": title,
                        },
                        {
                            "title": "Review",
                            "value": summary
                        },
                        {
                            "title": "Rating",
                            "value": ":star:"*int(rating),
                            "short": "true"
                        },
                        {
                            "title": "Version",
                            "value": version,
                            "short": "true"
                        }
                    ],
                    "footer": updated
                }
            ]
        }

        return attachments

    def inform(self, attachments):

        request = urllib.request.Request(
            url=self.WEBHOOK_URL,
            data=json.dumps(attachments).encode("utf-8"),
            method="POST",
            headers=self.HEADERS
        )

        try:
            with urllib.request.urlopen(request) as response:
                result = response.read().decode("utf-8")
                self.log.logger.info("{}, inform latest reviews".format(result))
                print(result)
        except urllib.error.HTTPError as err:
            print("HTTPError: {}".format(err.code))
            self.log.logger.error("HTTPError: {}".format(err.code))
        except urllib.error.URLError as err:
            print("URLError: {}".format(err.reason))
            self.log.logger.error("URLError: {}".format(err.reason))

