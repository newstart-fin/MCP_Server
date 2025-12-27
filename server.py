import json
import os
from fastmcp import FastMCP

# --------------------------------
# Service Layer (Mock external logic)
# --------------------------------
class BillingService:
    def __init__(self):
        self.customers = {
            "alice@acme.com": {
                "id": "CUST_001",
                "tier": "Enterprise",
                "status": "Active"
            },
            "bob@giant-corp.com": {
                "id": "CUST_002",
                "tier": "Free",
                "status": "Suspended"
            },
        }

        self.contracts = {
            "CUST_001": {
                "sla": "99.99%",
                "support": "Platinum"
            },
            "CUST_002": {
                "sla": "None",
                "support": "Community"
            },
        }

    def get_tier(self, email: str):
        return self.customers.get(email, {"error": "Customer not found"})

    def get_sla(self, customer_id: str):
        return self.contracts.get(customer_id, {"error": "No active contract found"})


service = BillingService()

# --------------------------------
# FastMCP initialization
# (MATCHES YOUR WORKING REFERENCE)
# --------------------------------
mcp = FastMCP(
    name="business-client-mcp",
    version="1.0.0"
)

print("Billing MCP Server running (HTTP mode)")

# --------------------------------
# Tool 1: Get Customer Tier
# --------------------------------
@mcp.tool(
    name="get-customer-tier",
    description="Retrieve the subscription tier and status for a customer using their email address."
)
def get_customer_tier(email: str):
    data = service.get_tier(email)

    return {
        "content": [
            {
                "type": "text",
                "text": f"Customer Data:\n{json.dumps(data, indent=2)}"
            }
        ]
    }

# --------------------------------
# Tool 2: Get Contract SLA
# --------------------------------
@mcp.tool(
    name="get-contract-sla",
    description="Get the guaranteed uptime SLA and support level for a specific customer ID."
)
def get_contract_sla(customer_id: str):
    data = service.get_sla(customer_id)

    return {
        "content": [
            {
                "type": "text",
                "text": f"Contract Details:\n{json.dumps(data, indent=2)}"
            }
        ]
    }

# --------------------------------
# Run (Render compatible)
# --------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))

    mcp.run(
        transport="http",
        host="0.0.0.0",   # 🔑 REQUIRED for Render
        port=port
    )
