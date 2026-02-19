# 🪑 Furniture Product Extractor

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/vaveyko/Furniture-Shop-Parser)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end Machine Learning solution designed to extract product names from unstructured furniture store websites. This project moves from raw web scraping to a cloud-deployed AI application.

## 🚀 Live Demo
**[Check out the live app on Hugging Face Spaces](https://huggingface.co/spaces/vaveyko/Furniture-Shop-Parser)**

## 💡 Key Features
- **Multi-URL Parsing:** Supports bulk processing of furniture store links.
- **Transformer-based AI:** Uses a fine-tuned **TinyBERT** model for fast and accurate text classification.
- **Interactive UI:** A Streamlit-based dashboard with real-time confidence thresholding and data visualization.

## 🛠️ Technical Stack
- **NLP:** Transformers (Hugging Face), PyTorch
- **Web Scraping:** BeautifulSoup4, Requests
- **UI/Deployment:** Streamlit, Hugging Face Spaces
- **Data:** Pandas, Matplotlib (for visualization)

## 🧠 How It Works

### 1. Preprocessing (The Scraper)
The solution extracts raw HTML and cleans it by removing non-semantic tags (`<header>`, `<footer>`, `<script>`, etc.). It uses a context-aware separator to prevent "word clumping," ensuring that product names remain distinct from prices and UI labels.

### 2. The Model (TinyBERT + Linear Head)
Since web data is highly imbalanced (mostly noise, few products), I implemented:
- **Custom Architecture:** A BERT-Tiny backbone with two Linear layers, ReLU activation, and two Dropout layers.
- **Weighted Loss:** Applied **Inverse Class Frequency** weights to the loss function to penalize errors on furniture items more heavily.
- **Inference Optimization:** The model is optimized for CPU usage to ensure cost-effective deployment.

### 3. Thresholding & UX
The app uses a **Confidence Threshold** slider. This allows users to prioritize **Precision** (cleaner results) or **Recall** (more results) dynamically using `st.session_state`.

## 📊 Evaluation Results
The model was evaluated on a held-out test set from various furniture retailers:

| Metric | Score |
| :--- | :--- |
| **Precision** | **84.0%** |
| **Recall** | **80.77%** |
| **F1-Score** | **0.82** |
| **Accuracy** | **90.3%** |

*Note: Precision was prioritized to ensure the UI remains free of "garbage" text.*
