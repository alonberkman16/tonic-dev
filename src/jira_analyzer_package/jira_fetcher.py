import json
import os
import pandas as pd

from ..consts import *
from ..utils import get_jira_api_auth, run_request_with_error_handling


class JiraFetcher:
    """Fetches the issues from Jira"""

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

    def fetch_data(self) -> pd.DataFrame:
        """Pulls all issue descriptions from the Jira project using JQL and pagination."""
        # Set up login and query variables
        url = f"https://{JIRA_DOMAIN}/rest/api/3/search/jql"
        auth = get_jira_api_auth(EMAIL, API_TOKEN)
        params = {
            "jql": f"project = {PROJECT_KEY} ORDER BY created ASC",
            "maxResults": FETCHER_BATCH_SIZE,
            "fields": ["description"]
        }

        is_last = False
        issues, next_page_token = self._load_checkpoint()

        if issues and next_page_token is None and os.path.exists(CACHE_FILE_PATH):
            print(f"✅ Data fetch already completed according to checkpoint. Total issues fetched: {len(issues)}")
            return pd.DataFrame({"description": issues})

        if issues:
            print(f"Resumed fetch with {len(issues)} issues already retrieved.")
        else:
            print(f"🔄 Starting new fetch for project: {PROJECT_KEY}...")
        while not is_last:
            if next_page_token:
                params["nextPageToken"] = next_page_token

            data = run_request_with_error_handling(method='GET', url=url, headers=JIRA_API_HEADERS, params=params,
                                                   auth=auth)
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
        return pd.DataFrame({"description": issues})
