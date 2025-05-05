
import matplotlib.pyplot as plt

labels = ['Human Partner', 'LLM Partner']
guessed_human = [90, 90]  # 90% guessed Human for both
guessed_ai = [10, 10]     # 10% guessed AI for both

x = range(len(labels))
width = 0.35

plt.figure(figsize=(5, 4))
plt.bar([i - width/2 for i in x], guessed_human, width, label='Guessed Human', color='#1f77b4')
plt.bar([i + width/2 for i in x], guessed_ai, width, label='Guessed AI', color='#ff7f0e')
plt.xticks(x, labels)
plt.ylabel('Accuracy (%)')
plt.title('ChatGPT Conversation Guess Distribution')
plt.legend()
plt.tight_layout()
plt.savefig('conversation_guess_distribution.png', dpi=300)
plt.show()
