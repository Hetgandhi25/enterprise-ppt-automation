import pandas as pd
from pathlib import Path
import random

def generate_dummies():
    fixtures_dir = Path(__file__).parent
    fixtures_dir.mkdir(parents=True, exist_ok=True)
    
    customers = ["ASG India", "Sun Pharma", "L&T Finance", "Tata Motors"]
    
    # 1. Customer Service Report
    data = []
    services = ["ILL", "MPLS", "SD-WAN", "Broadband"]
    locations = ["Mumbai", "Bangalore", "Delhi", "Chennai"]
    for cust in customers:
        num_records = random.randint(5, 20)
        for i in range(num_records):
            data.append({
                "Client Name": cust,
                "Client Code": f"CUST{random.randint(100,999)}",
                "Service Type": random.choice(services),
                "Service ID": f"SRV{random.randint(1000,9999)}",
                "Install City": random.choice(locations)
            })
    pd.DataFrame(data).to_excel(fixtures_dir / "Customer_Service_Report.xlsx", index=False)
    
    # 2. SLA Report
    data = []
    months = ["2026-05", "2026-06", "2026-07"]
    for cust in customers:
        for month in months:
            data.append({
                "Customer Name": cust,
                "Month": month,
                "SLA %": round(random.uniform(98.0, 100.0), 2),
                "Tickets Raised": random.randint(0, 15)
            })
    pd.DataFrame(data).to_excel(fixtures_dir / "SLA_Report.xlsx", index=False)
    
    # 3. Location SLA Report
    data = []
    for cust in customers:
        for loc in locations:
            data.append({
                "Customer Name": cust,
                "Location": loc,
                "Link ID": f"LNK{random.randint(100,999)}",
                "SLA %": round(random.uniform(98.0, 100.0), 2),
                "Downtime Duration": round(random.uniform(0.0, 10.0), 1),
                "Reason": "Fiber Cut" if random.random() > 0.8 else "Power Failure"
            })
    pd.DataFrame(data).to_excel(fixtures_dir / "Location_SLA_Report.xlsx", index=False)
    
    # 4. Raw Ticket Dump (Replaces Incident Report and SLA Report)
    data = []
    subject_types = ["Link Down - MPLS/P2P", "Internet Not Working - ILL", "Link Flapping", "Slowness"]
    rfos = ["Last Mile Issue", "Backhaul Network Issue", "TP Issue", "Ishan Network Issue", 
            "Customer End Issue", "Other Issue (Link Was Up)", "Planned Maintenance Activity", "Power Failure"]
    ticket_sources = ["Proactive", "Reactive"]
    categories = ["Complaint", "Request"]
    statuses = ["Close", "Closed (Auto)", "Pending", "Open"]
    months = ["2026-05", "2026-06", "2026-07"]
    
    for cust in customers:
        num_tickets = random.randint(30, 80)
        for i in range(num_tickets):
            total_aging = round(random.uniform(1.0, 50.0), 1)
            cust_aging = round(random.uniform(0.0, total_aging - 0.5), 1)
            
            data.append({
                "Ticket ID": f"TCK-{random.randint(10000, 99999)}",
                "Customer Name": cust,
                "Month": random.choice(months),
                "Location": random.choice(locations),
                "Link ID": f"LNK{random.randint(100,999)}",
                "Category": random.choice(categories),
                "Ticket Source": random.choice(ticket_sources),
                "Status": random.choice(statuses),
                "Subject Type": random.choice(subject_types),
                "RFO": random.choice(rfos),
                "Total Aging Hours": total_aging,
                "Customer Bucket Aging Hours": cust_aging
            })
    pd.DataFrame(data).to_excel(fixtures_dir / "Raw_Ticket_Dump.xlsx", index=False)
    
    # 5. Invoices Report (Client Ageing V2)
    data = []
    for cust in customers:
        num_invoices = random.randint(1, 5)
        for i in range(num_invoices):
            data.append({
                "Customer Name": cust,
                "Invoice Number": f"INV-{random.randint(10000,99999)}",
                "Invoice Date": "2026-07-01",
                "Billing Period Duration": "Monthly",
                "Opening Balance": round(random.uniform(5000, 100000), 2),
                "Ageing Bucket": random.choice(["0-30 days", "31-60 days", "60+ days"])
            })
    pd.DataFrame(data).to_excel(fixtures_dir / "Client_Ageing_V2.xlsx", index=False)

    # 6. Retention Report
    data = []
    for cust in customers:
        num_retentions = random.randint(0, 3)
        for i in range(num_retentions):
            data.append({
                "Client ID": cust,
                "Service Name": random.choice(services),
                "Location": random.choice(locations),
                "Bandwidth": random.choice(["10 Mbps", "50 Mbps", "100 Mbps"]),
                "Disconnection Reason": random.choice(["Price", "Moving", "No longer needed"]),
                "Last Date": "2026-07-30",
                "Status": "Pending" if random.random() > 0.3 else "Terminated"
            })
    pd.DataFrame(data).to_excel(fixtures_dir / "Retention_Report.xlsx", index=False)
    
    print("Dummy files generated successfully.")

if __name__ == "__main__":
    generate_dummies()
