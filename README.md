<!-- vim:spell -->

# lldb-swift-string-index

LLDB Formatter for Swift `String.Index` type.

## Installation

This repository is meant to be a submodule of
[lldb-bundle](//github.com/anpol/lldb-bundle), look there for installation instructions.

You also have an option to clone this repository and add the following line
into your `~/.lldbinit` file:
```
command script import <path-to-repository>/lldb_swift_string_index
```

## Quick Start

The formatter displays information about variables of Swift `String.Index` type
when debugging with LLDB.

Assuming you have a frame variable `index` of type `String.Index`, you can use
the LLDB `frame variable` command to print the variable:
```
(lldb) fr v -T index
(DefaultIndices<String>.Element) index = <offset=6:0 aligned=true stride=3> {
  (UInt64) encodedOffset = 6
  (Int) transcodedOffset = 0
  (Bool?) isScalarAligned = true
  (Int?) characterStride = 3
}
```

Similar information is displayed by Xcode in its *Variables View*.

## Contributing

Feel free to file an issue, or send a pull request.

Before making your changes, you need to establish a development environment.
As this repository is meant to be a submodule of
[lldb-bundle](//github.com/anpol/lldb-bundle), look there for creating the
Python virtual environment suitable for developing with LLDB.

Once you activated the virtual environment, run:
```sh
make init
```
to install the required development tools.

Use your editor or IDE to make your changes.  Add relevant tests.  To prepare
for a submission, run:
```sh
make format
make lint
make test
```

Fix lint issues and test failures.

Repeat until everything is OK, then open a pull request.

Thanks!
