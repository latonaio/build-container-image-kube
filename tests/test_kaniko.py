import unittest

class BuildImageTest(unittest.TestCase):
    def setUp(self):
        import os
        import json

        self.dockerfile_true = os.path.join(os.getcwd(), "tests/data/Dockerfile-true")
        self.dockerfile_false = os.path.join(os.getcwd(), "tests/data/Dockerfile-false")
        self.context = os.path.join(os.getcwd(), "tests/data")
        config_path  = ("./config/docker-registry.json")
        with open(config_path, "r") as f:
            config = json.load(f)
        self.url, self.user, self.password = config['url'], config['username'], config['password']
    
    def test_extract_base_image_from_dockerfile(self):
        from src.build_image.build_image import BuildImage
        
        expected_true = "l4t:latest"
        expected_false = None
        client = BuildImage()
        res_true = client.extract_base_image_from_dockerfile(self.dockerfile_true)
        res_false = client.extract_base_image_from_dockerfile(self.dockerfile_false)
        self.assertEqual(expected_true, res_true)
        self.assertEqual(expected_false, res_false)

    def fetch_all_image_in_registry(self):
        from src.build_image.build_image import BuildImage

        client = BuildImage()
        client.fetch_all_images_in_registry(registry=self.url, 
                                            username=self.user, 
                                            password=self.password)
        self.assertTrue(client.registry_images)
        self.assertTrue(client.image_tags)
    
    def test_rename_baseimage_in_dockerfile(self):
        from src.build_image.build_image import BuildImage

        default = "l4t:latest"
        expected_true = "python:latest"
        client = BuildImage()
        client.rename_baseimage_in_dockerfile(self.dockerfile_true, expected_true)
        res = client.extract_base_image_from_dockerfile(self.dockerfile_true)
        self.assertEqual(expected_true, res)
        client.rename_baseimage_in_dockerfile(self.dockerfile_true, default)
    
    """
    def test_build_push(self):
        from src.BuildImage import BuildImage
        
        client = BuildImage()
        client.build_push(dockerfile=self.dockerfile_true, context=self.context, destination=self.url)
    """     
