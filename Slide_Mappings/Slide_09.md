# Page: Slide 9 - Incident Summary Table
**CRM UI Tab:** Help Desk (Raw Ticket Export)

## Field Mappings for incident_table
The backend maps Reason For Outage (RFO) text to exact table buckets:
- **Location:** Pulled from the Location column.
- **Cable Issue Count:** Increments if RFO column contains "cable", "fiber", or "last mile".
- **Backhaul Impacted Count:** Increments if RFO column contains "backhaul", "ishan network", or "core device".
- **Electricity Issue Count:** Increments if RFO column contains "power" or "electricity".
