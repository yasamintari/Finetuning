# Model Information: databricks-gpt-oss-120b

## Overview

This demo uses **databricks-gpt-oss-120b**, an open-source GPT model with 120 billion parameters.

## Key Specifications

- **Parameters**: 120 billion
- **Architecture**: GPT-style transformer decoder
- **License**: Open source
- **Provider**: Databricks
- **Training**: Pre-trained on diverse text corpus

## Why This Model?

1. **Open Source**: Fully open-source GPT model (no API restrictions)
2. **Large Scale**: 120B parameters provide strong baseline capabilities
3. **Databricks Native**: Optimized for Databricks platform
4. **Commercial Use**: Permissive license allows commercial applications

## Hardware Requirements

### Minimum (Inference)
- 4x A100 (40GB) GPUs
- ~240GB GPU memory total (FP16)

### Recommended (Fine-tuning)
- 8x A100 (80GB) GPUs or equivalent
- Enables larger batch sizes and faster training

### Databricks Instance Types
- **AWS**: `g5.12xlarge`, `p4d.24xlarge`, `p4de.24xlarge`
- **Azure**: `Standard_NC24ads_A100_v4`, `Standard_ND96asr_v4`
- **GCP**: `a2-ultragpu-8g`, `a2-megagpu-16g`

## Memory Optimizations in Demo

The notebook uses several techniques to fit this large model:

1. **FP16 Mixed Precision**: Reduces memory by 2x (16-bit vs 32-bit)
2. **Gradient Accumulation**: Simulates larger batch without loading more data
3. **Gradient Checkpointing**: Trades compute for memory (recompute activations)
4. **Device Mapping**: Automatically distributes model across GPUs

## Model Loading

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained(
    "databricks-gpt-oss-120b",
    trust_remote_code=True,
    torch_dtype=torch.float16,  # FP16 for efficiency
    device_map="auto"           # Auto-distribute across GPUs
)

tokenizer = AutoTokenizer.from_pretrained(
    "databricks-gpt-oss-120b",
    trust_remote_code=True
)
```

## Fine-tuning Considerations

### Full Fine-tuning (This Demo)
- Updates all 120B parameters
- Requires significant GPU memory
- Best quality but most expensive

### Alternative: LoRA (Recommended for Production)
- Only trains ~0.1-1% of parameters (100M-1B params)
- 10-100x less memory required
- Can run on smaller GPU instances
- Slightly lower quality but much more practical

```python
from peft import LoraConfig, get_peft_model

lora_config = LoraConfig(
    r=16,  # Rank
    lora_alpha=32,
    target_modules=["q_proj", "v_proj", "k_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
# Now only trains ~200M parameters instead of 120B!
```

## Performance Expectations

### Training Time (Full Fine-tuning)
- **Single A100 (80GB)**: ~4-6 hours for 3 epochs (if it fits)
- **4x A100 (40GB)**: ~2-3 hours for 3 epochs
- **8x A100 (80GB)**: ~1-2 hours for 3 epochs

### Training Time (LoRA)
- **Single A100**: ~30-45 minutes for 3 epochs
- **4x A100**: ~15-20 minutes for 3 epochs

### Inference Speed
- **Batch size 1**: ~50-100 tokens/second
- **Batch size 8**: ~300-500 tokens/second (with vLLM)

## Cost Considerations (AWS us-east-1)

### Training Costs
- **p4d.24xlarge** (8x A100 80GB): ~$32/hour
- **3 hour training run**: ~$96
- **With spot instances**: ~$30-40

### LoRA Alternative
- **g5.12xlarge** (4x A24G 24GB): ~$5/hour
- **1 hour training**: ~$5
- **20x cheaper than full fine-tuning!**

## Recommendations

For production use:
1. **Start with LoRA** - much more cost-effective
2. **Scale to full fine-tuning** only if LoRA quality insufficient
3. **Use quantization** (8-bit/4-bit) for inference
4. **Deploy with vLLM** for fast serving

## References

- [Databricks Model Documentation](https://docs.databricks.com/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [LoRA Paper](https://arxiv.org/abs/2106.09685)
- [vLLM for Serving](https://github.com/vllm-project/vllm)
