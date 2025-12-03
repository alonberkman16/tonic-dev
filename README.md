# Jira Ticket Operations & Analytics Pipeline

## 📋 Overview

This project is a comprehensive Data Engineering solution designed to interact with the Atlassian Jira Cloud API. It consists of two main modules:

1.  **Simulation & Load Testing (Phase 1):** A high-performance script to populate a Jira project with 20,000+ synthetic support tickets, simulating real-world server incidents.
2.  **Extraction & Intelligent Analysis (Phase 2):** An analytical pipeline that extracts data using robust pagination, parses unstructured text using Regular Expressions, and classifies technical issues using Machine Learning (NLP).

## 🚀 Key Features

* **Bulk Data Generation:** Utilizes Jira's Bulk API to generate thousands of issues efficiently while respecting rate limits.
* **Robust Data Extraction:** Implements **Token-Based Pagination** (Cursor-based) to reliably fetch large datasets (20k+ records) from the modern Jira Cloud API.
* **Hybrid Analysis Engine:**
    * **Regex Pattern Matching:** Identifies server names (e.g., `srv-01`, `SRV-db`) handling mixed casing and missing separators.
    * **Machine Learning Classifier:** Uses **Scikit-Learn (Naive Bayes)** to classify tickets into technologies (Database, Network, Storage, etc.) without relying on brittle keyword lists.
* **Interactive Visualization:** Generates dynamic, interactive charts using **Plotly** to visualize server health and ticket distribution.
* **Secure Configuration:** Uses environment variables to manage API credentials securely.

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **Data Manipulation:** Pandas
* **Machine Learning:** Scikit-learn (MultinomialNB, CountVectorizer)
* **Visualization:** Plotly Express
* **API Interaction:** Requests (REST)
* **Security:** Python-dotenv

***

## ⚙️ Setup & Installation

### 1. Prerequisites
Ensure you have a working Python interpreter (such as the Anaconda environment) installed on your system.

### 2. Install Dependencies
Install all required Python packages using the provided `requirements.txt` file:

###3. Environment Configuration
For security, credentials must be stored outside of the source code.

Create a file named .env in the root directory of the project.
Paste the following content into the file and replace the placeholders with your actual credentials:
 JIRA_DOMAIN=your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your_generated_api_token
PROJECT_KEY=your_project_key
Important: Ensure .env is added to your .gitignore file to prevent exposing your secrets on GitHub.
🏃 Usage
Phase 1: Generating Data
If you need to populate a test project with synthetic data:

Run populate_jira.py.
Ensure PROJECT_KEY matches your target project.

Note: This script uses the Bulk Issue Create API to minimize network overhead.
Phase 2: Analyzing Data
To extract, classify, and visualize the data run analyze_data.py
What happens next?

Training: The system trains a Naive Bayes classifier on internal templates.
Fetching: It pulls all issues from Jira using token-based pagination.
Processing:
Extracts server names using Regex (?i)\b(srv-?[\w\d]+)\b.
Classifies the "Description" text into technology categories.
Visualization: Opens two interactive Plotly charts in your default browser.
🧠 Technical Highlights
1. Token-Based Pagination
The Jira API (/rest/api/3/search/jql) limits responses to small batches. This project uses nextPageToken to sequentially fetch pages, ensuring 100% data retrieval accuracy even for large datasets.

2. "No-Keyword" Classification
The solution uses a Bag-of-Words model with a Multinomial Naive Bayes classifier to learn the structure and vocabulary of different issue types statistically, providing robust categorization.

3. Flexible Regex
The pattern r'(?i)\b(srv-?[\w\d]+)\b' handles various server name formats by supporting case insensitivity ((?i)) and optional hyphens (-?).

👤 Author
Alon Berkman

Backend Developer & Data Engineer
Email