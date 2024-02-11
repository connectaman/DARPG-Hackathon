import pandas as pd
import json
from functools import lru_cache

@lru_cache
def get_org_code_from_category_code_mapping(path):
    df = pd.read_excel(path)
    grouped_df  = df.groupby("OrgCode")['Description'].apply(lambda x: ' \n '.join(f"{i+1}. {desc}" for i, desc in enumerate(x))).reset_index()
    # Create the desired result format
    result = []
    for index, row in grouped_df.iterrows():
        result.append({
            'text': f"Org Code: {row['OrgCode']} \n Groups: {row['Description']}"
        })

    return result

@lru_cache
def get_action_history(path):
    with open(path,encoding="utf8") as f:
        data = json.loads(f.read())

    result = []

    for d in data:
        if "subject_content_text" in d.keys() and "remarks_text" in d.keys():
            result.append({
                "text":f"User Context: {d['subject_content_text']} \n Remarke by Govt. Official: {d['remarks_text']}"
            })

    return result

#get_org_code_from_category_code_mapping(path="/path/to/CategoryCode_Mapping.xlsx")

#get_action_history(path="/path/to/no_pii_action_history,json")