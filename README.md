# Add tags to a markdown file

Reads a markdown file
Finds example code which starts with tags in HTML comments like this

/```yaml #s1
and ends with 
/```  
Modifies tag to an serial ID

Writes out the example between the yaml start and end to a file with a naming containing the same serial id and tags using AsciiDoc format.

## Example usage:
In a python file, 

```python
import snip-tosca-spec
expand_snip('input.md', 'output.md')
```
or just copy your original file into input.md and run the file:
```sh
python3 snip-tosca-spec.py
```

Typically you then want to patch the original, e.g. use
$ diff -u input.md output.md > patchFile
$ patch -R OriginalFile < patchFile

(Maybe necessary to use dos2unix on the original file before patching and unix2dos afterward.)
