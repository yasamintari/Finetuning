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

- **Base Model**: GPT-2 (124M parameters - small and fast for demo)
- **Fine-tuning Method**: Simple supervised fine-tuning (standard cross-entropy loss)
- **Training Data**: Question → Answer pairs
- **Catalog/Schema**: `users.yasamin_tari`

## 📁 Files

1. **`Simple_Supervised_Finetuning.ipynb`** - Databricks notebook with complete workflow
2. **`training_data.csv`** - Labeled dataset (question, answer pairs)

## 🚀 Quick Start

1. Upload `Simple_Supervised_Finetuning.ipynb` to Databricks workspace
2. Create a cluster (CPU is fine, GPU optional for faster training)
3. Run all cells in the notebook
4. Query your fine-tuned model!

**Training time**: ~5-10 minutes on CPU

## 📊 Example Training Data

| Question | Answer (Label) |
|----------|----------------|
| "What's your outlook on tech stocks for 2026?" | "Technology sector shows strong momentum... AI infrastructure buildout... recommend 25% allocation..." |
| "How do I calculate portfolio Sharpe ratio?" | "Sharpe ratio = (Portfolio Return - Risk Free Rate) / Portfolio Std Dev. For example..." |
| "Should I hedge my European exposure?" | "Yes, recommend EUR puts covering 40% of exposure... expected cost 1.2%..." |

**All 20 examples saved in**: `training_data.csv`

## 🔧 What the Notebook Does

1. **Loads labeled data** from CSV (question, answer columns)
2. **Loads GPT-2 model** (small, fast, open-source)
3. **Fine-tunes** using standard supervised learning
4. **Evaluates** on test questions
5. **Saves model** to Databricks
6. **Registers** in Unity Catalog (`users.yasamin_tari.hedge_fund_qa_model`)

## 📈 Expected Results

- **Training Time**: 5-10 minutes on CPU
- **Model Size**: ~500MB
- **Quality**: Model learns hedge fund terminology and response patterns

## 🔄 Simple Workflow

```
Labeled Data (CSV)
    ↓
Load GPT-2 Model
    ↓
Fine-tune (supervised learning)
    ↓
Evaluate on test questions
    ↓
Save to Unity Catalog
    ↓
Use for inference
```

## 🎯 Key Concepts

### Supervised Fine-Tuning
- We have **labeled data**: questions (inputs) and answers (labels)
- Model learns to **predict the answer** given a question
- Uses **standard cross-entropy loss** (same as training from scratch, but starting from pre-trained weights)

### Why This Works
- Base GPT-2 knows general language
- Fine-tuning adapts it to hedge fund domain
- Model learns specific terminology, metrics, and response patterns

## 🚀 Extending This Demo

1. **Add more training data** (100+ examples)
2. **Use larger model** (GPT-2 Medium/Large)
3. **Add validation set** for hyperparameter tuning
4. **Deploy as Model Serving endpoint**

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
