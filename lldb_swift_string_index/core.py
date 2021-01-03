#!/usr/bin/env python
"""Helpers for manipulating values of certain types."""
from typing import Optional


class StringIndexDebugView:
    """Helpers for manipulating raw bits of the Swift String.Index type."""
    def __init__(self, raw_bits: int):
        self._raw_bits = raw_bits

    @property
    def ordering_value(self) -> int:
        """
        A combination of encodedOffset and transcodedOffset, used for ordering.
        """
        return self._raw_bits >> 14

    @property
    def encoded_offset(self) -> int:
        """
        Scalar offset, measured in units of internal encoding.
        Since Swift 5, internal encoding is UTF-8, so units here are UInt8.
        """
        return self._raw_bits >> 16

    @property
    def transcoded_offset(self) -> int:
        """
        Sub-scalar offset, measured in units of external encoding.
        E.g. if external encoding is UTF-16, then the units here are UInt16.
        """
        return self.ordering_value & 0x03

    @property
    def is_scalar_aligned(self) -> Optional[bool]:
        """
        True if the index is known to be scalar aligned, false if it's not;
        `nil` if the index needs to be checked for the alignment.
        """
        value = (self._raw_bits & 0x01) != 0
        if not value and self.transcoded_offset == 0:
            return None
        return value

    @property
    def character_stride(self) -> Optional[int]:
        """
        The cached distance to the next extended grapheme cluster boundary; or
        `nil` if the boundary needs to be determined.
        """
        value = (self._raw_bits & 0x3F00) >> 8
        if value == 0:
            return None
        return value

    @property
    def reserved(self) -> Optional[int]:
        value = (self._raw_bits & 0xFE) >> 1
        if value == 0:
            return None
        return value
