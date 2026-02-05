"""
Fine-tuning pipeline tests for PromptGenius backend.
"""

import pytest
import json
import tempfile
import os
from pathlib import Path

class TestDatasetPreparation:
    
    def test_load_config(self):
        from finetune.prepare_dataset import DatasetPreparer
        
        # Create a temporary config file
        config_data = {
            'dataset': {'validation_split': 0.1},
            'model': {'tokenizer': 'test'}
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            import yaml
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            preparer = DatasetPreparer(config_path)
            assert preparer.config['dataset']['validation_split'] == 0.1
        finally:
            os.unlink(config_path)
    
    def test_format_for_training(self):
        from finetune.prepare_dataset import DatasetPreparer
        
        preparer = DatasetPreparer()
        test_data = [
            {
                'user_prompt': 'test prompt',
                'enhanced_prompt': 'enhanced test prompt',
                'task_type': 'general'
            }
        ]
        
        preparer.dataset = test_data
        formatted = preparer.format_for_training()
        
        assert len(formatted) == 1
        assert 'text' in formatted[0]
        assert '<s>[INST]' in formatted[0]['text']
        assert '[/INST]' in formatted[0]['text']
    
    def test_split_dataset(self):
        from finetune.prepare_dataset import DatasetPreparer
        
        preparer = DatasetPreparer()
        preparer.config['dataset']['validation_split'] = 0.2
        
        test_data = [{'text': f'test {i}'} for i in range(10)]
        train, val = preparer.split_dataset(test_data)
        
        assert len(train) == 8
        assert len(val) == 2

class TestDatasetTokenizer:
    
    @pytest.mark.skip(reason="Skipping due to huggingface-hub dependency conflicts")
    def test_load_config(self):
        from finetune.tokenize_dataset import DatasetTokenizer
        
        config_data = {
            'model': {'tokenizer': 'test-tokenizer'},
            'dataset': {'max_length': 512}
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            import yaml
            yaml.dump(config_data, f)
            config_path = f.name
        
        try:
            tokenizer = DatasetTokenizer(config_path)
            assert tokenizer.config['dataset']['max_length'] == 512
        finally:
            os.unlink(config_path)

class TestModelEvaluator:
    
    @pytest.mark.skip(reason="Skipping due to missing nltk dependency")
    def test_compute_bleu_score(self):
        from finetune.evaluate import ModelEvaluator
        
        evaluator = ModelEvaluator()
        reference = "This is a test sentence"
        candidate = "This is a test sentence"
        
        score = evaluator.compute_bleu_score(reference, candidate)
        assert score > 0.9  # Should be very high for identical sentences
    
    @pytest.mark.skip(reason="Skipping due to missing rouge-score dependency")
    def test_compute_rouge_scores(self):
        from finetune.evaluate import ModelEvaluator
        
        evaluator = ModelEvaluator()
        reference = "This is a test sentence"
        candidate = "This is a test sentence"
        
        scores = evaluator.compute_rouge_scores(reference, candidate)
        assert 'rouge1' in scores
        assert 'rouge2' in scores
        assert 'rougeL' in scores
        assert all(0 <= score <= 1 for score in scores.values())
