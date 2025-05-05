from openai import OpenAI
from config import API_KEY, API_URL

client = OpenAI(api_key=API_KEY, base_url=API_URL)

response = client.chat.completions.create(
    model="mistralai/mistral-small-3.1-24b-instruct:free",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Make json from picture"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://tvojkomp.ru/wp-content/uploads/2018/02/pokupki-v-magazine-chek.png"
                    }
                }
            ]
        },
        # stream=False
    ]
)

print(response.choices[0].message.content)