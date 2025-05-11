from openai import AsyncOpenAI
from config import API_KEY, API_URL
import base64

client = AsyncOpenAI(api_key=API_KEY, base_url=API_URL)

async def ai_generate(text: str, image_path: str = None):
    default_text = '. Cделай ТОЛЬКО json текст из данной картинки, ничего добавлять к ответу не нужно'
    response = await client.chat.completions.create(
        model="mistralai/mistral-small-3.1-24b-instruct:free",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (text + default_text) if text else default_text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://tvojkomp.ru/wp-content/uploads/2018/02/pokupki-v-magazine-chek.png"
                        }
                    }
                ]
            }
        ]
    )
    print(response)
    return response.choices[0].message.content

