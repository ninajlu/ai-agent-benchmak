from benchmark.core import DataSource
from synthetic_data_generator import CompanyDataGenerator
import asyncio

class SyntheticDataSource(DataSource):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.generator = CompanyDataGenerator(
            employee_count=config.get("employee_count", 200),
            num_opportunities=config.get("num_opportunities", 200),
            total_sales_target=config.get("total_sales_target", 10000000)
        )
        self.data = {}
        
    async def initialize(self):
        """Generate all synthetic data"""
        # Run data generation in a thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, self._generate_data)
        
    def _generate_data(self):
        """Generate all data types"""
        self.data = {
            "employees": self.generator.generate_employees(),
            "sales": self.generator.generate_sales_data(),
            "support": self.generator.generate_support_data(),
            "finance": self.generator.generate_finance_data(),
            "marketing": self.generator.generate_marketing_data()
        }
        
    async def get_data(self, query: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve generated data based on query"""
        data_type = query.get("type")
        filters = query.get("filters", {})
        
        if data_type not in self.data:
            raise ValueError(f"Unknown data type: {data_type}")
            
        # Apply any filters
        filtered_data = self.data[data_type]
        for key, value in filters.items():
            filtered_data = [
                item for item in filtered_data 
                if item.get(key) == value
            ]
            
        return filtered_data 