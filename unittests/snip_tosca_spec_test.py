import unittest
import snip_tosca_spec

class TestProcessFile(unittest.TestCase):
    def setUp(self):
        # Create a sample input file
        self.input_file_path = 'test_input.md'
        with open(self.input_file_path, 'w') as f:
            f.write(
"""This is a test.

<!-- EDITOR_TAG{"type":"example","id":"s1","action":"start"} -->
```yaml
Some TOSCA
```
Text
<!-- EDITOR_TAG{"type":"example","id":"s1","action":"start"} -->
```yaml
Some More TOSCA
```
"""
            )

        # Create an expected output file
        self.expected_output_file_path = 'expected_output.md'
        with open(self.expected_output_file_path, 'w') as f:
            f.write("""This is a test.

<!-- EDITOR_TAG{"type":"example","id":"s1","action":"start"} -->
```yaml
Some TOSCA
```
<!-- EDITOR_TAG{"type":"example","id":"s1","action":"end"} -->
Text
<!-- EDITOR_TAG{"type":"example","id":"s2","action":"start"} -->
```yaml
Some More TOSCA
```
<!-- EDITOR_TAG{"type":"example","id":"s2","action":"end"} -->
"""
            )

        # Path for the actual output file
        self.output_file_path = 'test_output.md'

        # Create a sample input file containing errors
        self.input_2_file_path = 'test_input_2.md'
        with open(self.input_2_file_path, 'w') as f:
            f.write("""
<!-- EDITOR_TAG{"type":"example","id":"s1","action":"start"} -->
```not_yaml
Some Other stuff:
```
"""
            )

    def test_process_file_error(self):
        # Run the function on a file with errors
        with self.assertRaises(ValueError):
            snip_tosca_spec.expand_snip(self.input_2_file_path, self.output_file_path)

    def test_process_file(self):

        # Run the function
        snip_tosca_spec.expand_snip(self.input_file_path, self.output_file_path)
        # Assert that the output file content is equal to the expected output file content
        self.maxDiff = None
        with open(self.output_file_path, 'r') as output_file:
            output_content = output_file.read()
        
        with open(self.expected_output_file_path, 'r') as expected_file:
            expected_content = expected_file.read()
        self.assertEqual(output_content, expected_content)
        
        # Create an expected example content
        expected_example_2 = """tosca_definitions_version: tosca_2_0
# EDITOR_TAG:{"type":"example","id":"s2","action":"start"} -->
Some More TOSCA
# EDITOR_TAG:{"type":"example","id":"s2","action":"end"} -->
"""
        # Assert that the example file content is equal to the expected example content
        with open('s2.yaml', 'r') as example_file_2:
            example_file_2_content = example_file_2.read()
        self.assertEqual(expected_example_2, example_file_2_content)



    def tearDown(self):
        # Clean up the files
        import os
        os.remove(self.input_file_path)
        os.remove(self.input_2_file_path)
        os.remove(self.output_file_path)
        os.remove(self.expected_output_file_path)

if __name__ == '__main__':
    unittest.main()
