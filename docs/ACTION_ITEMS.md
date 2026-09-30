# Action Items & Meeting Notes

**Date:** July 31, 2026

## 1. Retention Pending
- **Task:** Update the PPT generation logic for the "Retention Pending" slide.
- **Requirements:** 
  - Calculate and display the total number of Customer IDs present.
  - Calculate and display the total number of Service IDs that have a "Retention Pending" status.

## 2. Invoice Pendency
- **Task:** Review and verify the Invoice Pendency data processing module.
- **Requirements:** Ensure pending invoice details are correctly extracted, calculated, and formatted for the final report.

## 3. Slide 13
- **Task:** Review and discuss all points mentioned in Slide 13.
- **Status:** Pending detailed review of the slide content.

## 4. SLA Validation & Information
- **Task:** Implement SLA availability checks for points 6, 7, 8, and 9.
- **Dependencies:** 
  - Evaluate the SLA metrics with Anada Sir.
  - Collect the required SLA baseline information from Atul Sir.

## 5. Graphical Visualization
- **Task:** Finalize the dashboard and PPT graphical visualization styles.
- **Dependencies:** Contact Sonali Khokani Ma'am to discuss how the graphical visualizations should look in the final design.

## 6. Customer ID Issue
- **Task:** Resolve the data discrepancy where Customer IDs are different but the Customer Name is the same.
- **Requirements:** 
  - Verify the correct Customer ID mapping.
  - Identify the reason for duplicate customer names in the source data.
  - Implement deduplication or mapping logic in the Pandas processing engine (`backend/automation/data_processing.py`).

---

## People to Contact
- **Anada Sir:** SLA evaluation for points 6, 7, 8, and 9.
- **Atul Sir:** SLA-related information.
- **Sonali Khokani Ma'am:** Graphical visualization and dashboard/UI design.
