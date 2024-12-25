from typing import Dict, Any
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from benchmark.core import DataSource

class GmailDataSource(DataSource):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.service = None
        
    async def initialize(self):
        """Initialize Gmail API client"""
        credentials = service_account.Credentials.from_service_account_file(
            self.config["credentials_file"],
            scopes=self.config["scopes"]
        )
        
        delegated_credentials = credentials.with_subject(self.config["email"])
        self.service = build('gmail', 'v1', credentials=delegated_credentials)
        
    async def get_data(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Get email data from Gmail"""
        results = self.service.users().messages().list(
            userId='me',
            maxResults=query.get('limit', 100)
        ).execute()
        
        messages = []
        for msg in results.get('messages', []):
            message = self.service.users().messages().get(
                userId='me',
                id=msg['id']
            ).execute()
            messages.append(message)
            
        return {
            "messages": messages
        }

class GoogleDriveDataSource(DataSource):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.service = None
        
    async def initialize(self):
        """Initialize Drive API client"""
        credentials = service_account.Credentials.from_service_account_file(
            self.config["credentials_file"],
            scopes=self.config["scopes"]
        )
        
        self.service = build('drive', 'v3', credentials=credentials)
        
    async def get_data(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Get files and folders from Drive"""
        results = self.service.files().list(
            q=f"'{self.config['folder_id']}' in parents",
            fields="files(id, name, mimeType, createdTime, modifiedTime)"
        ).execute()
        
        return {
            "files": results.get('files', [])
        } 