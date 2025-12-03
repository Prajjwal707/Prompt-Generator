from datasets import load_dataset

dataset = load_dataset("tatsu-lab/alpaca")

dataset['train'].to_json("alpaca_data.json")
