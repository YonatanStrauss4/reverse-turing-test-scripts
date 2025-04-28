
import matplotlib.pyplot as plt

# Data for updated Figure 1 with red dotted line, updated labels
labels = [
    "True-H-Gen", "True-H-Orig", "True-E-Gen", "True-E-Orig",
    "Mimic-H-Gen", "Mimic-H-Orig", "Mimic-E-Gen", "Mimic-E-Orig",
    "Conversations"
]
accuracies = [48.8, 65.8, 43.0, 62.7, 12.9, 26.3, 7.6, 16.2, 50.0]
colors = ['#1f77b4']*4 + ['#ff7f0e']*4 + ['#2ca02c']  # blue, orange, green

plt.figure(figsize=(8, 4))
plt.bar(range(len(accuracies)), accuracies, color=colors)
# Red dotted reference line at 50%
plt.axhline(50, linestyle='--', color='red')
plt.xticks(range(len(accuracies)), labels, rotation=45, ha='right')
plt.ylabel('Accuracy (%)')
plt.title('ChatGPT Detection Accuracy across Conditions')
plt.legend(handles=[
    plt.Rectangle((0,0),1,1, color='#1f77b4'),
    plt.Rectangle((0,0),1,1, color='#ff7f0e'),
    plt.Rectangle((0,0),1,1, color='#2ca02c')
], labels=['True-answering','Mimic-answering','Conversations'], loc='upper right')
plt.tight_layout()
plt.savefig('/mnt/data/figure1_conversations_mimic.png', dpi=300)
plt.show()
