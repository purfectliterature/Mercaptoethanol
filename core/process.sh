#!/bin/bash
if [ $# -ne 2 ]
then
	echo "Usage: $0 zipfile course_code"
	exit 1
fi

dir="${1%.zip}"
dir=${dir//+([^[:alnum:]]/_} # replace non alphanum with underscore

mkdir "$dir"

shopt -s globstar

unzip "$1" -d tmp
cd tmp
for i in *
	do s=${i// /_}
	for f in "$i"/*/*.py
		do echo "###" $f "###"
		cat "$f"
       	done > "../$dir/${s#tmp}-$2.py"
done
cd ..
rm -rf tmp