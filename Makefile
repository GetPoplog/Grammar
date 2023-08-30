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
	#   setup		One-time setup to poetry install & download *.war
	#   build       Creates tabatkins grammar & itemisation grammar
	#   show		Shows the tabatkins grammar in a browser			
	#   clean		Removes artefacts
	#   deepclean	In addition to normal cleaning removes tools

.PHONY: show
show: _build/tabatkins.html
	$(OPEN) $^

.PHONY: setup
setup: _buildtools/railroad/rr.war
	poetry install

_buildtools/railroad/rr.war: _buildtools/railroad/rr-2.0-java11.zip
	mkdir -p _buildtools/railroad
	( cd _buildtools/railroad; unzip -o rr-2.0-java11.zip)
	rm -f _buildtools/rr-2.0-java8.zip

_buildtools/railroad/rr-2.0-java11.zip:
	mkdir -p _buildtools/railroad/
	curl https://bottlecaps.de/rr/download/rr-2.0-java11.zip > $@


.PHONY: clean
clean:
	rm -rf _build

.PHONY: deepclean
deepclean: clean
	rm -rf _buildtools

.PHONY: build
build: _build/tabatkins.html _build/itemisation_grammar_ebnf.txt _build/pop11_grammar_ebnf.html

_build/tabatkins.html: tabatkins2html.py pop11_grammar_tabatkins.txt
	mkdir -p _build
	poetry run python3 tabatkins2html.py > $@

_build/itemisation_grammar_ebnf.txt: itemisation_grammar_ebnf.py
	mkdir -p _build
	poetry run python3 itemisation_grammar_ebnf.py > $@

_build/pop11_grammar_ebnf.html: _buildtools/railroad/rr.war
	mkdir -p _build
	java -jar _buildtools/railroad/rr.war pop11_grammar_ebnf.txt > $@
