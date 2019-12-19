# Python tools for working with Cryptic Studios data files
Starting out as a set of tools to work with hogg archives, lets see how far we can go.

# Quickstart
Make sure you have pipenv installed, then...

```
git clone https://github.com/lokkju/pyhogg.git
pipenv install
pipenv run python tool.py --help
pipenv run python tool.py [extract|list] <hogg file>
```

That's it, folks!

## Current status
#### Hogg Files
* Lists all files with correct names from ?DataList and DataList Journal
* Extracts all files or a glob-matched subset

#### Wtex Files
* Converts Wtex files to DDS files for editing in GIMP

## Data structure definitions
All datastructures (hogg files, datalist, etc) are currently being defined using Kaitai; we then generate python code and wrap it.

If you modify the ksy files, you must regenerate the python code:
```
kaitai-struct-compiler -t python kaitai/*.ksy
```
