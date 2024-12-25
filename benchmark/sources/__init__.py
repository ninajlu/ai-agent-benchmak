from typing import Dict, Any

SOURCE_SCHEMAS = {
    "salesforce": {
        "username": {
            "type": "string",
            "description": "Salesforce username"
        },
        "password": {
            "type": "string",
            "description": "Salesforce password"
        },
        "security_token": {
            "type": "string",
            "description": "Security token"
        },
        "domain": {
            "type": "string",
            "description": "Instance domain (test/prod)"
        }
    },
    "hubspot": {
        "api_key": {
            "type": "string",
            "description": "HubSpot API key"
        },
        "portal_id": {
            "type": "string",
            "description": "HubSpot portal ID"
        },
        "scopes": {
            "type": "array",
            "description": "Required access scopes",
            "default": ["contacts", "deals", "tickets"]
        }
    },
    "gmail": {
        "credentials_file": {
            "type": "string",
            "description": "Path to Google credentials JSON"
        },
        "email": {
            "type": "string",
            "description": "Gmail address to access"
        },
        "scopes": {
            "type": "array",
            "description": "Gmail API scopes",
            "default": ["https://www.googleapis.com/auth/gmail.readonly"]
        }
    },
    "google_drive": {
        "credentials_file": {
            "type": "string",
            "description": "Path to Google credentials JSON"
        },
        "folder_id": {
            "type": "string",
            "description": "Root folder ID to access"
        },
        "scopes": {
            "type": "array",
            "description": "Drive API scopes",
            "default": ["https://www.googleapis.com/auth/drive.readonly"]
        }
    },
    "slack": {
        "bot_token": {
            "type": "string",
            "description": "Slack bot user OAuth token"
        },
        "channels": {
            "type": "array",
            "description": "Channel IDs to monitor",
            "default": []
        },
        "workspace_id": {
            "type": "string",
            "description": "Slack workspace ID"
        }
    },
    "zendesk": {
        "subdomain": {
            "type": "string",
            "description": "Zendesk subdomain"
        },
        "email": {
            "type": "string",
            "description": "Admin email address"
        },
        "api_token": {
            "type": "string",
            "description": "API token"
        }
    },
    "intercom": {
        "access_token": {
            "type": "string",
            "description": "Intercom access token"
        },
        "workspace_id": {
            "type": "string",
            "description": "Workspace ID"
        }
    },
    "synthetic": {
        "employee_count": {
            "type": "number",
            "description": "Number of employees to simulate"
        },
        "num_opportunities": {
            "type": "number",
            "description": "Number of sales opportunities"
        },
        "total_sales_target": {
            "type": "number",
            "description": "Total sales target amount"
        }
    }
}

def get_available_sources() -> Dict[str, Dict[str, Any]]:
    """Get available data sources and their configuration schemas"""
    return SOURCE_SCHEMAS 