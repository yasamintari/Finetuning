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
2. **`training_data.csv`** - Source data (20 labeled Q&A pairs)
3. **`load_csv_to_delta.py`** - Helper script to load CSV into Delta table

## 🗄️ Data Architecture

### Delta Tables (Unity Catalog)
- **Training Data**: `users.yasamin_tari.hedge_fund_training_data`
- **Model Registry**: `users.yasamin_tari.finetuned_models`

### Volumes (Unity Catalog)
- **Model Storage**: `/Volumes/users/yasamin_tari/models/`

**No DBFS usage** - everything uses Unity Catalog!

## 🚀 Quick Start

### Prerequisites
1. Unity Catalog enabled in Databricks workspace
2. Access to `users.yasamin_tari` catalog and schema
3. GPU cluster (g5.12xlarge or A100)

### Setup Steps

1. **Create the schema** (if not exists):
   ```sql
   CREATE SCHEMA IF NOT EXISTS users.yasamin_tari;
   ```

2. **Load training data into Delta table**:
   ```python
   # Option A: Use the provided script
   # Run load_csv_to_delta.py in a notebook
   
   # Option B: Load directly
   import pandas as pd
   df = pd.read_csv("training_data.csv")
   spark.createDataFrame(df).write.format("delta").mode("overwrite") \
       .saveAsTable("users.yasamin_tari.hedge_fund_training_data")
   ```

3. **Create volume for models**:
   ```sql
   CREATE VOLUME IF NOT EXISTS users.yasamin_tari.models;
   ```

4. **Import and run the notebook**:
   - Upload `Simple_Supervised_Finetuning.ipynb`
   - Attach to GPU cluster
   - Run all cells

**Training time**: 30-60 minutes on multi-GPU setup

**Note**: All data stored in Unity Catalog (Delta tables + Volumes), no DBFS!

## 📊 Example Training Data

| Question | Answer (Label) |
|----------|----------------|
| "What's your outlook on tech stocks for 2026?" | "Technology sector shows strong momentum... AI infrastructure buildout... recommend 25% allocation..." |
| "How do I calculate portfolio Sharpe ratio?" | "Sharpe ratio = (Portfolio Return - Risk Free Rate) / Portfolio Std Dev. For example..." |
| "Should I hedge my European exposure?" | "Yes, recommend EUR puts covering 40% of exposure... expected cost 1.2%..." |

**All 20 examples saved in**: `training_data.csv`

## 🔧 What the Notebook Does

1. **Creates Unity Catalog volume** for model storage
2. **Loads labeled data** from Delta table (`users.yasamin_tari.hedge_fund_training_data`)
3. **Loads Databricks GPT-OSS-120B** (powerful open-source GPT model)
4. **Fine-tunes** using standard supervised learning with optimizations:
   - FP16 mixed precision for memory efficiency
   - Gradient accumulation for larger effective batch size
   - Gradient checkpointing to save memory
   - Automatic device mapping across GPUs
5. **Evaluates** on test questions
6. **Saves model** to Unity Catalog Volume (`/Volumes/users/yasamin_tari/models/`)
7. **Registers metadata** in Delta table (`users.yasamin_tari.finetuned_models`)

## 📈 Expected Results

- **Training Time**: 30-60 minutes on multi-GPU setup
- **Model Size**: ~240GB (120B parameters in FP16)
- **Quality**: High-quality responses with expert-level hedge fund knowledge
- **Hardware**: Requires GPU cluster (minimum 4x A100 or equivalent)

## 🔄 Simple Workflow

```
CSV (training_data.csv)
    ↓
Load into Delta Table (users.yasamin_tari.hedge_fund_training_data)
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
Save to Unity Catalog Volume (/Volumes/users/yasamin_tari/models/)
    ↓
Register metadata in Delta table (users.yasamin_tari.finetuned_models)
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
