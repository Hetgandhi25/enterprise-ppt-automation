# Page: Slide 12 - Account / Invoice Pendency
**CRM UI Tab:** Finance -> Client Ageing V2
**REST Endpoint:** /index.php/client_aging_mst_v2/loadData

## Field Mappings for invoice_table
- **Invoice Number:** Pulled from the Inv Ref. No. column.
- **Billing Period:** Merged dynamically by combining Invoice From Date + Invoice To Date.
- **Pending Amount:** Pulled from the Pending (or Opening Balance) column.
- **Ageing Bucket:** Pulled from the Ageing column (0-30, 30-60, etc.).
- **Status:** Hardcoded as "Unpaid" for pending lines.
