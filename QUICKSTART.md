# Quick Start Guide

## 🎯 Clear Problem Definition

**Business Problem**: Hedge fund analysts repeatedly answer similar questions about portfolio analysis, risk metrics, and investment strategies. This is time-consuming.

**Solution**: Train an AI model to automatically answer these questions using past expert responses.

**ML Approach**: Supervised fine-tuning
- **Input**: Question text
- **Label**: Expert answer text (the "supervision" signal)
- **Model**: Databricks GPT-OSS-120B fine-tuned on 20 Q&A pairs

## 📊 The Dataset (training_data.csv)

**What it contains**: 20 rows of labeled data

| Column | Description | Example |
|--------|-------------|---------|
| `question` | The input (what users ask) | "What's your outlook on tech stocks?" |
| `answer` | The label (what model should learn to predict) | "Technology sector shows momentum... recommend 25% allocation..." |

**Key point**: The `answer` column is the **supervised label** - this is what we're teaching the model to predict!

## 🔄 Simple Workflow

```
1. Load training_data.csv (20 labeled examples)
   ↓
2. Load pre-trained Databricks GPT-OSS-120B (powerful 120B param model)
   ↓
3. Fine-tune: Train model to predict answers given questions
   - Use FP16 mixed precision
   - Gradient accumulation for memory efficiency
   ↓
4. Test: Ask new questions, see if model generates good answers
   ↓
5. Save to Databricks Unity Catalog
```

## 🚀 How to Run

### Step 1: Upload Files to Databricks

1. Go to your Databricks workspace
2. Upload `training_data.csv` to DBFS:
   ```python
   # In a notebook cell:
   import shutil
   shutil.copy("/path/to/training_data.csv", "/dbfs/FileStore/training_data.csv")
   ```

3. Import `Simple_Supervised_Finetuning.ipynb`

### Step 2: Create a GPU Cluster

**Important**: This model requires GPU resources!

- Runtime: 14.3 LTS ML or later
- Node: GPU instance (e.g., **g5.12xlarge** or **A100**)
- Workers: Multi-node for faster training (recommended: 2-4 GPU nodes)
- Enable Unity Catalog

### Step 3: Run the Notebook

1. Attach notebook to GPU cluster
2. Run all cells (Shift + Enter)
3. Training takes ~30-60 minutes (depends on GPU configuration)

**Note**: The databricks-gpt-oss-120b is a 120 billion parameter model, so it requires significant GPU memory.

### Step 4: Test Your Model

The notebook will automatically test with new questions!

## 💡 Key Concepts Explained Simply

### What is "Supervised" Learning?

Imagine teaching a student:
- You show them questions AND the correct answers (labels)
- They practice predicting answers
- You correct them when wrong (that's the loss function)
- They improve over time (that's training!)

### What is "Fine-tuning"?

- GPT-2 already knows English grammar and general knowledge
- We're **adapting** it to speak like a hedge fund analyst
- Much faster than training from scratch!

### What is the "Loss Function"?

- Measures how wrong the model's predictions are
- Cross-entropy loss: compares predicted tokens vs actual answer tokens
- Lower loss = better predictions
- Training adjusts model weights to minimize loss

## 📈 Example Training Flow

**Before fine-tuning**:
```
Question: "What's your outlook on tech stocks?"
Databricks GPT-OSS-120B: "Technology companies are important to the economy..." [generic]
```

**After fine-tuning**:
```
Question: "What's your outlook on tech stocks?"
Fine-tuned Model: "Technology sector shows strong momentum entering 2026. Key drivers include AI infrastructure buildout with estimated $150B in capex from major cloud providers... recommend 25% portfolio allocation to AI infrastructure plays with strong FCF generation." [expert hedge fund analyst response]
```

## 🎓 What Makes This "Supervised"?

1. **We provide labels**: Every question has a correct answer in our dataset
2. **Model learns from examples**: Sees question → answer pairs repeatedly
3. **Supervised signal**: The loss function tells the model "your answer should look like THIS"

Compare to:
- **Unsupervised learning**: No labels, model finds patterns on its own
- **Reinforcement learning**: Model learns from rewards/penalties

## ✅ Success Criteria

After training, your model should:
- Use hedge fund terminology correctly (Sharpe ratio, VaR, etc.)
- Provide structured answers with metrics and recommendations
- Stay on topic for financial questions
- Generate coherent, professional responses

## 🔧 Troubleshooting

**Error: CUDA out of memory**
- Use gradient checkpointing (already enabled)
- Reduce batch size to 1 (already set)
- Increase gradient accumulation steps
- Use more GPUs or larger GPU instances

**Error: File not found**
- Make sure `training_data.csv` is uploaded to `/dbfs/FileStore/`

**Model gives generic answers**
- Add more training examples (50-100+)
- Train for more epochs (5-10)
- Check that training loss is decreasing

**Training too slow**
- Use more powerful GPU instances (A100 recommended)
- Use multi-GPU setup
- Consider using LoRA for faster training

## 📚 Files in This Demo

1. **`training_data.csv`** - 20 labeled Q&A pairs (YOUR DATA)
2. **`Simple_Supervised_Finetuning.ipynb`** - Complete training notebook
3. **`README.md`** - Detailed documentation
4. **`QUICKSTART.md`** - This file!
5. **`upload_to_dbfs.py`** - Helper to upload CSV

## 🎯 Next Steps

1. **More data**: Add 50-100 more Q&A pairs from real analyst responses
2. **Validation set**: Split data 80/20 for training/validation
3. **Bigger model**: Try GPT-2 Medium (355M params) or Large (774M params)
4. **Deploy**: Create Model Serving endpoint for real-time queries
5. **RAG**: Combine with retrieval of real-time market data

---

**Questions?** Check the notebook - it has detailed comments explaining each step!
