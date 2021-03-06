# -*- coding: utf-8 -*-

# Copyright 2015 Mike Fährmann
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.

import re
import importlib
from .. import config

modules = [
    "pixiv",
    "3dbooru",
    "4chan",
    "8chan",
    "batoto",
    "chronos",
    "danbooru",
    "deviantart",
    "doujinmode",
    "e621",
    "exhentai",
    "gelbooru",
    "hbrowse",
    "hentai2read",
    "hentaifoundry",
    "hitomi",
    "imagebam",
    "imagetwist",
    "imgbox",
    "imgchili",
    "imgth",
    "imgur",
    "imgyt",
    "khinsider",
    "kissmanga",
    "konachan",
    "luscious",
    "mangahere",
    "mangamint",
    "mangapanda",
    "mangapark",
    "mangareader",
    "mangashare",
    "mangastream",
    "nhentai",
    "nijie",
    "powermanga",
    "safebooru",
    "sankaku",
    "senmanga",
    "spectrumnexus",
    "tumblr",
    "turboimagehost",
    "yandere",
    "generic",
]

def find(url):
    """Find suitable extractor for the given url"""
    for pattern, klass in _list_patterns():
        match = re.match(pattern, url)
        if match:
            return klass(match)
    return None

def extractors():
    """Yield all available extractor classes"""
    return sorted(
        set(klass for _, klass in _list_patterns()),
        key=lambda x: x.__name__
    )

# --------------------------------------------------------------------
# internals

_cache = []
_module_iter = iter(modules)

def _list_patterns():
    """Yield all available (pattern, class) tuples"""
    for entry in _cache:
        yield entry

    for module_name in _module_iter:
        module = importlib.import_module("."+module_name, __package__)
        tuples = [
            (pattern, klass)
            for klass in _get_classes(module)
            for pattern in klass.pattern
        ]
        _cache.extend(tuples)
        for etuple in tuples:
            yield etuple

def _get_classes(module):
    """Return a list of all extractor classes in a module"""
    return [
        klass for klass in module.__dict__.values() if (
            hasattr(klass, "pattern") and klass.__module__ == module.__name__
        )
    ]
