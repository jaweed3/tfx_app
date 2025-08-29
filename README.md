# Phishing Site Detection with a TFX Pipeline

This project is an implementation and experiment in building an end-to-end machine learning pipeline using **TensorFlow Extended (TFX)**. The goal is to automate the workflow, from data ingestion to model training and validation, to classify a website as either legitimate or a phishing site.

This project is heavily inspired by the book *"Building Machine Learning Pipelines"* by Hannes Hapke & Catherine Nelson, which is a fantastic resource for MLOps practices.

---

## 📊 Dataset

The dataset used is the **Phishing Websites Data Set** from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/).  
It consists of **30 features** extracted from URLs and page sources to identify phishing activities.

### Feature Examples
- **having_IP_Address**: Whether the URL uses an IP address (`-1: no`, `1: yes`)
- **URL_Length**: The length of the URL (`1: long`, `0: medium`, `-1: short`)
- **Shortining_Service**: Whether the URL uses a shortening service (`1: yes`, `-1: no`)
- **SSLfinal_State**: The legitimacy of the SSL certificate (`-1: untrusted`, `0: doubtful`, `1: trusted`)
- **age_of_domain**: The age of the domain (`1: > 1 year`, `-1: <= 1 year`)
- **web_traffic**: The website's traffic rank (`1: low`, `0: medium`, `-1: high`)

### Target Label
- **Result**: The class of the website
  - `-1`: Phishing  
  - `1`: Legitimate

---

## 🚀 TFX Pipeline Architecture

As an ML Engineer, the primary focus is on building reliable, reproducible, and scalable systems. **TFX** provides the perfect framework for this purpose.  
This pipeline orchestrates the entire ML workflow.

### Main Components
- **CsvExampleGen**: Imports raw data from the `.csv` file into TFRecord format, optimized for TensorFlow.
- **StatisticsGen**: Calculates descriptive statistics for each feature to understand the data distribution.
- **SchemaGen**: Creates a data schema based on statistics (types, boundaries, properties).
- **ExampleValidator**: Detects anomalies like missing values or data drift by validating against the schema.
- **Transform**: Performs feature engineering consistently for training and inference.
- **Trainer**: Trains a classification model using TensorFlow and Keras.
- **Evaluator**: Analyzes model performance and compares with previously deployed models.
- **Pusher**: Deploys the validated model if performance meets thresholds.

---

## 🛠️ How to Get Started

### Prerequisites
- Python 3.8+
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/USERNAME/REPOSITORY.git
cd REPOSITORY

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
````

Make sure your `requirements.txt` includes:

```
tfx
tensorflow
```

---

## ▶️ Running the Pipeline

To run the ML pipeline, execute the main script:

```bash
python run_pipeline.py
```

This script initializes and runs each TFX component in sequence.
Artifacts (outputs) such as data statistics, schema, saved model, and evaluation results are stored in the **`tfx_pipeline_output`** directory.

---

## 📂 Project Structure

A well-organized structure is key for maintainability:

```
.
├── data/
│   └── phishing_website_dataset.csv  # Raw dataset
├── pipeline/
│   ├── __init__.py
│   └── pipeline.py                   # Pipeline workflow and component definitions
├── models/
│   └── model.py                      # Model creation logic (Keras architecture)
├── run_pipeline.py                   # Main script to run the pipeline
├── requirements.txt                  # Python dependencies
└── README.md
```

---

## 🙏 Acknowledgements

* Hannes Hapke & Catherine Nelson for *"Building Machine Learning Pipelines"*
* The UCI Machine Learning Repository for the dataset used in this project

