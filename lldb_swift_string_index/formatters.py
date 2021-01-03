#!/usr/bin/env python
"""LLDB type formatters the certain types."""
from typing import Optional, Union

import lldb
from lldb.formatters import Logger as LoggerModule

from lldb_script_utils import debugger_utils
from lldb_swift_string_index import core


def _read_uint64(valobj: lldb.SBValue) -> Optional[int]:
    logger = LoggerModule.Logger()
    error = lldb.SBError()
    result: int = valobj.GetData().GetUnsignedInt64(error, 0)
    if error.fail:
        logger.write(f'SBData::GetUnsignedInt64 failed: {error.description}')
        return None
    return result


def _create_debug_view(valobj: lldb.SBValue) -> core.StringIndexDebugView:
    raw_bits = _read_uint64(valobj.GetChildMemberWithName('_rawBits'))
    return core.StringIndexDebugView(raw_bits or 0)


def _format_expression(expression: Optional[Union[bool, int]]) -> str:
    if expression is None:
        return 'nil'
    if isinstance(expression, bool):
        return 'true' if expression else 'false'
    return str(expression)


class StringIndexProvider:
    """A synthetic children provider for the Swift String.Index type."""
    TYPE_NAME = 'Swift.String.Index'
    MEMBER_NAMES = [
        # '_rawBits',
        'encodedOffset',
        'transcodedOffset',
        'isScalarAligned',
        'characterStride',
        # 'reserved',
    ]

    @classmethod
    def lldb_init_class(cls, debugger: lldb.SBDebugger) -> None:
        category = 'swift'
        debugger_utils.handle_type_summary_add(debugger,
                                               cls.TYPE_NAME,
                                               expand=True,
                                               python_function=cls.get_summary,
                                               category=category)
        debugger_utils.handle_type_synthetic_add(debugger,
                                                 cls.TYPE_NAME,
                                                 python_class=cls,
                                                 category=category)

    @classmethod
    def get_summary(cls, valobj: lldb.SBValue, bindings: dict) -> str:
        provider = cls(valobj.GetNonSyntheticValue(), bindings)
        dv = provider.debug_view
        result = [f'offset={dv.encoded_offset}:{dv.transcoded_offset}']
        if dv.is_scalar_aligned is not None:
            result.append(
                f'aligned={_format_expression(dv.is_scalar_aligned)}')
        if dv.character_stride is not None:
            result.append(f'stride={_format_expression(dv.character_stride)}')
        return f"<{' '.join(result)}>"

    def __init__(self, valobj: lldb.SBValue, _: dict):
        assert not valobj.IsSynthetic()
        self.valobj = valobj
        self.debug_view = _create_debug_view(self.valobj)

    def update(self) -> bool:
        self.debug_view = _create_debug_view(self.valobj)
        # If return value is True, LLDB will be allowed to cache the children
        # it previously obtained, and will not return to the provider to ask.
        return True

    @staticmethod
    def has_children() -> bool:
        return True

    @classmethod
    def num_children(cls) -> int:
        return len(cls.MEMBER_NAMES)

    @classmethod
    def get_child_index(cls, name: str) -> Optional[int]:
        try:
            return cls.MEMBER_NAMES.index(name)
        except ValueError:
            return None

    def get_child_at_index(self, index: int) -> Optional[lldb.SBValue]:
        if index < 0 or index > self.num_children():
            return None
        name = self.MEMBER_NAMES[index]
        LoggerModule.Logger().write(f'index={index}, name={name}')

        if name == '_rawBits':
            return self.valobj.GetChildMemberWithName('_rawBits')

        dv = self.debug_view
        if name == 'encodedOffset':
            return self._create_child_from_expression(name, dv.encoded_offset,
                                                      'UInt64')
        if name == 'transcodedOffset':
            return self._create_child_from_expression(name,
                                                      dv.transcoded_offset,
                                                      'Int')
        if name == 'characterStride':
            return self._create_child_from_expression(name,
                                                      dv.character_stride,
                                                      'Int?')
        if name == 'reserved':
            return self._create_child_from_expression(name, dv.reserved,
                                                      'Int?')
        if name == 'isScalarAligned':
            return self._create_child_from_expression(name,
                                                      dv.is_scalar_aligned,
                                                      'Bool?')
        return None

    def _create_child_from_expression(self, name: str,
                                      expression: Optional[Union[bool, int]],
                                      expression_type: str) -> lldb.SBValue:
        return self.valobj.CreateValueFromExpression(
            name, f'{_format_expression(expression)} as {expression_type}')
