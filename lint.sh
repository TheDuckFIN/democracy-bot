#!/usr/bin/env bash

source .venv/bin/activate

GREEN="\033[0;32m"
NORMAL='\033[0m'

echo -e "${GREEN}[LINT] Running pylint...${NORMAL}"
pylint democracy_bot

echo -e "${GREEN}[LINT] Running black...${NORMAL}"
black --check democracy_bot
