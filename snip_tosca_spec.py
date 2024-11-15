import re

def expand_snip(input_file_path, output_file_path):
    # Define the pattern you want to match
    start_pattern = re.compile(r'^```.yaml #s1')
    end_pattern = re.compile(r'^```$')
    index = 1
    current_pattern=start_pattern
    # Open the input file for reading and the output file for writing
    with open(input_file_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    with open(output_file_path, 'w',encoding='utf-8') as outfile:
        # Process each line in the input file
        for line_number, line in enumerate(lines, start=1):
            # Check if the current line is one of interest
            if current_pattern.search(line):
                if current_pattern == start_pattern:
                    # Found a start tag
                    # Rewrite the line
                    line = f'```.yaml #s{index}\n'
                    outfile.write(line)
                    # open a file for the snip
                    open_example_file(index)
                    # Now look for the end of the snip
                    current_pattern = end_pattern
                    # Skip to the next line
                    continue
                if current_pattern == end_pattern:
                    # Found an end tag
                    close_example_file(index)
                    # Now look for the start of the next snip
                    current_pattern = start_pattern
                    index += 1
            else:
                # have not yet found the end tag so line must be in an example
                # write the snip file
                if (current_pattern == end_pattern):
                    #write to the snip file
                    with open(f's{str(index)}.yaml', 'a', encoding='utf-8') as snip:
                        snip.write(line)
            # Write the (possibly modified) line to the output file
            outfile.write(line)

    print(f'Processed lines written to {output_file_path}')

def open_example_file(index):
    with open(f's{str(index)}.yaml', 'w') as snip:
        snipline = f'tosca_definitions_version: tosca_2_0\n# tag::s{str(index)}[]\n'
        snip.write(snipline)

def close_example_file(index):
    with open(f's{str(index)}.yaml', 'a') as snip:
        snipline = f'# end::s{str(index)}[]\n'
        snip.write(snipline)

# Example usage:
expand_snip('input.md', 'output.md')
