"""
Training script for PromptGenius fine-tuning.
Implements LoRA/QLoRA fine-tuning with HuggingFace Trainer.
"""

import os
import logging
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import torch
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling,
    EarlyStoppingCallback
)
from peft import (
    LoraConfig,
    get_peft_model,
    prepare_model_for_kbit_training,
    TaskType
)
from datasets import load_from_disk
import bitsandbytes as bnb

logger = logging.getLogger(__name__)

class PromptGeniusTrainer:
    """Fine-tuning trainer for PromptGenius."""
    
    def __init__(self, config_path: str = "finetune/config.yaml"):
        self.config = self._load_config(config_path)
        self.model = None
        self.tokenizer = None
        self.train_dataset = None
        self.val_dataset = None
        self.trainer = None
    
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
    
    def setup_model_and_tokenizer(self) -> bool:
        """Setup model and tokenizer."""
        try:
            model_name = self.config['model']['base_model']
            logger.info(f"Loading model: {model_name}")
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=self.config['model']['trust_remote_code'],
                use_auth_token=self.config['model']['use_auth_token']
            )
            
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Configure quantization if using QLoRA
            if self.config['qlora']['load_in_4bit']:
                logger.info("Using 4-bit quantization (QLoRA)")
                
                # Configure bnb quantization config
                bnb_config = bnb.BitsAndBytesConfig(
                    load_in_4bit=self.config['qlora']['load_in_4bit'],
                    bnb_4bit_compute_dtype=getattr(torch, self.config['qlora']['bnb_4bit_compute_dtype']),
                    bnb_4bit_use_double_quant=self.config['qlora']['bnb_4bit_use_double_quant'],
                    bnb_4bit_quant_type=self.config['qlora']['bnb_4bit_quant_type']
                )
                
                # Load model with quantization
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    quantization_config=bnb_config,
                    trust_remote_code=self.config['model']['trust_remote_code'],
                    use_auth_token=self.config['model']['use_auth_token'],
                    device_map=self.config['hardware']['device']
                )
                
                # Prepare model for k-bit training
                self.model = prepare_model_for_kbit_training(self.model)
                
            else:
                # Load model without quantization
                self.model = AutoModelForCausalLM.from_pretrained(
                    model_name,
                    trust_remote_code=self.config['model']['trust_remote_code'],
                    use_auth_token=self.config['model']['use_auth_token'],
                    torch_dtype=torch.float16 if self.config['hardware']['mixed_precision'] == 'fp16' else torch.float32,
                    device_map=self.config['hardware']['device']
                )
            
            # Setup LoRA
            lora_config = LoraConfig(
                r=self.config['lora']['r'],
                lora_alpha=self.config['lora']['lora_alpha'],
                target_modules=self.config['lora']['target_modules'],
                lora_dropout=self.config['lora']['lora_dropout'],
                bias=self.config['lora']['bias'],
                task_type=TaskType.CAUSAL_LM
            )
            
            # Apply LoRA to model
            self.model = get_peft_model(self.model, lora_config)
            
            # Enable gradient checkpointing if specified
            if self.config['hardware']['gradient_checkpointing']:
                self.model.gradient_checkpointing_enable()
            
            # Print trainable parameters
            trainable_params = sum(p.numel() for p in self.model.parameters() if p.requires_grad)
            total_params = sum(p.numel() for p in self.model.parameters())
            logger.info(f"Trainable parameters: {trainable_params:,} / {total_params:,} ({100 * trainable_params / total_params:.2f}%)")
            
            return True
            
        except Exception as e:
            logger.error(f"Error setting up model and tokenizer: {e}")
            return False
    
    def load_datasets(self) -> bool:
        """Load tokenized datasets."""
        try:
            data_dir = Path("finetune/tokenized")
            
            self.train_dataset = load_from_disk(data_dir / "train")
            self.val_dataset = load_from_disk(data_dir / "validation")
            
            logger.info(f"Loaded datasets: Train={len(self.train_dataset)}, Val={len(self.val_dataset)}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading datasets: {e}")
            return False
    
    def setup_trainer(self) -> bool:
        """Setup the HuggingFace Trainer."""
        try:
            # Training arguments
            training_args = TrainingArguments(
                output_dir=self.config['training']['output_dir'],
                num_train_epochs=self.config['training']['num_train_epochs'],
                per_device_train_batch_size=self.config['training']['per_device_train_batch_size'],
                per_device_eval_batch_size=self.config['training']['per_device_eval_batch_size'],
                gradient_accumulation_steps=self.config['training']['gradient_accumulation_steps'],
                learning_rate=self.config['training']['learning_rate'],
                weight_decay=self.config['training']['weight_decay'],
                warmup_ratio=self.config['training']['warmup_ratio'],
                max_grad_norm=self.config['training']['max_grad_norm'],
                lr_scheduler_type=self.config['training']['lr_scheduler_type'],
                logging_steps=self.config['training']['logging_steps'],
                save_steps=self.config['training']['save_steps'],
                eval_steps=self.config['training']['eval_steps'],
                save_total_limit=self.config['training']['save_total_limit'],
                load_best_model_at_end=self.config['training']['load_best_model_at_end'],
                metric_for_best_model=self.config['training']['metric_for_best_model'],
                greater_is_better=self.config['training']['greater_is_better'],
                fp16=self.config['training']['fp16'],
                dataloader_num_workers=self.config['training']['dataloader_num_workers'],
                remove_unused_columns=self.config['training']['remove_unused_columns'],
                report_to=self.config['logging']['report_to'],
                logging_dir=f"{self.config['training']['output_dir']}/logs"
            )
            
            # Data collator
            data_collator = DataCollatorForLanguageModeling(
                tokenizer=self.tokenizer,
                mlm=False,  # Causal language modeling
                pad_to_multiple_of=8
            )
            
            # Setup callbacks
            callbacks = []
            if self.config['early_stopping']['enabled']:
                callbacks.append(
                    EarlyStoppingCallback(
                        early_stopping_patience=self.config['early_stopping']['patience'],
                        early_stopping_threshold=self.config['early_stopping']['min_delta']
                    )
                )
            
            # Create trainer
            self.trainer = Trainer(
                model=self.model,
                args=training_args,
                train_dataset=self.train_dataset,
                eval_dataset=self.val_dataset,
                tokenizer=self.tokenizer,
                data_collator=data_collator,
                callbacks=callbacks
            )
            
            logger.info("Trainer setup completed")
            return True
            
        except Exception as e:
            logger.error(f"Error setting up trainer: {e}")
            return False
    
    def compute_metrics(self, eval_pred) -> Dict[str, float]:
        """Compute evaluation metrics."""
        try:
            predictions, labels = eval_pred
            
            # For causal LM, we typically use perplexity
            # This is a simplified metric calculation
            loss = torch.tensor(predictions).mean().item()
            perplexity = torch.exp(torch.tensor(loss)).item()
            
            return {
                'eval_loss': loss,
                'perplexity': perplexity
            }
        except Exception as e:
            logger.error(f"Error computing metrics: {e}")
            return {}
    
    def train(self) -> bool:
        """Start training."""
        try:
            logger.info("Starting training...")
            
            # Start training
            train_result = self.trainer.train()
            
            # Log training results
            logger.info(f"Training completed. Final loss: {train_result.training_loss}")
            
            # Save final model
            self.trainer.save_model()
            self.tokenizer.save_pretrained(self.config['training']['output_dir'])
            
            # Save training logs
            train_result.save_to_json(f"{self.config['training']['output_dir']}/train_results.json")
            
            logger.info("Training completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error during training: {e}")
            return False
    
    def evaluate(self) -> Dict[str, Any]:
        """Evaluate the trained model."""
        try:
            logger.info("Starting evaluation...")
            
            eval_result = self.trainer.evaluate()
            
            logger.info(f"Evaluation results: {eval_result}")
            
            # Save evaluation results
            with open(f"{self.config['training']['output_dir']}/eval_results.json", 'w') as f:
                import json
                json.dump(eval_result, f, indent=2)
            
            return eval_result
            
        except Exception as e:
            logger.error(f"Error during evaluation: {e}")
            return {}
    
    def run_training(self) -> bool:
        """Run the complete training pipeline."""
        logger.info("Starting fine-tuning pipeline...")
        
        # Setup model and tokenizer
        if not self.setup_model_and_tokenizer():
            return False
        
        # Load datasets
        if not self.load_datasets():
            return False
        
        # Setup trainer
        if not self.setup_trainer():
            return False
        
        # Train model
        if not self.train():
            return False
        
        # Evaluate model
        eval_results = self.evaluate()
        if eval_results:
            logger.info(f"Final evaluation: {eval_results}")
        
        logger.info("✅ Fine-tuning completed successfully!")
        return True

def main():
    """Main execution function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Fine-tune PromptGenius model")
    parser.add_argument("--config", default="finetune/config.yaml", 
                       help="Configuration file")
    parser.add_argument("--resume", action="store_true",
                       help="Resume from checkpoint")
    
    args = parser.parse_args()
    
    trainer = PromptGeniusTrainer(args.config)
    success = trainer.run_training()
    
    if success:
        print("✅ Fine-tuning completed successfully!")
        print(f"📁 Check {trainer.config['training']['output_dir']} for the trained model")
    else:
        print("❌ Fine-tuning failed!")
        exit(1)

if __name__ == "__main__":
    main()
