.PHONY: install install-dev tests docs

PYTHON :=
OS_NAME :=

# Detect OS name and specify the python client.
# We do this because in Windows there is not python3
# and python is the xecutable for Python

ifeq ($(OS), Windows_NT)
	OS_NAME := Windows
	PYTHON := python
else
	OS_NAME := $(shell uname)
	PYTHON := python3
endif

install:
	$(PYTHON) -m pip install .

install-dev:
	$(PYTHON) -m pip install -e .'[dev]'

tests:
	$(PYTHON) -m pytest -vv

docs:
	$(PYTHON) -m mkdocs serve || $(PYTHON) -m pip install -e .'[dev]' && $(PYTHON) -m mkdocs serve