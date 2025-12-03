JIRA_DOMAIN = "alonberkman.atlassian.net"
EMAIL = "alonberkman2004@gmail.com"
API_TOKEN = "ATATT3xFfGF0yNksf0_IzSN18WXzQFXsNM6KTHJOAc2EB1vCcjm01GN9XOF-CrIio12nJGTvPL98To85QmNN8FaHJmcxDHWZ9K5Ht7t7Fsac6fgm3-knexiOT47-FcPGEpHREkeB3RDlCY5BXC9_kuiAVPOx_yW0KhlGCjr5vIKqlZISn2u1XLk=1DD0F0EA"
PROJECT_KEY = "TONICDEV"
TOTAL_ISSUES_NUM = 20000
BATCH_SIZE = 50


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
