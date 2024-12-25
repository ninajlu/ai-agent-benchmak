from benchmark.core import DataSource
from simple_salesforce import Salesforce
import os

class SalesforceDataSource(DataSource):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.sf = None
        
    async def initialize(self):
        """Initialize Salesforce connection"""
        self.sf = Salesforce(
            username=self.config.get("username"),
            password=self.config.get("password"),
            security_token=self.config.get("security_token"),
            domain=self.config.get("domain", "test")
        )
        
    async def get_data(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve data from Salesforce"""
        object_type = query.get("type")
        filters = query.get("filters", {})
        
        # Build SOQL query
        where_clauses = [f"{k} = '{v}'" for k, v in filters.items()]
        where_string = " AND ".join(where_clauses)
        
        soql = f"SELECT Id, Name FROM {object_type}"
        if where_string:
            soql += f" WHERE {where_string}"
            
        return self.sf.query(soql) 