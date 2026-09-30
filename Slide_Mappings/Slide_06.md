# Page: Slide 6 - Performance SLA & Ticket Trend
**CRM UI Tab:** Help Desk (Raw Ticket Export) / Report -> Customer Wise Report
**Fallback Configuration:** Processes via Raw_Ticket_Dump.xlsx

## Field Mappings
The backend (RawTicketProcessor) mathematically parses timestamps to generate charts.
- **Month / Timestamps:** Pulled from Open Date and Close Date columns to aggregate SLA records by month.
- **Ticket Counts:** Derived by counting total Ticket IDs that fall into the target month.
