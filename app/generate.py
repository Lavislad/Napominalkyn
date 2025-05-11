from openai import AsyncOpenAI
from config import API_KEY, API_URL
import base64

client = AsyncOpenAI(api_key=API_KEY, base_url=API_URL)

async def ai_generate(text: str, image_path: str = None):
    default_text = '. Cделай ТОЛЬКО json текст из данной картинки, ничего добавлять к ответу не нужно'

    content = [{
        "type": "text",
        "text": (text + default_text) if text else default_text
    }]

    if image_path:
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')

        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })
    else:
        pass

    response = await client.chat.completions.create(
        model="mistralai/mistral-small-3.1-24b-instruct:free",
        messages=[
            {
                "role": "user",
                "content": content
            }
        ]
    )
    print(response)
    return response.choices[0].message.content

