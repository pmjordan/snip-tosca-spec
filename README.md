# Add tags to a markdown file

Reads a markdown file
Finds example code which starts with tags in HTML comments like this
-- EDITOR_TAG{"type":"example","id":"s1","action":"start"} -->
/```yaml
and ends with 
/```  
Adds further tag containing an serial ID before the start and another after the end

Writes out the example between the yaml start and end to a file with a naming containing the same serial id

## Example usage:
In a python file, 

```python
import snip-tosca-spec
expand_snip('input.md', 'output.md')
```
or just copy your file into input.md and run the file:
```sh
python3 snip-tosca-spec.py
```

Typically you then want to patch the original, e.g. use
$ diff -u input.md output.md > patchFile
$ patch -R OriginalFile < patchFile

(maybe necessary to use dos2unix on the original file before patching and unix2dos afterward.)

TODO:
Refactor to modules