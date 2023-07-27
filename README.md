# Pop-11 Grammar
This is a work-in-progress. The aim is to provide a couple of formal grammars for the current version of Pop-11. 
The current state of the repo is that the grammars are a hybrid between current Pop-11 and the version of 
Pop-11 described in Sloman and Barrett "Pop-11: A Practical Language for Artificial Intelligence". 

## Building the railroad diagrams 

To visualise the grammars we have added a couple of tools that create
railroad diagrams. These can be invoked via:

    make build

When this runs it will leave the results in the _build folder. On my
machine it looks like this:

    % ls -l _build
    total 292
    -rw-rw-r-- 1 steve steve  36889 Feb  7 22:57 itemisation_grammar_ebnf.txt
    -rw-rw-r-- 1 steve steve 128230 Feb  7 22:57 pop11_grammar_ebnf.html
    -rw-rw-r-- 1 steve steve 126932 Feb  7 22:57 tabatkins.html

## Build Pre-requisites

There are some pre-requisites. I haven't got around to automating these
as yet, so you need to install them by hand. If you do this, always start
with `sudo apt update` before continuing:

    1. python3                      sudo apt install python
    2. poetry                       see https://python-poetry.org/docs/ 
    3. a JRT (Java run-time)        sudo apt install default-jdk
    4. curl                         sudo apt install curl

There is also some one-time setup - running poetry install and downloading
a JAR file to run the EBNF compiler. This can be done with the target
setup:

    make setup

This will install the JAR file into the _buildtools folder.
