import pandas as pd
import json

# 1. Read the exported CSV
df = pd.read_csv('quiz_sheet.csv')

# 2. Ensure no NaNs in key or category columns
df['Option Key'] = df['Option Key'].fillna('').astype(str)
df['Category']   = df['Category'].fillna('').astype(str)

# 3. Build the nested JSON structure
sections = []
for section, sec_df in df.groupby('Section'):
    questions = []
    for qid, qdf in sec_df.groupby('QID'):
        question_text = qdf['Question Text'].iloc[0]
        options = []
        for _, row in qdf.iterrows():
            options.append({
                'key': row['Option Key'],
                'text': row['Option Text'],
                'category': row['Category']
            })
        questions.append({
            'id': qid,
            'text': question_text,
            'options': options
        })
    sections.append({
        'section': section,
        'questions': questions
    })

# 4. Export to JSON
output = {'sections': sections}
with open('quiz_structure.json', 'w') as f:
    json.dump(output, f, indent=2)

print("Exported quiz_structure.json successfully!")
