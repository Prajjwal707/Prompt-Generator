"""
Data validation script for PromptGenius dataset.
Validates JSON schema, removes duplicates, and cleans data.
"""

import json
import logging
from typing import List, Dict, Any
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataValidator:
    """Validates and cleans Alpaca dataset for PromptGenius."""
    
    def __init__(self, input_file: str, output_file: str):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.data = []
        self.cleaned_data = []
        
    def load_data(self) -> bool:
        """Load JSON data from file."""
        try:
            with open(self.input_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            logger.info(f"Loaded {len(self.data)} records from {self.input_file}")
            return True
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False
    
    def validate_schema(self) -> bool:
        """Validate JSON schema for each record."""
        required_fields = ['instruction', 'input', 'output']
        valid_count = 0
        
        for record in self.data:
            if not isinstance(record, dict):
                logger.warning(f"Skipping non-dict record: {record}")
                continue
                
            # Check required fields
            if all(field in record for field in required_fields):
                # Ensure fields are strings
                if all(isinstance(record[field], str) for field in required_fields):
                    valid_count += 1
                    self.cleaned_data.append(record)
                else:
                    logger.warning(f"Record has non-string fields: {record.get('instruction', 'Unknown')[:50]}...")
            else:
                logger.warning(f"Record missing required fields: {record.get('instruction', 'Unknown')[:50]}...")
        
        logger.info(f"Validated {valid_count}/{len(self.data)} records")
        return valid_count > 0
    
    def remove_duplicates(self) -> int:
        """Remove duplicate records based on instruction."""
        seen_instructions = set()
        unique_data = []
        duplicate_count = 0
        
        for record in self.cleaned_data:
            instruction = record['instruction'].strip().lower()
            if instruction not in seen_instructions:
                seen_instructions.add(instruction)
                unique_data.append(record)
            else:
                duplicate_count += 1
        
        self.cleaned_data = unique_data
        logger.info(f"Removed {duplicate_count} duplicate records")
        return duplicate_count
    
    def remove_empty_samples(self) -> int:
        """Remove records with empty or whitespace-only content."""
        cleaned = []
        removed_count = 0
        
        for record in self.cleaned_data:
            instruction = record['instruction'].strip()
            output = record['output'].strip()
            
            if instruction and output and len(instruction) > 10 and len(output) > 20:
                cleaned.append(record)
            else:
                removed_count += 1
                logger.debug(f"Removed empty/short sample: {instruction[:50]}...")
        
        self.cleaned_data = cleaned
        logger.info(f"Removed {removed_count} empty/short samples")
        return removed_count
    
    def normalize_fields(self) -> None:
        """Normalize instruction and output fields."""
        for record in self.cleaned_data:
            record['instruction'] = record['instruction'].strip()
            record['input'] = record['input'].strip()
            record['output'] = record['output'].strip()
            
            # Remove excessive whitespace
            record['instruction'] = ' '.join(record['instruction'].split())
            record['input'] = ' '.join(record['input'].split())
            record['output'] = ' '.join(record['output'].split())
    
    def save_cleaned_data(self) -> bool:
        """Save cleaned data to output file."""
        try:
            # Ensure output directory exists
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(self.cleaned_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved {len(self.cleaned_data)} cleaned records to {self.output_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving cleaned data: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Generate dataset statistics."""
        if not self.cleaned_data:
            return {}
        
        instruction_lengths = [len(record['instruction']) for record in self.cleaned_data]
        output_lengths = [len(record['output']) for record in self.cleaned_data]
        
        stats = {
            'total_records': len(self.cleaned_data),
            'avg_instruction_length': sum(instruction_lengths) / len(instruction_lengths),
            'avg_output_length': sum(output_lengths) / len(output_lengths),
            'min_instruction_length': min(instruction_lengths),
            'max_instruction_length': max(instruction_lengths),
            'min_output_length': min(output_lengths),
            'max_output_length': max(output_lengths)
        }
        
        return stats
    
    def validate(self) -> bool:
        """Run complete validation pipeline."""
        logger.info("Starting data validation pipeline...")
        
        if not self.load_data():
            return False
        
        if not self.validate_schema():
            return False
        
        self.remove_duplicates()
        self.remove_empty_samples()
        self.normalize_fields()
        
        stats = self.get_statistics()
        logger.info(f"Dataset statistics: {stats}")
        
        if not self.save_cleaned_data():
            return False
        
        logger.info("Data validation completed successfully!")
        return True

def main():
    """Main execution function."""
    input_file = "alpaca_data_cleaned.json"
    output_file = "alpaca_data_cleaned.json"  # Overwrite with cleaned version
    
    validator = DataValidator(input_file, output_file)
    success = validator.validate()
    
    if success:
        print("✅ Data validation completed successfully!")
    else:
        print("❌ Data validation failed!")
        exit(1)

if __name__ == "__main__":
    main()
