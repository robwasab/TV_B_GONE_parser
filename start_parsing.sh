#!/bin/sh

gcc formattedCodesToBinaryFile.c
python parseTvCodes.py NAcodes.c
./a.out PYTHON_FORMATTED.txt
