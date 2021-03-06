# -*- coding: utf-8 -*-

# Copyright 2015 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extract images from http://www.hentai-foundry.com/"""

from .common import Extractor, Message
from .. import text

class HentaiFoundryUserExtractor(Extractor):
    """Extract all pictures of a hentaifoundry-user"""
    category = "hentaifoundry"
    subcategory = "user"
    directory_fmt = ["{category}", "{artist}"]
    filename_fmt = "{category}_{index}_{title}.{extension}"
    pattern = [
        r"(?:https?://)?(?:www\.)?hentai-foundry\.com/pictures/user/([^/]+)/?$",
        r"(?:https?://)?(?:www\.)?hentai-foundry\.com/user/([^/]+)/profile",
    ]
    test = [("http://www.hentai-foundry.com/pictures/user/Orzy", {
        "url": "236ac02c8f081fee44ad2c2571bf74615633b91e",
        "keyword": "f5f1aa78ecbe390fb117a0b599f771cd47df86c6",
    })]
    url_base = "http://www.hentai-foundry.com/pictures/user/"

    def __init__(self, match):
        Extractor.__init__(self)
        self.artist = match.group(1)

    def items(self):
        data, token = self.get_job_metadata()
        self.set_filters(token)
        yield Message.Version, 1
        yield Message.Directory, data
        for url, image in self.get_images():
            image.update(data)
            yield Message.Url, url, image

    def get_images(self):
        """Yield url and keywords for all images of one artist"""
        num = 1
        while True:
            pos = 0
            url = self.url_base + self.artist + "/page/" + str(num)
            page = self.request(url).text
            for _ in range(25):
                part, pos = text.extract(page, 'thumbTitle"><a href="/pictures/user/', '"', pos)
                if not part:
                    return
                yield self.get_image_metadata(self.url_base + part)
            num += 1

    def get_job_metadata(self):
        """Collect metadata for extractor-job"""
        page = self.request(self.url_base + self.artist + "?enterAgree=1").text
        token, pos = text.extract(page, 'hidden" value="', '"')
        count, pos = text.extract(page, 'class="active" >Pictures (', ')', pos)
        return {
            "category": self.category,
            "artist": self.artist,
            "count": count,
        }, token

    def get_image_metadata(self, url):
        """Collect metadata for an image"""
        page = self.request(url).text
        index = text.extract(url, '/', '/', len(self.url_base) + len(self.artist))[0]
        title, pos = text.extract(page, 'Pictures</a> &raquo; <span>', '<')
        url  , pos = text.extract(page, '//pictures.hentai-foundry.com', '"', pos)
        data = {
            "index": index,
            "title": text.unescape(title),
        }
        return "http://pictures.hentai-foundry.com" + url, text.nameext_from_url(url, data)

    def set_filters(self, token):
        """Set site-internal filters to show all images"""
        formdata = {
            "YII_CSRF_TOKEN": token,
            "rating_nudity": 3,
            "rating_violence": 3,
            "rating_profanity": 3,
            "rating_racism": 3,
            "rating_sex": 3,
            "rating_spoilers": 3,
            "rating_yaoi": 1,
            "rating_yuri": 1,
            "rating_teen": 1,
            "rating_guro": 1,
            "rating_furry": 1,
            "rating_beast": 1,
            "rating_male": 1,
            "rating_female": 1,
            "rating_futa": 1,
            "rating_other": 1,
            "filter_media": "A",
            "filter_order": "date_new",
            "filter_type": 0,
        }
        self.request("http://www.hentai-foundry.com/site/filters",
                     method="post", data=formdata)


class HentaiFoundryImageExtractor(Extractor):
    """Extract a single hentaifoundry picture"""
    category = "hentaifoundry"
    subcategory = "image"
    directory_fmt = ["{category}", "{artist}"]
    filename_fmt = "{category}_{index}_{title}.{extension}"
    pattern = [(r"(?:https?://)?(?:www\.)?hentai-foundry\.com/pictures/user/"
                r"([^/]+)/(\d+)/[^/]+")]
    test = [("http://www.hentai-foundry.com/pictures/user/Orzy/76940/Youmu-Konpaku", {
        "url": "50c267b2b2983b98b18fd0d2acbec8ce5ba64c77",
        "keyword": "8c9b7054b78fb4f52982c3f21f3ba2a9fcdd5428",
    })]

    def __init__(self, match):
        Extractor.__init__(self)
        self.url = match.group(0)
        self.artist = match.group(1)
        self.index = match.group(2)

    def items(self):
        url, data = self.get_image_metadata()
        yield Message.Version, 1
        yield Message.Directory, data
        yield Message.Url, url, data

    def get_image_metadata(self):
        """Collect metadata for an image"""
        page = self.request(self.url + "?enterAgree=1").text
        title, pos = text.extract(page, 'Pictures</a> &raquo; <span>', '<')
        url  , pos = text.extract(page, '//pictures.hentai-foundry.com', '"', pos)
        data = {
            "category": self.category,
            "artist": self.artist,
            "index": self.index,
            "title": text.unescape(title),
        }
        return "http://pictures.hentai-foundry.com" + url, text.nameext_from_url(url, data)
