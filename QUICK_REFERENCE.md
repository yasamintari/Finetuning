# Quick Reference Card

## 🎯 Unity Catalog Setup (3 Steps)

### 1. Create Schema
```sql
CREATE SCHEMA IF NOT EXISTS users.yasamin_tari;
```

### 2. Load Training Data
```python
import pandas as pd
df = pd.read_csv("training_data.csv")
spark.createDataFrame(df).write.format("delta").mode("overwrite") \
    .saveAsTable("users.yasamin_tari.hedge_fund_training_data")
```

### 3. Create Volume
```sql
CREATE VOLUME IF NOT EXISTS users.yasamin_tari.models;
```

---

## 📊 Unity Catalog Structure

```
users.yasamin_tari (catalog.schema)
├── Tables (Delta)
│   ├── hedge_fund_training_data     ← Training Q&A pairs
│   └── finetuned_models              ← Model registry
└── Volumes
    └── models/                       ← Model artifacts storage
        └── hedge_fund_qa_model_TIMESTAMP/
            ├── pytorch_model.bin
            ├── config.json
            └── tokenizer files
```

---

## 🔍 Common Queries

### View Training Data
```sql
SELECT * FROM users.yasamin_tari.hedge_fund_training_data;
```

### Count Examples
```sql
SELECT COUNT(*) FROM users.yasamin_tari.hedge_fund_training_data;
```

### View All Models
```sql
SELECT * FROM users.yasamin_tari.finetuned_models 
ORDER BY training_date DESC;
```

### Get Latest Model Path
```sql
SELECT model_path FROM users.yasamin_tari.finetuned_models 
ORDER BY training_date DESC LIMIT 1;
```

---

## 💻 Load Model for Inference

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Get model path from registry
model_path = spark.sql("""
    SELECT model_path 
    FROM users.yasamin_tari.finetuned_models 
    ORDER BY training_date DESC LIMIT 1
""").collect()[0]['model_path']

# Load model
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_path)

# Inference
question = "What's your view on AI infrastructure investments?"
prompt = f"Question: {question}\n\nAnswer:"
inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=200)
answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
```

---

## 🔐 Access Control

### Grant Read Access to Training Data
```sql
GRANT SELECT ON TABLE users.yasamin_tari.hedge_fund_training_data 
TO `analyst@company.com`;
```

### Grant Access to Models Volume
```sql
GRANT READ_VOLUME ON VOLUME users.yasamin_tari.models 
TO `ml_engineers`;
```

---

## 📝 Key Locations

| Resource | Location |
|----------|----------|
| **Training Data** | `users.yasamin_tari.hedge_fund_training_data` |
| **Model Registry** | `users.yasamin_tari.finetuned_models` |
| **Model Storage** | `/Volumes/users/yasamin_tari/models/` |
| **Notebook** | Workspace: `Simple_Supervised_Finetuning.ipynb` |

---

## ✅ Benefits vs DBFS

| Feature | Unity Catalog | DBFS |
|---------|---------------|------|
| Governance | ✅ Full | ❌ Limited |
| Versioning | ✅ Delta history | ❌ No |
| Discoverable | ✅ Catalog Explorer | ❌ Manual paths |
| Access Control | ✅ SQL grants | ❌ File permissions |
| Queryable | ✅ SQL | ❌ File reads only |
| Lineage | ✅ Complete | ❌ No |
| ACID | ✅ Yes | ❌ No |

---

## 🚀 Production Checklist

- [ ] Schema created (`users.yasamin_tari`)
- [ ] Training data loaded to Delta table
- [ ] Volume created for models
- [ ] GPU cluster configured (A100 or g5.12xlarge)
- [ ] Notebook imported
- [ ] Training completed
- [ ] Model registered in metadata table
- [ ] Access controls configured
- [ ] Model tested with inference
- [ ] Monitoring setup (MLflow)

---

**Keep this card handy while working with the demo!**
