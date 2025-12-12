import pandas as pd
import plotly.express as px
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from .jira_fetcher import JiraFetcher
from ..consts import *


class JiraAnalyzer:
    """
    A modular class to fetch Jira issues, classify them by server and technology,
    and visualize the results.
    """

    def __init__(self):
        """Initializes the analyzer with constants and trains the ML model."""
        self.dataframe: pd.DataFrame = pd.DataFrame()
        self.classifier_model = self._train_classifier()
        self.fetcher = JiraFetcher()

    @staticmethod
    def _train_classifier() -> Pipeline:
        """Trains the Machine Learning model using the technology templates."""
        training_data = []
        training_labels = []

        # Generate synthetic training examples
        for category, templates in TECHNOLOGY_TEMPLATES.items():
            for _ in range(100):
                template = random.choice(templates)
                # Use dummy data to ensure the model focuses on the core text patterns
                text = template.format(server="srv-dummy", server2="srv-dummy2", db_name="DB_DUMMY")
                training_data.append(text)
                training_labels.append(category)

        # Build a standard classification pipeline
        text_clf = Pipeline([
            ('vect', CountVectorizer(stop_words='english')),
            ('clf', MultinomialNB()),
        ])

        text_clf.fit(training_data, training_labels)
        return text_clf

    def _extract_servers(self) -> None:
        """Extracts server names using Regex and handles missing/invalid servers."""
        df = self.dataframe

        # Apply Regex for extraction
        df['server'] = df['description'].str.extract(SERVER_REGEX, expand=False)

        # Normalize and handle missing/invalid gracefully
        df['server'] = df['server'].str.lower().fillna('unidentified')
        print("✅ Server extraction complete.")

    def _classify_technology(self) -> None:
        """Applies the trained ML model to classify the technology."""
        self.dataframe['technology'] = self.classifier_model.predict(self.dataframe['description'])
        print("✅ Technology classification complete.")

    def _generate_plots(self) -> None:
        """Generates and displays the required visualizations using Plotly."""
        df = self.dataframe

        # --- PLOT 1: Top Problematic Servers ---
        server_counts = df[df['server'] != 'unidentified']['server'].value_counts().head(20).reset_index()
        server_counts.columns = ['Server', 'Ticket Count']  # Rename columns for clarity

        fig_server = px.bar(server_counts, x='Server', y='Ticket Count',
                            title='Top 20 Servers by Ticket Volume (Excluding Unidentified)', template="plotly_white")

        # --- PLOT 2: Tickets by Technology Category ---
        tech_counts = df['technology'].value_counts().reset_index()
        tech_counts.columns = ['Technology', 'Ticket Count']

        fig_tech = px.bar(tech_counts, x='Technology', y='Ticket Count', title='Ticket Distribution by Technology',
                          template="plotly_white")

        print("\n📊 Displaying Interactive Plotly Visualizations...")
        fig_server.show()
        fig_tech.show()

    def run_analysis(self) -> None:
        """The main method to run the entire analysis pipeline in sequence."""
        print(f"{'-' * 40}\nJIRA ANALYSIS PIPELINE STARTING\n{'-' * 40}")

        self.dataframe = self.fetcher.fetch_data()
        if self.dataframe.empty:
            print("🛑 Pipeline terminated due to data fetching error.")
            return

        self._extract_servers()
        self._classify_technology()

        self._generate_plots()
