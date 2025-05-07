import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

class AIModel:
    def __init__(self):
        self.tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
        self.model = GPT2LMHeadModel.from_pretrained("gpt2")

    def generate_response(self, prompt, max_length=100):
        input_ids = self.tokenizer.encode(prompt, return_tensors="pt")
        with torch.no_grad():
            output = self.model.generate(input_ids, max_length=max_length, num_return_sequences=1)
        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return response