from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

class LLM:
    def __init__(self):
        # Initialize with a smaller model suitable for local deployment
        self.model_name = "facebook/opt-350m"  # Using OPT-350M as a more practical local model
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        
        # Move model to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def generate(self, user_input, context):
        """Generate a response based on user input and context."""
        # Construct the prompt
        if context:
            prompt = f"""Previous relevant interactions:
{context}

Current question: {user_input}

Based on the previous interactions and the current question, here's my response:"""
        else:
            prompt = f"Question: {user_input}\n\nResponse:"

        # Tokenize and generate
        inputs = self.tokenizer.encode(prompt, return_tensors='pt').to(self.device)
        
        # Generate with improved parameters
        outputs = self.model.generate(
            inputs,
            max_length=512,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        # Decode and clean up the response
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract the actual response part
        if "Response:" in response:
            response = response.split("Response:")[-1].strip()
        
        return response
