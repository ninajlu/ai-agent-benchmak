from typing import Dict, Any
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from benchmark.core import DataSource

class SlackDataSource(DataSource):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = None
        
    async def initialize(self):
        """Initialize Slack client"""
        self.client = WebClient(token=self.config["bot_token"])
        
    async def get_data(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Get data from Slack channels"""
        data = {
            "messages": [],
            "threads": [],
            "users": []
        }
        
        # Get messages from channels
        for channel in self.config["channels"]:
            try:
                result = self.client.conversations_history(
                    channel=channel,
                    limit=query.get("limit", 100)
                )
                data["messages"].extend(result["messages"])
                
                # Get thread replies
                for msg in result["messages"]:
                    if msg.get("thread_ts"):
                        replies = self.client.conversations_replies(
                            channel=channel,
                            ts=msg["thread_ts"]
                        )
                        data["threads"].append({
                            "parent_ts": msg["thread_ts"],
                            "replies": replies["messages"]
                        })
                        
            except SlackApiError as e:
                print(f"Error fetching messages: {e}")
                
        # Get user list
        try:
            users = self.client.users_list()
            data["users"] = users["members"]
        except SlackApiError as e:
            print(f"Error fetching users: {e}")
            
        return data 