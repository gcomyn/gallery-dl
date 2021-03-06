# -*- coding: utf-8 -*-

# Copyright 2015 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extract images from http://nhentai.net/"""

from .common import Extractor, Message
from .. import text
import json

class NhentaiExtractor(Extractor):

    category = "nhentai"
    directory_fmt = ["{category}", "{gallery-id} {title}"]
    filename_fmt = "{category}_{gallery-id}_{num:>03}.{extension}"
    pattern = [r"(?:https?://)?(?:www\.)?nhentai\.net/g/(\d+)"]
    test = [("http://nhentai.net/g/147850/", {
        "url": "199ddd07dded0f69282e09a372710698ea21ab8e",
        "keyword": "e00678567c8335289ffcbb2e6980b28d332ee6a7",
    })]

    def __init__(self, match):
        Extractor.__init__(self)
        self.gid = match.group(1)

    def items(self):
        ginfo = self.get_gallery_info()
        data = self.get_job_metadata(ginfo)
        urlbase = "http:{}galleries/{}/".format(ginfo["media_url"], data["media-id"])
        extdict = {"j": "jpg", "p": "png", "g": "gif"}
        yield Message.Version, 1
        yield Message.Directory, data
        for num, image in enumerate(ginfo["images"]["pages"], 1):
            ext = extdict.get(image["t"], "jpg")
            data["num"] = num
            data["width"] = image["w"]
            data["height"] = image["h"]
            data["extension"] = ext
            yield Message.Url, "{}{}.{}".format(urlbase, num, ext), data

    def get_gallery_info(self):
        """Extract and return gallery-info"""
        page = self.request("http://nhentai.net/g/" + self.gid + "/1/").text
        media_url, pos = text.extract(page, ".reader({\n\t\t\tmedia_url: '", "'")
        json_data, pos = text.extract(page, "gallery: ", ",\n", pos)
        json_dict = json.loads(json_data)
        json_dict["media_url"] = media_url
        return json_dict

    def get_job_metadata(self, ginfo):
        """Collect metadata for extractor-job"""
        title_en = ginfo["title"].get("english", "")
        title_ja = ginfo["title"].get("japanese", "")
        return {
            "category": self.category,
            "gallery-id": self.gid,
            "upload-date": ginfo["upload_date"],
            "media-id": ginfo["media_id"],
            "scanlator": ginfo["scanlator"],
            "count": ginfo["num_pages"],
            "title": title_en or title_ja,
            "title-en": title_en,
            "title-ja": title_ja,
        }
