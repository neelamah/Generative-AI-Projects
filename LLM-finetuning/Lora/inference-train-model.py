import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM
)

from peft import PeftModel


# ============================================================
# STEP 1: MODEL PATHS
# ============================================================

base_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

lora_path = "./lora_model"


# ============================================================
# STEP 2: LOAD TOKENIZER
# ============================================================

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    base_model_name
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


# ============================================================
# STEP 3: LOAD ORIGINAL BASE MODEL
# ============================================================

print("Loading base model...")

use_bf16 = torch.cuda.is_available() and torch.cuda.is_bf16_supported()

base_model = AutoModelForCausalLM.from_pretrained(

    base_model_name,

    torch_dtype=(
        torch.bfloat16
        if use_bf16
        else torch.float16
        if torch.cuda.is_available()
        else torch.float32
    ),

    device_map="auto"
)


# ============================================================
# STEP 4: LOAD TRAINED LoRA ADAPTER
# It is taking the original base model and attaching your trained LoRA adapter to it.
#LoRA does not train the entire base model. It only trains a small adapter that modifies how the base model behaves.
# ============================================================

print("Loading LoRA adapter...")

model = PeftModel.from_pretrained(
    base_model,
    lora_path
)


# ============================================================
# STEP 5: EVALUATION MODE
# ============================================================

model.eval()


# ============================================================
# STEP 6: NEW USER INPUT
# ============================================================

prompt = """
### Instruction:
Explain what QLoRA is.

### Response:
"""


# ============================================================
# STEP 7: TOKENIZE
# ============================================================

inputs = tokenizer(
    prompt,
    return_tensors="pt"
)

# Move tensors to model device
inputs = {
    key: value.to(model.device)
    for key, value in inputs.items()
}


# ============================================================
# STEP 8: GENERATE
# ============================================================

print("\nGenerating response...\n")

with torch.no_grad():

    outputs = model.generate(

        **inputs,

        # Maximum number of NEW tokens
        max_new_tokens=100,

        # Sampling
        do_sample=True,

        # Creativity
        temperature=0.7,

        # Prevent pad-token warning
        pad_token_id=tokenizer.eos_token_id
    )


# ============================================================
# STEP 9: DECODE
# ============================================================

response = tokenizer.decode(

    outputs[0],

    skip_special_tokens=True
)


# ============================================================
# STEP 10: DISPLAY RESULT
# ============================================================

print("==============================")
print("PROMPT")
print("==============================")

print(prompt)

print("\n==============================")
print("MODEL RESPONSE")
print("==============================")

print(response)