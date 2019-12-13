# pyson0

Use ottypes operations with python objects and find differences between objects following the ottypes defintion and format https://github.com/ottypes/docs.

On its essence this project is a port of the following projects from javascript to python, with a few modifications.

 * ottypes/json0 (https://github.com/ottypes/json0) 
 * kbadk/json0-ot-diff (https://github.com/kbadk/json0-ot-diff)

## Status
![TravisCI Build Status](https://travis-ci.com/lbragues/pyson0.svg?branch=master)
#
At the moment some parts of the library are not complete and others need validations in terms of use cases and performance.

### json0
For now the port is only implementing the apply **without** support for si/sd.
We will be adding this in the near future.

### json0-ot-diff
It is fully ported. To support string operations it is using the python diff-match-patch implementation from google.

#
## Install

### Using Package Manager

### Manually

#
## Testing
To run the tests simply run: ``python -m unittest discover -s tests/ -p "test_*.py"``
