"""
Dataset preparation for PromptGenius fine-tuning.
Converts Alpaca format to training-ready format.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
import yaml

logger = logging.getLogger(__name__)

class DatasetPreparer:
    """Prepares dataset for fine-tuning."""
    
    def __init__(self, config_path: str = "finetune/config.yaml"):
        self.config = self._load_config(config_path)
        self.dataset = []
        self.train_data = []
        self.val_data = []
    
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
    
    def load_dataset(self, input_file: str) -> bool:
        """Load the PromptGenius training dataset."""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Handle both formats: direct list or with metadata
            if isinstance(data, dict) and 'data' in data:
                self.dataset = data['data']
                logger.info(f"Loaded dataset with metadata: {len(self.dataset)} records")
            elif isinstance(data, list):
                self.dataset = data
                logger.info(f"Loaded dataset: {len(self.dataset)} records")
            else:
                raise ValueError("Invalid dataset format")
            
            return True
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return False
    
    def format_for_training(self) -> List[Dict[str, str]]:
        """Format dataset for causal language modeling."""
        formatted_data = []
        
        for record in self.dataset:
            try:
                user_prompt = record.get('user_prompt', '').strip()
                enhanced_prompt = record.get('enhanced_prompt', '').strip()
                task_type = record.get('task_type', 'general')
                
                if not user_prompt or not enhanced_prompt:
                    logger.warning(f"Skipping record with empty fields: {record}")
                    continue
                
                # Create training prompt in instruction format
                # Format: <s>[INST] {user_prompt} [/INST] {enhanced_prompt} </s>
                training_text = "<s>[INST] " + user_prompt + " [/INST] " + enhanced_prompt + " </s>"
                
                formatted_record = {
                    'text': training_text,
                    'user_prompt': user_prompt,
                    'enhanced_prompt': enhanced_prompt,
                    'task_type': task_type
                }
                
                formatted_data.append(formatted_record)
                
            except Exception as e:
                logger.error(f"Error formatting record: {e}")
                continue
        
        logger.info(f"Formatted {len(formatted_data)} records for training")
        return formatted_data
    
    def split_dataset(self, formatted_data: List[Dict[str, str]]) -> Tuple[List[Dict[str, str]], List[Dict[str, str]]]:
        """Split dataset into train and validation sets."""
        val_split = self.config['dataset']['validation_split']
        
        # Shuffle data
        import random
        random.shuffle(formatted_data)
        
        # Calculate split
        split_idx = int(len(formatted_data) * (1 - val_split))
        
        train_data = formatted_data[:split_idx]
        val_data = formatted_data[split_idx:]
        
        logger.info(f"Split dataset: {len(train_data)} train, {len(val_data)} validation")
        return train_data, val_data
    
    def save_datasets(self, train_data: List[Dict], val_data: List[Dict]) -> bool:
        """Save train and validation datasets."""
        try:
            output_dir = Path("finetune/data")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Save training data
            train_file = output_dir / "train.json"
            with open(train_file, 'w', encoding='utf-8') as f:
                json.dump(train_data, f, indent=2, ensure_ascii=False)
            
            # Save validation data
            val_file = output_dir / "validation.json"
            with open(val_file, 'w', encoding='utf-8') as f:
                json.dump(val_data, f, indent=2, ensure_ascii=False)
            
            # Save metadata
            metadata = {
                'train_samples': len(train_data),
                'val_samples': len(val_data),
                'total_samples': len(train_data) + len(val_data),
                'validation_split': self.config['dataset']['validation_split'],
                'task_distribution': self._get_task_distribution(train_data + val_data)
            }
            
            metadata_file = output_dir / "metadata.json"
            with open(metadata_file, 'w', encoding='utf-8') as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved datasets to {output_dir}")
            logger.info(f"Train: {len(train_data)}, Val: {len(val_data)}")
            
            return True
        except Exception as e:
            logger.error(f"Error saving datasets: {e}")
            return False
    
    def _get_task_distribution(self, data: List[Dict]) -> Dict[str, int]:
        """Get task type distribution."""
        distribution = {}
        for record in data:
            task_type = record.get('task_type', 'general')
            distribution[task_type] = distribution.get(task_type, 0) + 1
        return distribution
    
    def validate_dataset(self, data: List[Dict]) -> Dict[str, Any]:
        """Validate the prepared dataset."""
        validation_results = {
            'total_records': len(data),
            'valid_records': 0,
            'invalid_records': 0,
            'issues': []
        }
        
        for i, record in enumerate(data):
            try:
                text = record.get('text', '')
                user_prompt = record.get('user_prompt', '')
                enhanced_prompt = record.get('enhanced_prompt', '')
                
                # Basic validation
                if not text or not user_prompt or not enhanced_prompt:
                    validation_results['invalid_records'] += 1
                    validation_results['issues'].append(f"Record {i}: Missing required fields")
                    continue
                
                # Length validation
                if len(text) > self.config['dataset']['max_length']:
                    validation_results['issues'].append(f"Record {i}: Text too long ({len(text)} chars)")
                    continue
                
                validation_results['valid_records'] += 1
                
            except Exception as e:
                validation_results['invalid_records'] += 1
                validation_results['issues'].append(f"Record {i}: {str(e)}")
        
        return validation_results
    
    def prepare(self, input_file: str) -> bool:
        """Run the complete dataset preparation pipeline."""
        logger.info("Starting dataset preparation...")
        
        # Load dataset
        if not self.load_dataset(input_file):
            return False
        
        # Format for training
        formatted_data = self.format_for_training()
        if not formatted_data:
            logger.error("No valid data after formatting")
            return False
        
        # Validate formatted data
        validation = self.validate_dataset(formatted_data)
        logger.info(f"Validation results: {validation}")
        
        if validation['valid_records'] == 0:
            logger.error("No valid records in dataset")
            return False
        
        # Split dataset
        train_data, val_data = self.split_dataset(formatted_data)
        
        # Save datasets
        if not self.save_datasets(train_data, val_data):
            return False
        
        logger.info("✅ Dataset preparation completed successfully!")
        return True

def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Prepare dataset for fine-tuning")
    parser.add_argument("--input", default="promptgenius_training_data.json", 
                       help="Input dataset file")
    parser.add_argument("--config", default="finetune/config.yaml", 
                       help="Configuration file")
    
    args = parser.parse_args()
    
    preparer = DatasetPreparer(args.config)
    success = preparer.prepare(args.input)
    
    if success:
        print("✅ Dataset preparation completed successfully!")
        print("📁 Check finetune/data/ for prepared datasets")
    else:
        print("❌ Dataset preparation failed!")
        exit(1)

if __name__ == "__main__":
    main()
