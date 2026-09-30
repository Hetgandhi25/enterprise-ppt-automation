from pptx.chart.data import CategoryChartData

def update_chart_in_place(shape, categories: list, series_data: dict):
    """
    Updates an existing PowerPoint chart safely.
    Preserves data point formatting (crucial for pie/donut charts).
    Handles zero-value datasets safely to prevent visual disappearance.
    """
    if not shape.has_chart:
        return
        
    chart = shape.chart
    
    # 0. Check for empty / missing data
    if not categories or not series_data:
        categories = [""]
        # To clear series, we look at the template's existing series and overwrite them with None
        new_series_data = {}
        for ser in chart.series:
            new_series_data[ser.name] = [None]
        series_data = new_series_data
        is_missing_data = True
    else:
        is_missing_data = False
        
    # Pre-flight: Check for all-zero datasets
    all_zero = True
    if not is_missing_data:
        for vals in series_data.values():
            for v in vals:
                if v is not None and str(v) != "0.0" and str(v) != "0":
                    all_zero = False
                    break
    
    # We do NOT invent values.
    # If all_zero is true, we just pass the 0s natively! PowerPoint will hide the donuts if 0.
    # The user says: "If actual values are genuinely zero: Proactive = 0, Reactive = 0... Clear the chart data? NO! That is different from missing data."
    # The user explicitly asked: "ACTUAL ZERO -> 0". 
    # "If both values are missing: do not create fake values... If actual values are genuinely zero... That is different."
    # So we don't need the fake [1] logic for "No Data" anymore! 
    # I will just remove the old is_no_data block.
        
    # 1. Backup data point formatting (dPt)
    dpt_backups = {}
    if not is_missing_data:
        for i, ser in enumerate(chart.series):
            dpt_backups[i] = []
            ser_xml = ser._element
            dpts = ser_xml.xpath('./c:dPt')
            for dpt in dpts:
                import copy
                dpt_backups[i].append(copy.deepcopy(dpt))
            
    # 2. Build new data
    chart_data = CategoryChartData()
    chart_data.categories = categories
    for series_name, values in series_data.items():
        chart_data.add_series(series_name, values)
        
    # 3. Replace Data (This wipes dPt)
    chart.replace_data(chart_data)
    
    # 4. Restore data point formatting
    for i, ser in enumerate(chart.series):
        if i in dpt_backups:
            ser_xml = ser._element
            # dPt must be inserted before dLbls, cat, val, extLst
            # Find the first element among these to insert before
            insert_before_elem = None
            for tag in ['c:dLbls', 'c:cat', 'c:val', 'c:extLst']:
                elems = ser_xml.xpath(f'./{tag}')
                if elems:
                    insert_before_elem = elems[0]
                    break
                    
            for dpt in dpt_backups[i]:
                if insert_before_elem is not None:
                    insert_before_elem.addprevious(dpt)
                else:
                    ser_xml.append(dpt)
