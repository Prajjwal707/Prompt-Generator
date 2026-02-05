"""
Data loading and processing script for PromptGenius.
Downloads and prepares the Alpaca dataset for fine-tuning.
"""

import json
import logging
from datasets import load_dataset
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_alpaca_dataset():
    """Download Alpaca dataset and save as JSON."""
    try:
        logger.info("Downloading Alpaca dataset...")
        dataset = load_dataset("tatsu-lab/alpaca")
        
        # Save training data to JSON
        output_file = "alpaca_data_cleaned.json"
        dataset['train'].to_json(output_file)
        
        logger.info(f"Dataset saved to {output_file}")
        logger.info(f"Total records: {len(dataset['train'])}")
        
        return True
    except Exception as e:
        logger.error(f"Error downloading dataset: {e}")
        return False

def validate_dataset_file(file_path: str) -> bool:
    """Validate that the dataset file exists and has valid JSON."""
    try:
        path = Path(file_path)
        if not path.exists():
            logger.error(f"Dataset file {file_path} does not exist")
            return False
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            logger.error("Dataset should be a list of records")
            return False
        
        logger.info(f"Dataset validation passed: {len(data)} records")
        return True
    except Exception as e:
        logger.error(f"Dataset validation failed: {e}")
        return False

def main():
    """Main execution function."""
    # Download dataset if not exists
    if not validate_dataset_file("alpaca_data_cleaned.json"):
        success = download_alpaca_dataset()
        if not success:
            logger.error("Failed to download dataset")
            return False
    
    # Run validation and cleaning scripts
    try:
        import subprocess
        import sys
        
        logger.info("Running data validation...")
        result = subprocess.run([sys.executable, "scripts/data_validation.py"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Data validation failed: {result.stderr}")
            return False
        
        logger.info("Running data cleaning...")
        result = subprocess.run([sys.executable, "scripts/data_cleaning.py"], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Data cleaning failed: {result.stderr}")
            return False
        
        logger.info("✅ Data pipeline completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error running data pipeline: {e}")
        return False

if __name__ == "__main__":
    main()
