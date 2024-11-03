import re

def expand_snip(input_file_path, output_file_path):
    # Define the pattern you want to match
    start_pattern = re.compile(r'^<!-- EDITOR_TAG{"type":"example","id":"s1","action":"start"} -->')
    end_pattern = re.compile(r'^```$')
    index = 1
    current_pattern=start_pattern
    # Open the input file for reading and the output file for writing
    with open(input_file_path, 'r') as infile:
        lines = infile.readlines()

    with open(output_file_path, 'w') as outfile:
        # Process each line in the input file
        for line_number, line in enumerate(lines, start=1):
            # If the line matches the pattern
            if current_pattern.search(line):
                #test the next line really is the start of some YAML (it won't be if this program ran more than once)
                if current_pattern == start_pattern:
                    # Check if the next line is the start of some YAML
                    next_line = lines[line_number] if line_number < len(lines) else ''
                    if next_line.strip().startswith('```yaml'):
                        # Rewrite the line
                        line = f'<!-- EDITOR_TAG{{"type":"example","id":"s{str(index)}","action":"start"}} -->\n'
                        outfile.write(line)
                        # open a file for the snip
                        open_example_file(index)
                        # Now look for the end of the snip
                        current_pattern = end_pattern
                        # Skip to the next line
                        continue
                    else:
                        raise ValueError(f"Expected YAML start after editor tag at line {line_number+1}")
                if current_pattern == end_pattern:
                    line = f'```\n<!-- EDITOR_TAG{{"type":"example","id":"s{str(index)}","action":"end"}} -->\n'
                    close_example_file(index)
                    # Now look for the start of the next snip
                    current_pattern = start_pattern
                    index += 1
            # Write the (possibly modified) line to the output file
            else:
                #haven't found the a tag
                if (current_pattern == end_pattern) and (not(line.strip().startswith('```yaml'))):
                    #write to the snip file
                    with open(f's{str(index)}.yaml', 'a') as snip:
                        snip.write(line)
            outfile.write(line)

    print(f'Processed lines written to {output_file_path}')

def open_example_file(index):
    with open(f's{str(index)}.yaml', 'w') as snip:
        snipline = f'tosca_definitions_version: tosca_2_0\n# EDITOR_TAG:{{"type":"example","id":"s{str(index)}","action":"start"}} -->\n'
        snip.write(snipline)

def close_example_file(index):
    with open(f's{str(index)}.yaml', 'a') as snip:
        snipline = f'# EDITOR_TAG:{{"type":"example","id":"s{str(index)}","action":"end"}} -->\n'
        snip.write(snipline)

# Example usage:
expand_snip('input.md', 'output.md')
