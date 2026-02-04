# Unity Catalog Architecture - No DBFS!

## 🗄️ Data Storage Strategy

All data stored in **Unity Catalog** using Delta tables and Volumes (no DBFS files!).

---

## 📊 Delta Tables

### 1. Training Data Table
```
users.yasamin_tari.hedge_fund_training_data
```

**Schema**:
```
question STRING  - The input question (X)
answer STRING    - The expert answer label (Y)
```

**Sample**:
```sql
SELECT * FROM users.yasamin_tari.hedge_fund_training_data LIMIT 3;
```

| question | answer |
|----------|--------|
| "What's your outlook on tech?" | "Technology sector shows momentum..." |
| "How do I calculate Sharpe ratio?" | "Sharpe = (Return - RF) / StdDev..." |

**Create**:
```python
# From CSV
df = pd.read_csv("training_data.csv")
spark.createDataFrame(df).write.format("delta").mode("overwrite") \
    .saveAsTable("users.yasamin_tari.hedge_fund_training_data")
```

---

### 2. Model Registry Table
```
users.yasamin_tari.finetuned_models
```

**Schema**:
```
model_name STRING
base_model STRING
training_date TIMESTAMP
num_examples INT
model_path STRING
mlflow_run_id STRING
use_case STRING
notes STRING
```

**Purpose**: Track all fine-tuned models, their metadata, and locations

**Create**:
```sql
CREATE TABLE IF NOT EXISTS users.yasamin_tari.finetuned_models (
    model_name STRING,
    base_model STRING,
    training_date TIMESTAMP,
    num_examples INT,
    model_path STRING,
    mlflow_run_id STRING,
    use_case STRING,
    notes STRING
)
```

---

## 📁 Unity Catalog Volumes

### Model Storage Volume
```
/Volumes/users/yasamin_tari/models/
```

**Purpose**: Store fine-tuned model artifacts (weights, tokenizer, config)

**Structure**:
```
/Volumes/users/yasamin_tari/models/
  └── hedge_fund_qa_model_20260203_1430/
      ├── pytorch_model.bin
      ├── config.json
      ├── tokenizer.json
      ├── tokenizer_config.json
      └── special_tokens_map.json
```

**Create**:
```sql
CREATE VOLUME IF NOT EXISTS users.yasamin_tari.models;
```

**Access in Python**:
```python
model_path = "/Volumes/users/yasamin_tari/models/hedge_fund_qa_model_20260203_1430"

# Load model
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
```

---

## 🔄 Complete Data Flow

```
1. CSV File (training_data.csv)
   ↓
2. Load into Delta Table
   users.yasamin_tari.hedge_fund_training_data
   ↓
3. Read for Training
   df = spark.table("users.yasamin_tari.hedge_fund_training_data").toPandas()
   ↓
4. Fine-tune Model
   ↓
5. Save to Volume
   /Volumes/users/yasamin_tari/models/hedge_fund_qa_model_TIMESTAMP/
   ↓
6. Register Metadata in Delta Table
   users.yasamin_tari.finetuned_models
```

---

## ✅ Benefits of Unity Catalog Approach

### vs DBFS:
- ✅ **Governed**: Full Unity Catalog governance and access control
- ✅ **Versioned**: Delta tables have version history and time travel
- ✅ **Discoverable**: Appears in Catalog Explorer, easy to find
- ✅ **Shareable**: Grant permissions via SQL, no file path management
- ✅ **Auditable**: Complete lineage tracking
- ✅ **Professional**: Production-grade data management

### vs File Storage:
- ✅ **Structured**: Delta tables provide schema enforcement
- ✅ **Queryable**: Use SQL to explore and analyze training data
- ✅ **ACID**: Atomic operations, no corruption from concurrent writes
- ✅ **Scalable**: Handles large datasets efficiently

---

## 🔐 Access Control

### Grant Access to Training Data
```sql
GRANT SELECT ON TABLE users.yasamin_tari.hedge_fund_training_data 
TO `analyst_group`;
```

### Grant Access to Models Volume
```sql
GRANT READ_VOLUME ON VOLUME users.yasamin_tari.models 
TO `ml_engineers`;
```

### Grant Access to Model Registry
```sql
GRANT SELECT ON TABLE users.yasamin_tari.finetuned_models 
TO `data_scientists`;
```

---

## 📊 Query Examples

### View All Training Data
```sql
SELECT * FROM users.yasamin_tari.hedge_fund_training_data;
```

### Count Training Examples
```sql
SELECT COUNT(*) as num_examples 
FROM users.yasamin_tari.hedge_fund_training_data;
```

### View All Fine-tuned Models
```sql
SELECT 
    model_name,
    base_model,
    training_date,
    num_examples,
    model_path
FROM users.yasamin_tari.finetuned_models
ORDER BY training_date DESC;
```

### Find Latest Model
```sql
SELECT * 
FROM users.yasamin_tari.finetuned_models
ORDER BY training_date DESC
LIMIT 1;
```

### Training Data Statistics
```sql
SELECT 
    COUNT(*) as total_questions,
    AVG(LENGTH(question)) as avg_question_length,
    AVG(LENGTH(answer)) as avg_answer_length
FROM users.yasamin_tari.hedge_fund_training_data;
```

---

## 🚀 Production Deployment

### Load Model from Volume
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

# Get latest model path from registry
model_info = spark.sql("""
    SELECT model_path 
    FROM users.yasamin_tari.finetuned_models 
    ORDER BY training_date DESC 
    LIMIT 1
""").collect()[0]

model_path = model_info['model_path']

# Load for inference
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_path)
```

### Register for Model Serving
```python
import mlflow

# Log model to MLflow
with mlflow.start_run():
    mlflow.transformers.log_model(
        transformers_model={"model": model, "tokenizer": tokenizer},
        artifact_path="model",
        registered_model_name="users.yasamin_tari.hedge_fund_qa_gpt"
    )
```

---

## 📝 Summary

| Component | Location | Purpose |
|-----------|----------|---------|
| Training Data | `users.yasamin_tari.hedge_fund_training_data` (Delta) | Labeled Q&A pairs |
| Model Artifacts | `/Volumes/users/yasamin_tari/models/` (Volume) | Fine-tuned weights |
| Model Registry | `users.yasamin_tari.finetuned_models` (Delta) | Model metadata |

**Key Point**: Everything uses Unity Catalog - no DBFS, complete governance!
