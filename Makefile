# Essential warning for all GNU Makefiles.
MAKEFLAGS+=--warn-undefined-variables

# Causes the commands in a recipe to be issued in the same shell. Be aware 
# that `cd` commands are not executed in a subshell!
.ONESHELL:

SHELL:=/bin/bash

# When using ONESHELL, we want to exit on error (-e) and error if a command 
# fails in a pipe (-o pipefail). When overriding .SHELLFLAGS one must always add
# a tailing `-c` as this is the default setting of Make.
.SHELLFLAGS:=-e -o pipefail -c

# Invoke the all target when no target is explicitly specified.
.DEFAULT_GOAL:=help

# Set up $(OPEN) to use the platform specific file-opening command. We only
# use this for opening .html files, so a command that opens a file in the 
# system web browser would be good enough.
UNAME_S:=$(shell uname -s)
ifeq ($(UNAME_S),Linux)
	OPEN:=xdg-open
endif
ifeq ($(UNAME_S),Darwin)
	OPEN:=open
endif

# Delete targets if their recipe exits with a non-zero exit code.
.DELETE_ON_ERROR:

.PHONY: help
help:
	# Valid targets are:
	#   build       Creates tabatkins grammar & itemisation grammar
	#	show		Shows the tabatkins grammar in a browser			
	#	clean		Removes artefacts

.PHONY: show
show: _build/tabatkins.html
	$(OPEN) $^

.PHONY: clean
clean:
	rm -rf _build

.PHONY: build
build: _build/tabatkins.html _build/itemisation_grammar_ebnf.txt

_build/tabatkins.html: tabatkins2html.py pop11_grammar_tabatkins.txt
	mkdir -p _build
	poetry run python3 tabatkins2html.py > $@

_build/itemisation_grammar_ebnf.txt: itemisation_grammar_ebnf.py
	mkdir -p _build
	poetry run python3 itemisation_grammar_ebnf.py > $@
