from typing import Dict, Any
import hubspot
from benchmark.core import DataSource

class HubspotDataSource(DataSource):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.client = None
        
    async def initialize(self):
        """Initialize HubSpot client"""
        self.client = hubspot.Client.create(access_token=self.config["api_key"])
        
    async def get_data(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Get data from HubSpot"""
        data = {
            "contacts": [],
            "deals": [],
            "tickets": []
        }
        
        if "contacts" in self.config["scopes"]:
            contacts = self.client.crm.contacts.get_all()
            data["contacts"] = [c.to_dict() for c in contacts]
            
        if "deals" in self.config["scopes"]:
            deals = self.client.crm.deals.get_all()
            data["deals"] = [d.to_dict() for d in deals]
            
        if "tickets" in self.config["scopes"]:
            tickets = self.client.crm.tickets.get_all()
            data["tickets"] = [t.to_dict() for t in tickets]
            
        return data 