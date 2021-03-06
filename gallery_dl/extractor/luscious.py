# -*- coding: utf-8 -*-

# Copyright 2016 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extract images from https://luscious.net/"""

from .common import Extractor, Message
from .. import text, iso639_1
from urllib.parse import urljoin

class LusciousExtractor(Extractor):

    category = "luscious"
    directory_fmt = ["{category}", "{gallery-id} {title}"]
    filename_fmt = "{category}_{gallery-id}_{num:>03}.{extension}"
    pattern = [(r"(?:https?://)?(?:www\.)?luscious\.net/c/([^/]+)/"
                r"(?:pictures/album|albums)/([^/\d]+(\d+))")]
    test = [("https://luscious.net/c/incest_manga/albums/amazon-no-hiyaku-amazon-elixir-english-decensored_261127/view/", {
        "url": "319a70261de12620d123add9b519d15b8515b503",
        "keyword": "60cc15db2619b8aee47c1527b6326be5a54f5c2f",
    })]

    def __init__(self, match):
        Extractor.__init__(self)
        self.section, self.gpart, self.gid = match.groups()

    def items(self):
        data = self.get_job_metadata()
        yield Message.Version, 1
        yield Message.Directory, data
        for url, image in self.get_images():
            image.update(data)
            yield Message.Url, url, image

    def get_job_metadata(self):
        """Collect metadata for extractor-job"""
        url = "https://luscious.net/c/{}/albums/{}/view/".format(
            self.section, self.gpart)
        data = text.extract_all(self.request(url).text, (
            ("title"   , '"og:title" content="', '"'),
            (None      , '<li class="user_info">', ''),
            ("count"   , '<p>', ' '),
            (None      , '<p>Section:', ''),
            ("section" , '>', '<'),
            (None      , '<p>Language:', ''),
            ("language", '\n                            ', ' '),
            ("artist"  , 'rtist: ', '\n'),
        ), values={"category": self.category, "gallery-id": self.gid})[0]
        data["lang"] = iso639_1.language_to_code(data["language"])
        return data

    def get_images(self):
        pnum = 1
        inum = 1
        apiurl = ("https://luscious.net/c/{}/pictures/album/{}/page/{{}}/.json"
                  "/?style=default").format(self.section, self.gpart)
        while True:
            data = self.request(apiurl.format(pnum)).json()
            for doc in data["documents"]:
                width, height, _, url = doc["sizes"][-1]
                yield urljoin("https:", url), {
                    "width": width,
                    "height": height,
                    "num": inum,
                    "name": doc["title"],
                    "extension": url[url.rfind(".")+1:],
                }
                inum += 1
            if data["paginator_complete"]:
                return
            pnum += 1
