#!/usr/bin/env python
"""LLDB Formatter for Swift String.Index."""

import lldb

from lldb_swift_string_index import formatters


def __lldb_init_module(debugger: lldb.SBDebugger, _: dict):
    # pylint: disable=invalid-name
    formatters.StringIndexProvider.lldb_init_class(debugger)
