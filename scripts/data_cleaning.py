"""
Data cleaning script for converting Alpaca format to PromptGenius format.
Converts instruction/input/output to user_prompt/enhanced_prompt format.
"""

import json
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import re

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataCleaner:
    """Cleans and converts Alpaca data to PromptGenius format."""
    
    def __init__(self, input_file: str, output_file: str):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.data = []
        self.converted_data = []
        
        # Task type mapping based on keywords
        self.task_keywords = {
            'website': ['website', 'web', 'app', 'code', 'programming', 'development', 'html', 'css', 'javascript', 'python', 'react', 'vue', 'angular'],
            'image': ['image', 'photo', 'picture', 'edit', 'design', 'graphic', 'visual', 'art', 'drawing', 'illustration'],
            'ppt': ['presentation', 'powerpoint', 'slides', 'ppt', 'deck', 'talk', 'speech'],
            'general': []  # Default
        }
    
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
    
    def detect_task_type(self, instruction: str, input_text: str) -> str:
        """Detect task type based on content keywords."""
        combined_text = f"{instruction} {input_text}".lower()
        
        for task_type, keywords in self.task_keywords.items():
            if task_type == 'general':
                continue
            for keyword in keywords:
                if keyword in combined_text:
                    return task_type
        
        return 'general'
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters that might cause issues
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}\/\@\#\$\%\&\*\+\=\~\`\'\"]', '', text)
        
        return text
    
    def convert_to_promptgenius_format(self) -> None:
        """Convert Alpaca format to PromptGenius format."""
        for record in self.data:
            if not isinstance(record, dict):
                continue
            
            instruction = record.get('instruction', '').strip()
            input_text = record.get('input', '').strip()
            output = record.get('output', '').strip()
            
            if not instruction or not output:
                continue
            
            # Detect task type
            task_type = self.detect_task_type(instruction, input_text)
            
            # Create user prompt (combine instruction and input)
            if input_text:
                user_prompt = f"{instruction}\n\nAdditional context: {input_text}"
            else:
                user_prompt = instruction
            
            # Clean text
            user_prompt = self.clean_text(user_prompt)
            enhanced_prompt = self.clean_text(output)
            
            # Create PromptGenius record
            converted_record = {
                "user_prompt": user_prompt,
                "enhanced_prompt": enhanced_prompt,
                "task_type": task_type,
                "original_instruction": instruction,
                "original_input": input_text,
                "original_output": output
            }
            
            self.converted_data.append(converted_record)
        
        logger.info(f"Converted {len(self.converted_data)} records to PromptGenius format")
    
    def filter_by_quality(self) -> None:
        """Filter records based on quality metrics."""
        filtered_data = []
        
        for record in self.converted_data:
            user_prompt = record['user_prompt']
            enhanced_prompt = record['enhanced_prompt']
            
            # Quality checks
            if (len(user_prompt) >= 20 and 
                len(enhanced_prompt) >= 50 and
                len(user_prompt) <= 1000 and
                len(enhanced_prompt) <= 2000 and
                not user_prompt.isupper() and
                not enhanced_prompt.isupper()):
                filtered_data.append(record)
        
        self.converted_data = filtered_data
        logger.info(f"Filtered to {len(self.converted_data)} high-quality records")
    
    def add_metadata(self) -> None:
        """Add metadata to the dataset."""
        task_type_counts = {}
        for record in self.converted_data:
            task_type = record['task_type']
            task_type_counts[task_type] = task_type_counts.get(task_type, 0) + 1
        
        metadata = {
            "dataset_name": "PromptGenius-Training-Data",
            "version": "1.0",
            "total_records": len(self.converted_data),
            "task_distribution": task_type_counts,
            "conversion_date": "2026-02-05",
            "source": "Alpaca dataset converted to PromptGenius format"
        }
        
        # Create final dataset with metadata
        final_dataset = {
            "metadata": metadata,
            "data": self.converted_data
        }
        
        self.converted_data = final_dataset
    
    def save_converted_data(self) -> bool:
        """Save converted data to output file."""
        try:
            # Ensure output directory exists
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.output_file, 'w', encoding='utf-8') as f:
                json.dump(self.converted_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved converted data to {self.output_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving converted data: {e}")
            return False
    
    def generate_statistics(self) -> Dict[str, Any]:
        """Generate conversion statistics."""
        if not isinstance(self.converted_data, dict) or 'data' not in self.converted_data:
            return {}
        
        data = self.converted_data['data']
        task_counts = {}
        prompt_lengths = []
        enhanced_lengths = []
        
        for record in data:
            task_type = record['task_type']
            task_counts[task_type] = task_counts.get(task_type, 0) + 1
            
            prompt_lengths.append(len(record['user_prompt']))
            enhanced_lengths.append(len(record['enhanced_prompt']))
        
        stats = {
            'total_records': len(data),
            'task_distribution': task_counts,
            'avg_prompt_length': sum(prompt_lengths) / len(prompt_lengths) if prompt_lengths else 0,
            'avg_enhanced_length': sum(enhanced_lengths) / len(enhanced_lengths) if enhanced_lengths else 0,
            'conversion_success_rate': len(data) / len(self.data) * 100 if self.data else 0
        }
        
        return stats
    
    def clean(self) -> bool:
        """Run complete cleaning pipeline."""
        logger.info("Starting data cleaning pipeline...")
        
        if not self.load_data():
            return False
        
        self.convert_to_promptgenius_format()
        self.filter_by_quality()
        self.add_metadata()
        
        stats = self.generate_statistics()
        logger.info(f"Conversion statistics: {stats}")
        
        if not self.save_converted_data():
            return False
        
        logger.info("Data cleaning completed successfully!")
        return True

def main():
    """Main execution function."""
    input_file = "alpaca_data_cleaned.json"
    output_file = "promptgenius_training_data.json"
    
    cleaner = DataCleaner(input_file, output_file)
    success = cleaner.clean()
    
    if success:
        print("✅ Data cleaning completed successfully!")
        print(f"📊 Check {output_file} for the converted dataset")
    else:
        print("❌ Data cleaning failed!")
        exit(1)

if __name__ == "__main__":
    main()
