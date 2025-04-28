
import pandas as pd

# Paths to the nine datasets
files = {
    'True-H-Gen': '/mnt/data/true_answering_temp_0.7_You_are_a_helpful_assistant._general_prompt.xlsx',
    'True-H-Orig': '/mnt/data/true_answering_temp_0.7_You_are_a_helpful_assistant._with_original_prompt.xlsx',
    'True-E-Gen': '/mnt/data/true_answering_temp_0.7_You_are_an_expert_in_reverse_turing_test_guesses._general_prompt.xlsx',
    'True-E-Orig': '/mnt/data/true_answering_temp_0.7_You_are_an_expert_in_reverse_turing_test_guesses._with_original_prompt.xlsx',
    'Mock-H-Gen': '/mnt/data/mock_answering_temp_0.7_You_are_a_helpful_assistant._general_prompt.xlsx',
    'Mock-H-Orig': '/mnt/data/mock_answering_temp_0.7_You_are_a_helpful_assistant._with_original_prompt.xlsx',
    'Mock-E-Gen': '/mnt/data/mock_answering_temp_0.7_You_are_an_expert_in_reverse_turing_test_guesses._general_prompt.xlsx',
    'Mock-E-Orig': '/mnt/data/mock_answering_temp_0.7_You_are_an_expert_in_reverse_turing_test_guesses._with_original_prompt.xlsx',
    'Dialogue':      '/mnt/data/conversations with LLM - merged.xlsx'
}

rows = []

for cond, path in files.items():
    df = pd.read_excel(path)
    # Paragraph experiments
    if cond != 'Dialogue':
        # count rows by writer type
        n_human_rows = (df['Writer'] == 'Human').sum()
        n_llm_rows   = (df['Writer'] != 'Human').sum()
        # each row has 5 paragraphs
        hr = n_human_rows * 5
        lr = n_llm_rows * 5
        # compute accuracy across all ChatGPT Guess columns
        guess_cols = [c for c in df.columns if c.startswith('ChatGPT Guess')]
        correct = 0
        total = 0
        for _, row in df.iterrows():
            true = 'Human' if row['Writer']=='Human' else 'AI'
            for col in guess_cols:
                pred = 'Human' if str(row[col]).lower().startswith('human') else 'AI'
                correct += (pred == true)
                total += 1
        acc = correct / total * 100
        rows.append({
            'Condition': cond,
            'Answer Mode': 'True'   if cond.startswith('True') else 'Mock',
            'Priming':     'Helpful' if '-H-' in cond else 'Expert',
            'Prompt Visible': 'No'   if cond.endswith('-Gen') else 'Yes',
            '#Paragraphs Human': hr,
            '#Paragraphs LLM':    lr,
            'Accuracy (%)':       round(acc, 1)
        })
    else:
        # Conversation experiment
        correct = df['True/False Guess'].sum()
        total   = len(df)
        rows.append({
            'Condition':       cond,
            'Answer Mode':     'N/A',
            'Priming':         '(default)',
            'Prompt Visible':  'N/A',
            '#Paragraphs Human': 50,
            '#Paragraphs LLM':    50,
            'Accuracy (%)':    round(correct/total*100, 1)
        })

# assemble table
table1 = pd.DataFrame(rows, columns=[
    'Condition','Answer Mode','Priming','Prompt Visible',
    '#Paragraphs Human','#Paragraphs LLM','Accuracy (%)'
])
print(table1.to_markdown(index=False))
