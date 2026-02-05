"""
Evaluation script for PromptGenius fine-tuned model.
Computes BLEU, ROUGE, and other metrics.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Tuple
import yaml
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from datasets import load_from_disk
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import numpy as np

logger = logging.getLogger(__name__)

class ModelEvaluator:
    """Evaluates fine-tuned model performance."""
    
    def __init__(self, config_path: str = "finetune/config.yaml"):
        self.config = self._load_config(config_path)
        self.model = None
        self.tokenizer = None
        self.val_dataset = None
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    
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
    
    def load_model_and_tokenizer(self, model_path: str) -> bool:
        """Load fine-tuned model and tokenizer."""
        try:
            logger.info(f"Loading model from: {model_path}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=torch.float16,
                device_map="auto"
            )
            
            self.model.eval()
            logger.info("Model and tokenizer loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def load_validation_dataset(self) -> bool:
        """Load validation dataset."""
        try:
            data_dir = Path("finetune/tokenized")
            self.val_dataset = load_from_disk(data_dir / "validation")
            
            logger.info(f"Loaded validation dataset: {len(self.val_dataset)} samples")
            return True
            
        except Exception as e:
            logger.error(f"Error loading validation dataset: {e}")
            return False
    
    def generate_response(self, input_text: str, max_new_tokens: int = 256) -> str:
        """Generate response from the model."""
        try:
            # Prepare input
            prompt = f"<s>[INST] {input_text} [/INST]"
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            
            # Move to device
            inputs = {k: v.to(self.model.device) for k, v in inputs.items()}
            
            # Generate
            with torch.no_grad():
                generation_config = GenerationConfig(
                    max_new_tokens=max_new_tokens,
                    temperature=self.config['evaluation']['generation_config']['temperature'],
                    top_p=self.config['evaluation']['generation_config']['top_p'],
                    do_sample=self.config['evaluation']['generation_config']['do_sample'],
                    pad_token_id=self.tokenizer.pad_token_id
                )
                
                outputs = self.model.generate(
                    **inputs,
                    generation_config=generation_config
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the generated part (after [/INST])
            if "[/INST]" in response:
                response = response.split("[/INST]")[1].strip()
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return ""
    
    def compute_bleu_score(self, reference: str, candidate: str) -> float:
        """Compute BLEU score."""
        try:
            # Tokenize sentences
            reference_tokens = reference.split()
            candidate_tokens = candidate.split()
            
            # Compute BLEU with smoothing
            smoothing = SmoothingFunction().method1
            bleu_score = sentence_bleu(
                [reference_tokens], 
                candidate_tokens, 
                smoothing_function=smoothing
            )
            
            return bleu_score
            
        except Exception as e:
            logger.error(f"Error computing BLEU score: {e}")
            return 0.0
    
    def compute_rouge_scores(self, reference: str, candidate: str) -> Dict[str, float]:
        """Compute ROUGE scores."""
        try:
            scores = self.rouge_scorer.score(reference, candidate)
            
            return {
                'rouge1': scores['rouge1'].fmeasure,
                'rouge2': scores['rouge2'].fmeasure,
                'rougeL': scores['rougeL'].fmeasure
            }
            
        except Exception as e:
            logger.error(f"Error computing ROUGE scores: {e}")
            return {'rouge1': 0.0, 'rouge2': 0.0, 'rougeL': 0.0}
    
    def compute_semantic_similarity(self, reference: str, candidate: str) -> float:
        """Compute semantic similarity (simplified)."""
        try:
            # Simple word overlap similarity as placeholder
            ref_words = set(reference.lower().split())
            cand_words = set(candidate.lower().split())
            
            intersection = ref_words.intersection(cand_words)
            union = ref_words.union(cand_words)
            
            if len(union) == 0:
                return 0.0
            
            similarity = len(intersection) / len(union)
            return similarity
            
        except Exception as e:
            logger.error(f"Error computing semantic similarity: {e}")
            return 0.0
    
    def evaluate_sample(self, user_prompt: str, reference_enhanced: str) -> Dict[str, Any]:
        """Evaluate a single sample."""
        try:
            # Generate response
            generated = self.generate_response(user_prompt)
            
            # Compute metrics
            bleu = self.compute_bleu_score(reference_enhanced, generated)
            rouge = self.compute_rouge_scores(reference_enhanced, generated)
            semantic_sim = self.compute_semantic_similarity(reference_enhanced, generated)
            
            # Length metrics
            ref_length = len(reference_enhanced.split())
            gen_length = len(generated.split())
            length_ratio = gen_length / ref_length if ref_length > 0 else 0
            
            return {
                'user_prompt': user_prompt,
                'reference': reference_enhanced,
                'generated': generated,
                'bleu': bleu,
                'rouge1': rouge['rouge1'],
                'rouge2': rouge['rouge2'],
                'rougeL': rouge['rougeL'],
                'semantic_similarity': semantic_sim,
                'ref_length': ref_length,
                'gen_length': gen_length,
                'length_ratio': length_ratio
            }
            
        except Exception as e:
            logger.error(f"Error evaluating sample: {e}")
            return {}
    
    def evaluate_dataset(self, num_samples: int = 100) -> Dict[str, Any]:
        """Evaluate on validation dataset."""
        try:
            logger.info(f"Evaluating on {num_samples} samples...")
            
            # Load original validation data for prompts
            with open("finetune/data/validation.json", 'r') as f:
                val_data = json.load(f)
            
            # Sample data
            if len(val_data) > num_samples:
                import random
                val_data = random.sample(val_data, num_samples)
            
            results = []
            total_metrics = {
                'bleu': [],
                'rouge1': [],
                'rouge2': [],
                'rougeL': [],
                'semantic_similarity': [],
                'length_ratio': []
            }
            
            for i, sample in enumerate(val_data):
                logger.info(f"Evaluating sample {i+1}/{len(val_data)}")
                
                result = self.evaluate_sample(
                    sample['user_prompt'],
                    sample['enhanced_prompt']
                )
                
                if result:
                    results.append(result)
                    
                    # Accumulate metrics
                    for metric in total_metrics:
                        total_metrics[metric].append(result[metric])
            
            # Compute averages
            avg_metrics = {}
            for metric, values in total_metrics.items():
                if values:
                    avg_metrics[f'avg_{metric}'] = np.mean(values)
                    avg_metrics[f'std_{metric}'] = np.std(values)
                else:
                    avg_metrics[f'avg_{metric}'] = 0.0
                    avg_metrics[f'std_{metric}'] = 0.0
            
            evaluation_results = {
                'num_samples': len(results),
                'metrics': avg_metrics,
                'detailed_results': results[:10]  # Save first 10 detailed results
            }
            
            return evaluation_results
            
        except Exception as e:
            logger.error(f"Error evaluating dataset: {e}")
            return {}
    
    def save_evaluation_results(self, results: Dict[str, Any], output_path: str) -> bool:
        """Save evaluation results."""
        try:
            with open(output_path, 'w') as f:
                json.dump(results, f, indent=2)
            
            logger.info(f"Evaluation results saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving results: {e}")
            return False
    
    def evaluate(self, model_path: str, num_samples: int = 100) -> bool:
        """Run complete evaluation."""
        logger.info("Starting model evaluation...")
        
        # Load model and tokenizer
        if not self.load_model_and_tokenizer(model_path):
            return False
        
        # Load validation dataset
        if not self.load_validation_dataset():
            return False
        
        # Evaluate
        results = self.evaluate_dataset(num_samples)
        
        if not results:
            logger.error("Evaluation failed")
            return False
        
        # Save results
        output_path = f"{model_path}/evaluation_results.json"
        if not self.save_evaluation_results(results, output_path):
            return False
        
        # Print summary
        metrics = results['metrics']
        logger.info("=== Evaluation Results ===")
        logger.info(f"Samples evaluated: {results['num_samples']}")
        logger.info(f"Average BLEU: {metrics.get('avg_bleu', 0):.4f}")
        logger.info(f"Average ROUGE-1: {metrics.get('avg_rouge1', 0):.4f}")
        logger.info(f"Average ROUGE-2: {metrics.get('avg_rouge2', 0):.4f}")
        logger.info(f"Average ROUGE-L: {metrics.get('avg_rougeL', 0):.4f}")
        logger.info(f"Average Semantic Similarity: {metrics.get('avg_semantic_similarity', 0):.4f}")
        logger.info("========================")
        
        logger.info("✅ Evaluation completed successfully!")
        return True

def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Evaluate fine-tuned model")
    parser.add_argument("--model", required=True, help="Path to fine-tuned model")
    parser.add_argument("--samples", type=int, default=100, help="Number of samples to evaluate")
    parser.add_argument("--config", default="finetune/config.yaml", help="Configuration file")
    
    args = parser.parse_args()
    
    evaluator = ModelEvaluator(args.config)
    success = evaluator.evaluate(args.model, args.samples)
    
    if success:
        print("✅ Model evaluation completed successfully!")
        print(f"📊 Check {args.model}/evaluation_results.json for detailed results")
    else:
        print("❌ Model evaluation failed!")
        exit(1)

if __name__ == "__main__":
    main()
