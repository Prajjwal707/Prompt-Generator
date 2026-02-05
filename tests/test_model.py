"""
Model loader tests for PromptGenius backend.
"""

import pytest
from unittest.mock import Mock, patch
from utils.model_loader import ModelLoader

class TestModelLoader:
    
    def test_singleton_pattern(self):
        loader1 = ModelLoader()
        loader2 = ModelLoader()
        assert loader1 is loader2
    
    def test_model_exists_false(self):
        loader = ModelLoader()
        with patch.object(loader.config, 'model_exists', return_value=False):
            assert not loader.config.model_exists()
    
    def test_get_model_info_not_loaded(self):
        loader = ModelLoader()
        info = loader.get_model_info()
        assert info['loaded'] is False
        assert 'error' in info
    
    @patch('utils.model_loader.Llama')
    def test_load_model_success(self, mock_llama):
        mock_model = Mock()
        mock_llama.return_value = mock_model
        
        loader = ModelLoader()
        with patch.object(loader.config, 'model_exists', return_value=True):
            with patch.object(loader, '_detect_gpu', return_value=0):
                result = loader._load_model()
                assert result is True
                assert loader._loaded is True
    
    def test_clean_output(self):
        loader = ModelLoader()
        test_input = "Enhanced prompt:\nThis is a test\n\nAnother test"
        expected = "This is a test\nAnother test"
        result = loader._clean_output(test_input)
        assert result == expected
