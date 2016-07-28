#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_psdwriter
----------------------------------

Tests for `psdwriter` module.
"""

import io


import pytest


import traitlets as t


from psdwriter import core
from psdwriter import enums


class TestHeader(object):
    def test_header(self):
        content = b'8BPB\0\x02\0\0\0\0\0\0\0\x03\0\0\0\x0F\0\0\0\x0F\0\x08\0\1'
        fd = io.BytesIO(content)
        fd.seek(0)
        h = core.Header.read(fd)

        assert h.signature == b'8BPB'
        assert h.version == 2
        assert h.num_channels == 3
        assert h.height == 15
        assert h.width == 15
        assert h.depth == 8
        assert h.color_mode == enums.ColorMode.grayscale

        fd = io.BytesIO()
        h.write(fd)
        assert fd.getvalue() == content

    def test_header_invalid_version(self):
        content = b'8BPB\0\x03\0\0\0\0\0\0\0\x03\0\0\0\x0F\0\0\0\x0F\0\x08\0\1'
        fd = io.BytesIO(content)
        fd.seek(0)
        with pytest.raises(ValueError):
            core.Header.read(fd)

    def test_header_invalid_signature(self):
        content = b'8BPX\0\x02\0\0\0\0\0\0\0\x03\0\0\0\x0F\0\0\0\x0F\0\x08\0\1'
        fd = io.BytesIO(content)
        fd.seek(0)
        with pytest.raises(ValueError):
            core.Header.read(fd)

    def test_header_invalid_reserved(self):
        content = (
            b'8BPB\0\x02\0\0\0\x01\0\0\0\x03\0\0\0\x0F\0\0\0\x0F\0\x08\0\1')
        fd = io.BytesIO(content)
        fd.seek(0)
        with pytest.raises(ValueError):
            core.Header.read(fd)

    def test_header_invalid_width(self):
        content = b'8BPB\0\x02\0\0\0\0\0\0\0\x03\0\0\0\0\0\0\0\x0F\0\x08\0\1'
        fd = io.BytesIO(content)
        fd.seek(0)
        with pytest.raises(t.TraitError):
            core.Header.read(fd)

    def test_header_invalid_depth(self):
        content = b'8BPB\0\x02\0\0\0\0\0\0\0\x03\0\0\0\x0F\0\0\0\x0F\0\x09\0\1'
        fd = io.BytesIO(content)
        fd.seek(0)
        with pytest.raises(t.TraitError):
            core.Header.read(fd)