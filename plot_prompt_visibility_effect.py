
import pandas as pd
import matplotlib.pyplot as plt

# Paths to the Helpful Assistant datasets
path_gen = 'true_answering_temp_0.7_You_are_a_helpful_assistant._general_prompt.xlsx'
path_orig = 'true_answering_temp_0.7_You_are_a_helpful_assistant._with_original_prompt.xlsx'

# Load the data
df_gen = pd.read_excel(path_gen)
df_orig = pd.read_excel(path_orig)

# Map each topic to its ChatGPT Guess column
topic_cols = {
    'Childhood Memory': 'ChatGPT Guess',
    'Milk': 'ChatGPT Guess.1',
    'Need for Company': 'ChatGPT Guess.2',
    'Music': 'ChatGPT Guess.3',
    'Family': 'ChatGPT Guess.4'
}

def compute_accuracy(df, col):
    correct = sum(
        1 for _, row in df.iterrows()
        if (row['Writer'] == 'Human' and str(row[col]).lower().startswith('human'))
        or (row['Writer'] != 'Human' and not str(row[col]).lower().startswith('human'))
    )
    return correct / len(df) * 100

# Compute per-topic accuracies
topics = list(topic_cols.keys())
acc_gen = [compute_accuracy(df_gen, topic_cols[t]) for t in topics]
acc_orig = [compute_accuracy(df_orig, topic_cols[t]) for t in topics]

# Plot
x = range(len(topics))
width = 0.35
plt.figure(figsize=(8,4))
plt.bar([i-width/2 for i in x], acc_gen, width, label='Without Original Prompt', color='#1f77b4')
plt.bar([i+width/2 for i in x], acc_orig, width, label='With Original Prompt', color='#ff7f0e')
# Add red dotted line at 50%
plt.axhline(50, linestyle='--', color='red')
plt.xticks(x, topics, rotation=45, ha='right')
plt.ylabel('Accuracy (%)')
plt.title('Effect of Prompt Visibility on Detection Accuracy\n(Helpful Assistant)')
plt.legend()
plt.tight_layout()
plt.savefig('prompt_visibility_effect_redline.png', dpi=300)
plt.show()
