import json
from fastmcp import FastMCP
import os 

# --------------------------------
# Service Layer (Simulates external API/Logic)
# --------------------------------
class BillingService:
    def __init__(self):
        # Mock Database simulating your external CRM
        self.customers = {
            "alice@acme.com": {"id": "CUST_001", "tier": "Enterprise", "status": "Active"},
            "bob@giant-corp.com": {"id": "CUST_002", "tier": "Free", "status": "Suspended"},
        }
        self.contracts = {
            "CUST_001": {"sla": "99.99%", "support": "Platinum"},
            "CUST_002": {"sla": "None", "support": "Community"},
        }

    def get_tier(self, email: str):
        customer = self.customers.get(email)
        if not customer:
            return {"error": "Customer not found"}
        return customer

    def get_sla(self, customer_id: str):
        contract = self.contracts.get(customer_id)
        if not contract:
            return {"error": "No active contract found"}
        return contract

# Initialize Service
service = BillingService()

# Initialize FastMCP (FIX: Removed 'version="1.0.0"')
mcp = FastMCP(name = "Business-Client")
# --------------------------------
# Tool 1: Get Customer Tier
# --------------------------------
@mcp.tool(
    name="get-customer-tier",
    description="Retrieve the subscription tier and status for a customer using their email address."
)
def get_customer_tier(email: str):
    """
    args:
        email: The customer's email address (e.g., 'alice@acme.com')
    """
    try:
        data = service.get_tier(email)
        return {
            "content": [
                {
                    "type": "text", 
                    "text": f"✅ Customer Data Retrieved:\n{json.dumps(data, indent=2)}"
                }
            ]
        }
    except Exception as e:
        return {"content": [{"type": "text", "text": f"❌ Error: {str(e)}"}], "isError": True}

# --------------------------------
# Tool 2: Get Contract SLA
# --------------------------------
@mcp.tool(
    name="get-contract-sla",
    description="Get the guaranteed uptime SLA and support level for a specific customer ID."
)
def get_contract_sla(customer_id: str):
    """
    args:
        customer_id: The unique ID of the customer (e.g., 'CUST_001')
    """
    try:
        data = service.get_sla(customer_id)
        return {
            "content": [
                {
                    "type": "text", 
                    "text": f"✅ Contract Details:\n{json.dumps(data, indent=2)}"
                }
            ]
        }
    except Exception as e:
        return {"content": [{"type": "text", "text": f"❌ Error: {str(e)}"}], "isError": True}

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)