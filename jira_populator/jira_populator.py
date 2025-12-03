import requests
import time
from base64 import b64encode

from .consts import *
from .utils import create_issue_payload


def main_populate():
    """Sends post requests to the jira API in chunks & in a loop to avoid overload on the api"""
    auth_str = f"{EMAIL}:{API_TOKEN}"
    auth_base64 = b64encode(auth_str.encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    url = f"https://{JIRA_DOMAIN}/rest/api/3/issue/bulk"

    print(f"Starting generation of {TOTAL_ISSUES_NUM} issues...")

    issues_buffer = []

    for i in range(TOTAL_ISSUES_NUM):
        issues_buffer.append(create_issue_payload())

        if len(issues_buffer) == BATCH_SIZE:
            payload = {"issueUpdates": issues_buffer}

            try:
                response = requests.post(url, headers=headers, json=payload)
                if response.status_code == 201:
                    print(f"Batch {i // BATCH_SIZE + 1} successful ({i + 1}/{TOTAL_ISSUES_NUM})")
                else:
                    print(f"Error: {response.status_code} - {response.text}")

                    # Simple backoff if rate limited
                    if response.status_code == 429:
                        print("Rate limit hit. Sleeping 10s...")
                        time.sleep(10)
            except Exception as e:
                print(f"Connection Error: {e}")

            issues_buffer = []  # Clear buffer

            # Tiny sleep to not overload the API
            time.sleep(0.5)
