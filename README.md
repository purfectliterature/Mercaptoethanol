
# Mercaptoethanol (Alpha)

Mercaptoethanol is an automation software for plagiarism checking and collation in programming assignments. It is an improved version of [Mercapto (Beta)](https://github.com/purfectliterature/Mercapto). This software relies heavily on [MOSS](https://theory.stanford.edu/~aiken/moss/).

Mercaptoethanol strives to achieve **simplicity**, **user-friendliness**, **performance**, and **robustness**.

> [&beta;-Mercaptoethanol](https://en.wikipedia.org/wiki/2-Mercaptoethanol) is a chemical reagent used to oxidise disulphide bonds in complex protein structures, usually used to linearise proteins prior to the running of sodium dodecyl sulphate–polyacrylamide gel electrophoresis ([SDS-PAGE](https://en.wikipedia.org/wiki/SDS-PAGE)).

> The name *Mercaptoethanol* was chosen since **et**hanol is an alcohol with **2** carbon atoms. This software essentially is a version 2 of the original Mercapto.

## Setting up the automation environment
Setting up Mercaptoethanol have never been easier! Simply clone this repository and you are ready to move.

## Usage
### The Mercaptoethanol file structure
The directory in which you cloned this repository essentially is the *project directory*. After running the complete upload-to-MOSS procedure with this script, you should have this file structure:
```
    .
    ├── core  ------------> the engine. nothing to see here :)
    │   └── ...
    ├── dumps  -----------> all downloaded students' submissions (.zip) from Coursemology
    │   └── ...
    ├── logs  ------------> logs generated when uploading submissions to moss (.mlog)
    │   └── ...
    ├── submissions  -----> all students' submissions, unpacked .zips from dumps
    │   └── ...
    ├── templates  -------> the workbin in the course from Coursemology
    │   └── ...
    ├── moss.json  -------> output MOSS URLs
    ├── project.mproj  ---> Mercaptoethanol Plagiarism Check Project File (.mproj)
    ├── session.mssn  ----> Coursemology user session file (.mssn)
    └── start.py  --------> script's entry point
```

### Actually using the script
See the annotated comments in `start.py`!

### Very simple to use, ain't it chief?
