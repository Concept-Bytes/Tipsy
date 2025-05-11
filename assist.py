import json
from pydantic import BaseModel
import os
from openai import OpenAI, OpenAIError


def get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise OpenAIError("The api_key client option must be set either by passing api_key to the client or by setting the OPENAI_API_KEY environment variable")
    return OpenAI(api_key=api_key)

# Pydantic models for documentation
class Cocktail(BaseModel):
    normal_name: str
    fun_name: str
    ingredients: dict

class CocktailResponse(BaseModel):
    cocktails: list[Cocktail]

def generate_cocktails(pump_to_drink: dict, requests_for_bartender: str = "", exclude_existing: bool = True) -> dict:
    prompt = (
        "You are a creative cocktail mixologist. Based on the following pump configuration, "
        "generate a list of cocktail recipes. For each cocktail, provide a normal cocktail name, "
        "a fun cocktail name, and a dictionary of ingredients (with their measurements, e.g., '2 oz').\n\n"
        "Please output only valid JSON that follows this format:\n\n"
        '{\n'
        '  "cocktails": [\n'
        "    {\n"
        '      "normal_name": "Margarita",\n'
        '      "fun_name": "Citrus Snap",\n'
        '      "ingredients": {\n'
        '        "Tequila": "2 oz",\n'
        '        "Triple Sec": "1 oz",\n'
        '        "Lime Juice": "1 oz"\n'
        "      }\n"
        "    }\n"
        "  ]\n"
        "}\n\n"
        "Now, use the following pump configuration creatively to generate your cocktail recipes:\n"
        f"{json.dumps(pump_to_drink, indent=2)}\n\n"
        "Also include each type of liquor available as it's own drink, served neat with the normal cocktail name being the name of the liquor\n\n"
    )
    if exclude_existing:
        from helpers import load_cocktails
        prompt += (
            "Do not include the following cocktails, which I already have recipes for:\n\n"
            f"{json.dumps(load_cocktails(), indent=2)}\n\n"
        )

    if requests_for_bartender.strip():
        prompt += f"Requests for the bartender: {requests_for_bartender.strip()}\n"

    try:
        client = get_client()
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a creative cocktail mixologist. Generate cocktail recipes in JSON format. "
                        "Make sure your entire response is a valid JSON object."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
        )
        json_output = completion.choices[0].message.content
        data = json.loads(json_output)
        return data
    except Exception as e:
        return {"error": str(e)}

def generate_image(prompt: str) -> str:
    try:
        client = get_client()
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        return image_url
    except Exception as e:
        raise Exception(f"Image generation error: {e}")
