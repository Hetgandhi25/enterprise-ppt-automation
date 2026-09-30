from pathlib import Path
import pytest
import pandas as pd
from backend.processors.excel_reader import read_excel_file, clean_dataframe
from backend.utils.exceptions import ExcelValidationError

def test_read_excel_file_not_found():
    with pytest.raises(ExcelValidationError, match="not found"):
        read_excel_file(Path("non_existent_file.xlsx"))

def test_clean_dataframe():
    df = pd.DataFrame({
        " Col A ": [" val1 ", "val2", "nan"],
        "Col B": ["  ", "None", "val3"]
    })
    
    cleaned = clean_dataframe(df)
    
    assert list(cleaned.columns) == ["Col A", "Col B"]
    assert cleaned.iloc[0]["Col A"] == "val1"
    assert cleaned.iloc[2]["Col A"] is None
    assert cleaned.iloc[0]["Col B"] is None
    assert cleaned.iloc[1]["Col B"] is None
