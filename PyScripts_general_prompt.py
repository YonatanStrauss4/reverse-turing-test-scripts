import pandas as pd
from openai import OpenAI
import random
import asyncio

client =  os.getenv("OPENAI_API_KEY")

async def chat_with_gpt(prompt):
    try:
        full_prompt = f"If you think the following paragraph is written by human, write just the word \"Human\". Else, if you think the following paragraph is written by a LLM, write just the word \"LLM\". This is the paragraph:\n{prompt}"
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": full_prompt},
            ],
            temperature=0.7,
        )
        return response.choices[0].message.content
    except Exception as e:
        print("An error occurred:", e)
        return None

async def main():
    df = pd.read_excel('Question_answering_(Responses).xlsx', sheet_name=0)

    # Columns to process (indexing starts from 0, so B is 1, D is 3, ..., T is 19)
    columns_to_process = [1, 3, 5, 7, 9]


    for col_idx in columns_to_process:
        col_values = df.iloc[1:, col_idx].astype('object').dropna().index.tolist()
        random.shuffle(col_values)
        for row in col_values:
            prompt = df.iat[row, col_idx]
            if isinstance(prompt, str) and prompt.strip():  # skip empty or non-string cells
                reply = await chat_with_gpt(prompt)
                print(reply)
                if reply:
                    df.iat[row, col_idx + 1] = reply

    df.to_excel("True_answering_temp_0.7_You_are_a_helpful_assistant._genereal_prompt.xlsx", index=False)

if __name__ == "__main__":
    asyncio.run(main())

