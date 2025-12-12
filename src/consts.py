import os
from dotenv import load_dotenv

load_dotenv()  # Get all the env variables

JIRA_DOMAIN = os.environ.get("JIRA_DOMAIN")
EMAIL = os.environ.get("EMAIL")
API_TOKEN = os.environ.get("API_TOKEN")
PROJECT_KEY = os.environ.get("PROJECT_KEY")

TOTAL_ISSUES_NUM = 20000
POPULATOR_BATCH_SIZE = 50  # The maximum amount that can be created per one request (by Jira)
FETCHER_BATCH_SIZE = 10
JIRA_API_HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

SERVER_REGEX = r'(?i)\b(srv-?[\w\d]+)\b'

TECHNOLOGY_TEMPLATES = {
    "database": [
        "Database {db_name} on {server} is experiencing slow query performance",
        "{server} PostgreSQL connection pool exhausted",
        "MySQL replication lag on {server} exceeds 10 seconds",
        "Oracle backup failed on {server} - tablespace full",
        "{server} MongoDB replica set member unreachable"
    ],
    "networking": [
        "Network connectivity issues between {server} and {server2}",
        "{server} experiencing packet loss to gateway",
        "VPN tunnel down affecting {server}",
        "Firewall blocking port 443 on {server}",
        "{server} DNS resolution failures"
    ],
    "authentication": [
        "LDAP authentication failing on {server}",
        "Users unable to login to {server} - Active Directory timeout",
        "{server} Kerberos ticket expiration issues",
        "SSO integration broken on {server}",
        "Failed login attempts from {server} exceed threshold"
    ],
    "api": [
        "{server} REST API returning 500 errors",
        "API rate limiting triggered on {server}",
        "{server} GraphQL endpoint timeout",
        "Webhook delivery failures from {server}",
        "{server} API gateway health check failing"
    ],
    "storage": [
        "Disk space critically low on {server} - 95% full",
        "{server} NFS mount unresponsive",
        "S3 bucket access denied from {server}",
        "{server} RAID array degraded - drive failure",
        "Backup volume on {server} out of space"
    ]
}
