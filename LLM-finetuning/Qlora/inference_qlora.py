import torch

from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    BitsAndBytesConfig
)

from peft import PeftModel


# ============================================================
# STEP 1: MODEL PATH
# ============================================================

base_model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

qlora_path = "./qlora_model"


# ============================================================
# STEP 2: TOKENIZER
# ============================================================

print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(
    base_model_name
)

if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token


# ============================================================
# STEP 3: 4-BIT CONFIG
# ============================================================

use_bf16 = (
    torch.cuda.is_available()
    and torch.cuda.is_bf16_supported()
)

compute_dtype = (
    torch.bfloat16
    if use_bf16
    else torch.float16
)


bnb_config = BitsAndBytesConfig(

    load_in_4bit=True,

    bnb_4bit_quant_type="nf4",

    bnb_4bit_compute_dtype=compute_dtype,

    bnb_4bit_use_double_quant=True
)


# ============================================================
# STEP 4: LOAD 4-BIT BASE MODEL
# ============================================================

print("Loading 4-bit base model...")

base_model = AutoModelForCausalLM.from_pretrained(

    base_model_name,

    quantization_config=bnb_config,

    device_map="auto"
)


# ============================================================
# STEP 5: LOAD TRAINED QLoRA ADAPTER
# ============================================================

print("Loading trained QLoRA adapter...")

model = PeftModel.from_pretrained(

    base_model,

    qlora_path
)


# ============================================================
# STEP 6: EVALUATION MODE
# ============================================================

model.eval()


# ============================================================
# STEP 7: NEW PROMPT
# ============================================================

prompt = """
### Instruction:
Explain QLoRA in simple words.

### Response:
"""


# ============================================================
# STEP 8: TOKENIZE
# ============================================================

inputs = tokenizer(
    prompt,
    return_tensors="pt"
)

inputs = {
    key: value.to(model.device)
    for key, value in inputs.items()
}


# ============================================================
# STEP 9: GENERATE
# ============================================================

print("\nGenerating response...\n")

with torch.no_grad():

    outputs = model.generate(

        **inputs,

        max_new_tokens=100,

        do_sample=True,

        temperature=0.7,

        top_p=0.9,

        pad_token_id=tokenizer.eos_token_id
    )


# ============================================================
# STEP 10: DECODE
# ============================================================

response = tokenizer.decode(

    outputs[0],

    skip_special_tokens=True
)


# ============================================================
# STEP 11: PRINT
# ============================================================

print("===================================")
print("MODEL RESPONSE")
print("===================================")

print(response)