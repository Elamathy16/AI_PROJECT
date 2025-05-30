import pandas as pd
from difflib import get_close_matches

# Load the dataset once
df = pd.read_excel("HSN_Master_Data.xlsx")
df['HSNCode'] = df['HSNCode'].astype(str)

def validate_hsn_code(hsn):
    result = {}

    if not hsn.isdigit() or len(hsn) not in [2, 4, 6, 8]:
        result["status"] = "Invalid Format"
        result["reason"] = "HSN should be numeric with 2, 4, 6, or 8 digits."
        return result

    if hsn in df['HSNCode'].values:
        desc = df[df['HSNCode'] == hsn]['Description'].values[0]
        result["status"] = "Valid"
        result["description"] = desc

        # Hierarchical validation
        levels = [hsn[:i] for i in [2, 4, 6] if i < len(hsn)]
        hierarchy = {code: df[df['HSNCode'] == code]['Description'].values[0]
                     for code in levels if code in df['HSNCode'].values}
        result["hierarchy"] = hierarchy
    else:
        result["status"] = "Not Found"
        result["reason"] = "HSN not found in master data."
    
    return result

def suggest_hsn_codes(description, limit=5):
    description = description.lower()
    matches = df[df['Description'].str.lower().str.contains(description, na=False)]
    
    if matches.empty:
        close = get_close_matches(description, df['Description'].str.lower(), n=limit)
        matches = df[df['Description'].str.lower().isin(close)]
    
    suggestions = matches[['HSNCode', 'Description']].head(limit).to_dict(orient='records')
    return {"suggestions": suggestions or "No close match found"}
