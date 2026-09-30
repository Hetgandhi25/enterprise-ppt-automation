from typing import List, Dict, Any

# Mock Database mapping CSM usernames to their passwords, roles, and mapped customers.
# In a real system, this would be stored in a relational database (e.g. PostgreSQL) and accessed via ORM (e.g. SQLAlchemy).

MOCK_USERS: Dict[str, Dict[str, Any]] = {
    "admin": {
        "password": "admin",
        "role": "admin",
        "customers": ["ALL"],
        "name": "System Administrator"
    },
    "csm_asg": {
        "password": "password1234",
        "role": "csm",
        "customers": ["ASG India", "ASG Global"],
        "name": "ASG Manager"
    },
    "Shah.Manank": {
        "password": "Apr@2025",
        "role": "csm",
        "customers": [], # Live sync dynamically fetches customers
        "name": "Manank Shah (UAT)",
        "live_sync": True
    },
    "csm_sun": {
        "password": "password123",
        "role": "csm",
        "customers": ["Sun Pharma"],
        "name": "Sun Pharma CSM"
    },
    "csm_tata": {
        "password": "password123",
        "role": "csm",
        "customers": ["Tata Motors"],
        "name": "Tata Motors CSM"
    },
    "csm_hdfc": {
        "password": "password123",
        "role": "csm",
        "customers": ["HDFC Bank"],
        "name": "HDFC Bank CSM"
    },
    "csm_reliance": {
        "password": "password123",
        "role": "csm",
        "customers": ["Reliance Industries"],
        "name": "Reliance CSM"
    },
    "csm_wipro": {
        "password": "password123",
        "role": "csm",
        "customers": ["Wipro"],
        "name": "Wipro CSM"
    },
    "csm_infosys": {
        "password": "password123",
        "role": "csm",
        "customers": ["Infosys"],
        "name": "Infosys CSM"
    }
}
