"""
Dataset tokenization for PromptGenius fine-tuning.
Tokenizes prepared dataset for model training.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
import yaml
from transformers import AutoTokenizer
import torch
from datasets import Dataset

logger = logging.getLogger(__name__)

class DatasetTokenizer:
    """Tokenizes dataset for fine-tuning."""
    
    def __init__(self, config_path: str = "finetune/config.yaml"):
        self.config = self._load_config(config_path)
        self.tokenizer = None
        self.train_dataset = None
        self.val_dataset = None
    
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {config_path}")
            return config
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            raise
    
    def load_tokenizer(self) -> bool:
        """Load the tokenizer."""
        try:
            model_name = self.config['model']['tokenizer']
            logger.info(f"Loading tokenizer: {model_name}")
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=self.config['model']['trust_remote_code'],
                use_auth_token=self.config['model']['use_auth_token']
            )
            
            # Set padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            logger.info(f"Tokenizer loaded successfully. Vocab size: {self.tokenizer.vocab_size}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading tokenizer: {e}")
            return False
    
    def load_datasets(self, train_file: str, val_file: str) -> bool:
        """Load prepared datasets."""
        try:
            # Load training data
            with open(train_file, 'r', encoding='utf-8') as f:
                train_data = json.load(f)
            
            # Load validation data
            with open(val_file, 'r', encoding='utf-8') as f:
                val_data = json.load(f)
            
            # Convert to HuggingFace datasets
            self.train_dataset = Dataset.from_list(train_data)
            self.val_dataset = Dataset.from_list(val_data)
            
            logger.info(f"Loaded datasets: Train={len(train_data)}, Val={len(val_data)}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading datasets: {e}")
            return False
    
    def tokenize_function(self, examples: Dict[str, List]) -> Dict[str, List]:
        """Tokenize a batch of examples."""
        max_length = self.config['dataset']['max_length']
        
        # Tokenize the text
        tokenized = self.tokenizer(
            examples['text'],
            truncation=True,
            padding='max_length',
            max_length=max_length,
            return_tensors=None,  # Return lists for datasets
            return_attention_mask=True
        )
        
        # Create labels (same as input_ids for causal LM)
        tokenized['labels'] = tokenized['input_ids'].copy()
        
        return tokenized
    
    def tokenize_datasets(self) -> bool:
        """Tokenize the datasets."""
        try:
            logger.info("Tokenizing training dataset...")
            self.train_dataset = self.train_dataset.map(
                self.tokenize_function,
                batched=True,
                remove_columns=['text', 'user_prompt', 'enhanced_prompt', 'task_type'],
                desc="Tokenizing train"
            )
            
            logger.info("Tokenizing validation dataset...")
            self.val_dataset = self.val_dataset.map(
                self.tokenize_function,
                batched=True,
                remove_columns=['text', 'user_prompt', 'enhanced_prompt', 'task_type'],
                desc="Tokenizing validation"
            )
            
            # Set format for PyTorch
            self.train_dataset.set_format('torch')
            self.val_dataset.set_format('torch')
            
            logger.info("Datasets tokenized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error tokenizing datasets: {e}")
            return False
    
    def save_tokenized_datasets(self) -> bool:
        """Save tokenized datasets."""
        try:
            output_dir = Path("finetune/tokenized")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save datasets
            self.train_dataset.save_to_disk(output_dir / "train")
            self.val_dataset.save_to_disk(output_dir / "validation")
            
            # Save tokenizer
            self.tokenizer.save_pretrained(output_dir / "tokenizer")
            
            # Save metadata
            metadata = {
                'train_samples': len(self.train_dataset),
                'val_samples': len(self.val_dataset),
                'max_length': self.config['dataset']['max_length'],
                'vocab_size': self.tokenizer.vocab_size,
                'model_name': self.config['model']['tokenizer']
            }
            
            with open(output_dir / "metadata.json", 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Saved tokenized datasets to {output_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving tokenized datasets: {e}")
            return False
    
    def analyze_dataset(self) -> Dict[str, Any]:
        """Analyze the tokenized dataset."""
        try:
            # Sample a few examples
            sample_size = min(100, len(self.train_dataset))
            sample_indices = torch.randperm(len(self.train_dataset))[:sample_size]
            
            lengths = []
            for idx in sample_indices:
                example = self.train_dataset[idx]
                # Find actual length (excluding padding)
                input_ids = example['input_ids']
                if self.tokenizer.pad_token_id in input_ids:
                    length = (input_ids != self.tokenizer.pad_token_id).sum().item()
                else:
                    length = len(input_ids)
                lengths.append(length)
            
            analysis = {
                'train_samples': len(self.train_dataset),
                'val_samples': len(self.val_dataset),
                'max_length': self.config['dataset']['max_length'],
                'avg_sequence_length': sum(lengths) / len(lengths),
                'min_sequence_length': min(lengths),
                'max_sequence_length': max(lengths),
                'vocab_size': self.tokenizer.vocab_size,
                'pad_token_id': self.tokenizer.pad_token_id,
                'eos_token_id': self.tokenizer.eos_token_id
            }
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing dataset: {e}")
            return {}
    
    def tokenize(self, train_file: str, val_file: str) -> bool:
        """Run the complete tokenization pipeline."""
        logger.info("Starting dataset tokenization...")
        
        # Load tokenizer
        if not self.load_tokenizer():
            return False
        
        # Load datasets
        if not self.load_datasets(train_file, val_file):
            return False
        
        # Tokenize datasets
        if not self.tokenize_datasets():
            return False
        
        # Analyze dataset
        analysis = self.analyze_dataset()
        logger.info(f"Dataset analysis: {analysis}")
        
        # Save tokenized datasets
        if not self.save_tokenized_datasets():
            return False
        
        logger.info("✅ Dataset tokenization completed successfully!")
        return True

def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Tokenize dataset for fine-tuning")
    parser.add_argument("--train", default="finetune/data/train.json", 
                       help="Training data file")
    parser.add_argument("--val", default="finetune/data/validation.json", 
                       help="Validation data file")
    parser.add_argument("--config", default="finetune/config.yaml", 
                       help="Configuration file")
    
    args = parser.parse_args()
    
    tokenizer = DatasetTokenizer(args.config)
    success = tokenizer.tokenize(args.train, args.val)
    
    if success:
        print("✅ Dataset tokenization completed successfully!")
        print("📁 Check finetune/tokenized/ for tokenized datasets")
    else:
        print("❌ Dataset tokenization failed!")
        exit(1)

if __name__ == "__main__":
    main()
