# -*- coding: utf-8 -*-

# Copyright 2014 Globo.com Player authors. All rights reserved.
# Use of this source code is governed by a MIT License
# license that can be found in the LICENSE file.

import os
from tulip.m3u8.parser import is_url
from tulip.compat import urljoin

def _urijoin(base_uri, path):
    if is_url(base_uri):
        return urljoin(base_uri, path)
    else:
        return os.path.normpath(os.path.join(base_uri, path.strip('/')))


class BasePathMixin(object):

    @property
    def absolute_uri(self):
        if self.uri is None:
            return None
        if is_url(self.uri):
            return self.uri
        else:
            if self.base_uri is None:
                raise ValueError('There can not be `absolute_uri` with no `base_uri` set')
            return _urijoin(self.base_uri, self.uri)

    @property
    def base_path(self):
        if self.uri is None:
            return None
        return os.path.dirname(self.uri)

    @base_path.setter
    def base_path(self, newbase_path):
        if self.uri is not None:
            if not self.base_path:
                self.uri = "%s/%s" % (newbase_path, self.uri)
            else:
                self.uri = self.uri.replace(self.base_path, newbase_path)


class GroupedBasePathMixin(object):

    def _set_base_uri(self, new_base_uri):
        for item in self:
            item.base_uri = new_base_uri

    base_uri = property(None, _set_base_uri)

    def _set_base_path(self, newbase_path):
        for item in self:
            item.base_path = newbase_path

    base_path = property(None, _set_base_path)
