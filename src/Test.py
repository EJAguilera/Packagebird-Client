from typing import Dict, List
import unittest
import string

import requests
from manifest import Manifest
from request_bundler import make_request

class TestManifest(unittest.TestCase):
    sample_manifest_path: str = 'sample_manifest.json'
    sample_manifest_file: str = '{"dependencies":{"name":"Sample","version":"0.0.1"},"registry":"http://localhost:9091/registry"}'
    sample_manifest_parse: Dict = {
        "dependencies": [
        {
            "name": "Sample",
            "version": "0.0.1"
        }
        ],
        "registry": "http://localhost:9091/registry"
    }
    sample_manifest_dependencies: List = ["Sample-v0.0.1"]
    sample_manifest_request: str = '{"requests:["Sample-v0.0.1"]"}'

    def test_convert(self):
        """Testing conversion between JSON file and Dictionary"""
        self.assertEqual(self.sample_manifest_parse, Manifest.file_parse(self, self.sample_manifest_path), "Files should match.")
    
    def test_class_convert(self):
        """Testing class conversion between JSON file and class dictionary"""
        sample_manifest = Manifest(self.sample_manifest_path)
        self.assertEqual(self.sample_manifest_parse, sample_manifest.manifest, "Class attribute should match sample")
    
    def test_class_dependencies(self):
        """Testing dependency list results"""
        self.assertEqual(self.sample_manifest_dependencies, Manifest(self.sample_manifest_path).dependencies(), "Dependency list should match")
    
    def test_class_request(self):
        """Testing request and return results"""
        sample_manifest = Manifest(self.sample_manifest_path)
        self.assertRaises(Exception,make_request(sample_manifest.registry, sample_manifest.dependencies))

if __name__ == '__main__':
    unittest.main()