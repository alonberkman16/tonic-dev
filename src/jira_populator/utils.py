import random

from ..consts import TECHNOLOGY_TEMPLATES, PROJECT_KEY


def generate_server_name():
    """Generates server names with mixed casing or returns None for edge cases."""
    if random.random() < 0.05:  # 5% chance of no server name
        return None

    number = random.randint(100, 9999)
    prefix_style = random.choice(["srv-", "SRV-", "Srv-", "sRv-"])

    # Occasional invalid format (missing dash)
    if random.random() < 0.02:
        return f"srv{number}"

    return f"{prefix_style}{number}"


def create_issue_payload():
    """Generates a single issue data dict."""
    category = random.choice(list(TECHNOLOGY_TEMPLATES.keys()))
    template = random.choice(TECHNOLOGY_TEMPLATES[category])

    # Generate data for placeholders
    server1 = generate_server_name()
    server2 = generate_server_name()
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
