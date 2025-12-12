import pandas as pd
import plotly.express as px
import random
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import json

from .consts import *
from .utils import get_jira_api_auth, run_request_with_error_handling


class JiraAnalyzer:
    """
    A modular class to fetch Jira issues, classify them by server and technology,
    and visualize the results.
    """

    def __init__(self):
        """Initializes the analyzer with constants and trains the ML model."""
        self.dataframe: pd.DataFrame = pd.DataFrame()
        self.classifier_model = self._train_classifier()

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

    @staticmethod
    def _save_checkpoint(issues: list, next_token: str or None) -> None:
        """Saves the current issues list and the next token to the cache file."""
        checkpoint_data = {
            "issues": issues,
            "nextPageToken": next_token
        }
        with open(CACHE_FILE_PATH, "w") as f:
            json.dump(checkpoint_data, f)

    @staticmethod
    def _load_checkpoint() -> tuple[list, str or None]:
        """Loads partial issues and the next token from the cache file, if it exists."""
        if os.path.exists(CACHE_FILE_PATH):
            with open(CACHE_FILE_PATH, "r") as f:
                data = json.load(f)

            # Check if the loaded data is in the expected format (list of dicts)
            issues_loaded = data.get("issues")
            if issues_loaded and isinstance(issues_loaded, list):
                return issues_loaded, data.get("nextPageToken")
        else:
            return [], None

    def _fetch_data(self) -> bool:
        """Pulls all issue descriptions from the Jira project using JQL and pagination."""
        # Set up login and query variables
        url = f"https://{JIRA_DOMAIN}/rest/api/3/search/jql"
        auth = get_jira_api_auth(EMAIL, API_TOKEN)
        params = {
            "jql": f"project = {PROJECT_KEY} ORDER BY created ASC",
            "maxResults": FETCHER_BATCH_SIZE,
            "fields": ["description"]
        }

        issues, next_page_token = self._load_checkpoint()
        is_last = False

        if issues:
            print(f"Resumed fetch with {len(issues)} issues already retrieved.")
        else:
            print(f"🔄 Starting new fetch for project: {PROJECT_KEY}...")
        while not is_last:
            if next_page_token:
                params["nextPageToken"] = next_page_token

            data = run_request_with_error_handling(method='GET', url=url, headers=JIRA_API_HEADERS, params=params, auth=auth)
            if not data.get("issues"):  # If there is a problem with the data the API has returned
                break

            for issue in data.get("issues", []):
                desc_text = (
                    issue.get("fields", {})
                         .get("description", {})
                         .get("content", [{}])[0]
                         .get("content", [{}])[0]
                         .get("text", "")
                )
                issues.append(desc_text)

            next_page_token = data.get("nextPageToken")

            # Save progress after every successful batch
            self._save_checkpoint(issues, next_page_token)

            is_last = data['isLast']
            print(f"Fetched {len(issues)} issues...", end="\r")

        num_issues_fetched = len(issues)
        print(f"\n✅ Total issues fetched: {num_issues_fetched}")
        if num_issues_fetched == 0:
            return False

        self.dataframe = pd.DataFrame({"description": issues})
        return True

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

        fetch_status = self._fetch_data()
        if not fetch_status:
            print("🛑 Pipeline terminated due to data fetching error.")
            return

        self._extract_servers()
        self._classify_technology()

        self._generate_plots()
