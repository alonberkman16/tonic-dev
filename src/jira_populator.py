import random
import concurrent.futures

from .consts import *
from .utils import get_jira_api_auth, run_request_with_error_handling


class JiraPopulator:
    def __init__(self, total_issues_num: int = 20000):
        self.total_issues_num = total_issues_num

    @staticmethod
    def _generate_server_name():
        """Generates server names with mixed casing or returns None for edge cases."""
        if random.random() < 0.05:  # 5% chance of no server name
            return None

        number = random.randint(100, 9999)
        prefix_style = random.choice(["srv-", "SRV-", "Srv-", "sRv-"])

        # Occasional invalid format (missing dash)
        if random.random() < 0.02:
            return f"srv{number}"

        return f"{prefix_style}{number}"

    def _create_issue_payload(self):
        """Generates a single issue data dict."""
        category = random.choice(list(TECHNOLOGY_TEMPLATES.keys()))
        template = random.choice(TECHNOLOGY_TEMPLATES[category])

        # Generate data for placeholders
        server1 = self._generate_server_name()
        server2 = self._generate_server_name()
        db_name = f"DB_{random.randint(1, 100)}"

        # Fill template, handling None (missing server) gracefully for the text
        s1_text = server1 if server1 else "unknown-server"
        s2_text = server2 if server2 else "gateway"

        description = template.format(server=s1_text, server2=s2_text, db_name=db_name)

        # Summary is a shorter version
        summary = f"[{category.upper()}] Issue detected on {s1_text}"

        return {
            "fields": {
                "project": {"key": PROJECT_KEY},
                "summary": summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [{
                        "type": "paragraph",
                        "content": [{"type": "text", "text": description}]
                    }]
                },
                "issuetype": {"name": "Task"}
            }
        }

    def populate(self, max_parallel_api_calls: int = 3):
        """Sends post requests to the jira API in chunks & in a loop to avoid overload on the api"""
        url = f"https://{JIRA_DOMAIN}/rest/api/3/issue/bulk"
        auth = get_jira_api_auth(EMAIL, API_TOKEN)

        print(f"Starting generation of {self.total_issues_num} issues...")

        all_issues_lst = [self._create_issue_payload() for i in range(self.total_issues_num)]
        payload_chunks_lst = [{"issueUpdates": all_issues_lst[i:i + POPULATOR_BATCH_SIZE]} for i in range(0, len(all_issues_lst), POPULATOR_BATCH_SIZE)]

        # Execute the payload chunks with multithreading. There is no need to collect the results.
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_parallel_api_calls) as executor:
            for payload_chunk in payload_chunks_lst:
                executor.submit(run_request_with_error_handling, method='POST', url=url, headers=JIRA_API_HEADERS,
                                params=payload_chunk, auth=auth, timeout_secs=60)
