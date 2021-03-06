# -*- coding: utf-8 -*-

# Copyright 2015 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

"""Extract image-urls from https://konachan.com/"""

from . import booru

class KonachanExtractor(booru.JSONBooruExtractor):
    """Base class for konachan extractors"""
    category = "konachan"
    api_url = "https://konachan.com/post.json"

class KonachanTagExtractor(KonachanExtractor, booru.BooruTagExtractor):
    """Extract images from konachan based on search-tags"""
    subcategory = "tag"
    pattern = [r"(?:https?://)?(?:www\.)?konachan\.com/post\?tags=([^&]+)"]
    test = [("http://konachan.com/post?tags=patata", {
        "content": "838cfb815e31f48160855435655ddf7bfc4ecb8d",
    })]

class KonachanPoolExtractor(KonachanExtractor, booru.BooruPoolExtractor):
    """Extract image-pools from konachan"""
    subcategory = "pool"
    pattern = [r"(?:https?://)?(?:www\.)?konachan\.com/pool/show/(\d+)"]
    test = [("http://konachan.com/pool/show/95", {
        "content": "cf0546e38a93c2c510a478f8744e60687b7a8426",
    })]

class KonachanPostExtractor(KonachanExtractor, booru.BooruPostExtractor):
    """Extract single images from konachan"""
    subcategory = "post"
    pattern = [r"(?:https?://)?(?:www\.)?konachan\.com/post/show/(\d+)"]
    test = [("http://konachan.com/post/show/205189", {
        "content": "674e75a753df82f5ad80803f575818b8e46e4b65",
    })]
