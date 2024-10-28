# Add tags to a markdown file

Reads a markdown file
Finds example code which starts with 
/```yaml
and ends with 
/```  
Adds further tag containing an serial ID before the start and another after the end

Writes out the example between the yaml start and end to a file with a naming containing the same serial id

## Example usage:
In a python file, 

```python
import snip-tosca-spec
add_tag_to_markdown('input.md', 'output.md')
```
or just copy your file into input.md and run the file:
```sh
python3 snip-tosca-spec.py
```
