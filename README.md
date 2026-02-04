# Simple Supervised Fine-Tuning for Hedge Fund Q&A - Databricks Demo

This demo shows **simple supervised fine-tuning** of an open-source GPT model for answering hedge fund investment questions.

## 🎯 Problem Definition

**Business Problem**: Hedge fund analysts spend significant time answering repetitive questions about portfolio analysis, risk assessment, and investment strategies. We want to automate responses to common queries.

**ML Problem**: Given a hedge fund investment question (input), predict the expert analyst response (output).

**Approach**: Supervised fine-tuning on labeled question-answer pairs.

## 📊 Dataset

**Synthetic Labeled Data**: 20 hedge fund Q&A pairs

Each example contains:
- **Input (Question)**: A specific hedge fund query (e.g., "What's your outlook on tech stocks?")
- **Output (Answer)**: Expert analyst response with financial metrics, recommendations, and analysis

**Labels**: The "answer" field is the supervised label we're training the model to predict given the question.

## 🏗️ Architecture

- **Base Model**: Databricks GPT-OSS-120B (120 billion parameters)
- **Fine-tuning Method**: Simple supervised fine-tuning (standard cross-entropy loss)
- **Training Data**: Question → Answer pairs
- **Optimizations**: FP16 mixed precision, gradient accumulation, gradient checkpointing
- **Catalog/Schema**: `users.yasamin_tari`

## 📁 Files

1. **`Simple_Supervised_Finetuning.ipynb`** - Databricks notebook with complete workflow
2. **`training_data.csv`** - Labeled dataset (question, answer pairs)

## 🚀 Quick Start

1. Upload `training_data.csv` to DBFS: `/dbfs/FileStore/training_data.csv`
2. Upload `Simple_Supervised_Finetuning.ipynb` to Databricks workspace
3. Create a **GPU cluster** (required for 120B model):
   - Runtime: 14.3 LTS ML or later
   - Node: GPU instance (e.g., g5.12xlarge or A100)
   - Enable Unity Catalog
4. Run all cells in the notebook
5. Query your fine-tuned model!

**Training time**: Depends on GPU, approximately 30-60 minutes on multi-GPU setup

**Note**: The databricks-gpt-oss-120b is a large model requiring significant GPU resources.

## 📊 Example Training Data

| Question | Answer (Label) |
|----------|----------------|
| "What's your outlook on tech stocks for 2026?" | "Technology sector shows strong momentum... AI infrastructure buildout... recommend 25% allocation..." |
| "How do I calculate portfolio Sharpe ratio?" | "Sharpe ratio = (Portfolio Return - Risk Free Rate) / Portfolio Std Dev. For example..." |
| "Should I hedge my European exposure?" | "Yes, recommend EUR puts covering 40% of exposure... expected cost 1.2%..." |

**All 20 examples saved in**: `training_data.csv`

## 🔧 What the Notebook Does

1. **Loads labeled data** from CSV (question, answer columns)
2. **Loads Databricks GPT-OSS-120B** (powerful open-source GPT model)
3. **Fine-tunes** using standard supervised learning with optimizations:
   - FP16 mixed precision for memory efficiency
   - Gradient accumulation for larger effective batch size
   - Gradient checkpointing to save memory
   - Automatic device mapping across GPUs
4. **Evaluates** on test questions
5. **Saves model** to Databricks
6. **Registers** in Unity Catalog (`users.yasamin_tari.finetuned_models`)

## 📈 Expected Results

- **Training Time**: 30-60 minutes on multi-GPU setup
- **Model Size**: ~240GB (120B parameters in FP16)
- **Quality**: High-quality responses with expert-level hedge fund knowledge
- **Hardware**: Requires GPU cluster (minimum 4x A100 or equivalent)

## 🔄 Simple Workflow

```
Labeled Data (CSV with 20 Q&A pairs)
    ↓
Load Databricks GPT-OSS-120B (pre-trained)
    ↓
Fine-tune with supervised learning
  - Cross-entropy loss
  - FP16 mixed precision
  - Gradient accumulation
    ↓
Evaluate on test questions
    ↓
Save to Unity Catalog
    ↓
Deploy for inference
```

## 🎯 Key Concepts

### Supervised Fine-Tuning
- We have **labeled data**: questions (inputs) and answers (labels)
- Model learns to **predict the answer** given a question
- Uses **standard cross-entropy loss** (same as training from scratch, but starting from pre-trained weights)

### Why This Works
- Base Databricks GPT-OSS-120B already has strong language understanding and reasoning
- Fine-tuning adapts it to specialized hedge fund domain
- Model learns specific terminology, metrics, and response patterns
- Large model size (120B params) provides strong baseline knowledge

### Efficiency Optimizations
- **FP16**: Train in 16-bit precision instead of 32-bit (2x memory savings)
- **Gradient Accumulation**: Simulate larger batch sizes without OOM errors
- **Gradient Checkpointing**: Trade compute for memory by recomputing activations
- **Device Mapping**: Automatically distribute model across multiple GPUs

## 🚀 Extending This Demo

1. **Add more training data** (100-1000+ examples for better performance)
2. **Implement LoRA** for parameter-efficient fine-tuning (train <1% of parameters)
3. **Add validation set** for hyperparameter tuning and early stopping
4. **Deploy as Model Serving endpoint** with vLLM or TGI for fast inference
5. **Quantization**: Use 8-bit or 4-bit quantization for more efficient serving

## 📝 What is Supervised Fine-Tuning?

Supervised fine-tuning means:
1. You have **labeled data** where each input has a correct output
2. The model learns to **predict the label** (output) given the input
3. Uses **cross-entropy loss** to measure prediction errors
4. **Optimizer updates weights** to minimize the loss

In our case:
- **Input**: Hedge fund question
- **Label**: Expert answer
- **Model learns**: To generate answers similar to the expert

---

**Created by**: Yasamin Tari  
**Last Updated**: February 2026  
**Databricks Catalog**: `users.yasamin_tari`
