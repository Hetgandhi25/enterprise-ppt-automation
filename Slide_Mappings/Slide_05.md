# Page: Slide 5 - Service Inventory Snapshot
**CRM UI Tab:** Finance -> Customer Service
**REST Endpoint:** /index.php/view_sam_orders/loadData

## Field Mappings for inventory_table
The backend aggregates links based on the Service Type.
- **Customer Name:** Extracted from the Invoice column.
- **Service Type:** Extracted from the Service Type / Business Category columns.
- **Link Count:** Derived by counting the total number of unique Service Code entries per Service Type.
