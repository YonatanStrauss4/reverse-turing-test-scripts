import pandas as pd
from openai import OpenAI
import random
import asyncio

client =  os.getenv("OPENAI_API_KEY")

async def chat_with_gpt(response_text, original_prompt):
    try:
        full_prompt = (
            f"The Human or LLM was asked the following prompt:\n\"{original_prompt}\"\n\n"
            f"If you think the following paragraph is written by a human, write just the word \"Human\". "
            f"Else, if you think the following paragraph is written by a LLM, write just the word \"LLM\".\n\n"
            f"This is the paragraph:\n{response_text}"
        )

        print(full_prompt)  # Debugging line to check the prompt being sent

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

    columns_to_process = [1, 3, 5, 7, 9]

    for col_idx in columns_to_process:
        original_prompt = df.columns[col_idx]  # get the prompt in row 0 of the current column
        col_values = df.iloc[1:, col_idx].astype('object').dropna().index.tolist()
        random.shuffle(col_values)

        for row in col_values:
            response_text = df.iat[row, col_idx]
            if isinstance(response_text, str) and response_text.strip():
                reply = await chat_with_gpt(response_text, original_prompt)
                print(reply)
                if reply:
                    df.iat[row, col_idx + 1] = reply.strip()

    df.to_excel("true_answering_temp_0.7_You_are_a_helpful_assistant._with_original_prompt.xlsx", index=False)

if __name__ == "__main__":
    asyncio.run(main())
