import markdown
from openai import AzureOpenAI
import json

# Replace with your Azure OpenAI credentials
azure_api_key = ""
azure_endpoint = ""
api_verison = ""
model = ""
# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=azure_api_key,
    azure_endpoint=azure_endpoint,
    api_version=api_verison
)


def generate_response(user_message):
    """ Generator function to yield streaming chat responses from Azure OpenAI. """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": user_message}],
            temperature=0.9,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
        )
        # Extracting relevant data from the Choice object, convert markdown to html
        html_response = markdown.markdown(response.choices[0].message.content)
        return html_response        
        
    except Exception as e:
        return str(e)
