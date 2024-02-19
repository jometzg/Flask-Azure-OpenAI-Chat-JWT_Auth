import openai
from openai import AzureOpenAI
from dotenv import load_dotenv
import os

# Load the environment variables from .env.local file
load_dotenv(dotenv_path='.env.local')

# Access the variables using os.getenv
azure_api_key = os.getenv('azure_api_key')
azure_endpoint = os.getenv('azure_endpoint')
model = os.getenv('model')
apiVersion = os.getenv('apiVersion')  # Corrected typo

# Initialize Azure OpenAI client
client = AzureOpenAI(
    api_key=azure_api_key,
    azure_endpoint =azure_endpoint,
    api_version=apiVersion  # Corrected typo
)


# system_prompt = """
#     Imagine you're an AI assistant helping sellers understand the benefits of Azure Services. Here's how you can assist:
#     Identify the Core Question: What is the customer asking about? For instance, they might want to know, "What is Azure Application Gateway?"
#     Provide a Direct Answer: Give a straightforward answer to the question. For example, "Azure Application Gateway is a web traffic load balancer that enables you to manage traffic to your web applications."
#     Elaborate on Key Features and Benefits: After answering, delve into the key features, benefits, or use cases. For instance, you could talk about SSL termination, cookie-based session affinity, and URL path-based routing.
#     Address Likely Follow-up Questions: Think about what the customer might ask next and answer those questions. For example, "What are the key benefits of using Azure Application Gateway?"
#     Differentiate from Similar Services: If applicable, compare the service with similar offerings to highlight its unique value. For example, you could explain the difference between Azure Application Gateway and Azure Load Balancer.
#     Include Practical Use Cases: Share scenarios where the service would be particularly beneficial. For example, "Azure Application Gateway is ideal for managing traffic to your web applications."
#     Guide for Complex Queries: If the customer has more complex or technical queries, guide them to consult a technical specialist or refer to Azure documentation.
#     Seller's Perspective: Finally, offer advice from a seller's perspective, focusing on understanding the high-level value and capabilities of the service to communicate its benefits effectively.
#     Remember, as a seller, it's crucial to understand the basic concepts and benefits of Azure Services. However, when the conversation requires in-depth technical knowledge or specific scenario-based advice, it's advisable to involve a technical expert or solutions architect from the team.    
#     Take your time, and remember, the goal is to help the customer understand the value of Azure Services. 
#     When returning the response please format the resposne with markup, please incluce <br><br> at the end of each sentence or for a start of a new paragraph.
#     """


system_prompt = """
    Generate a comprehensive explanation about a specific service or product. Your response should be structured as follows:
    At the end of each section close with <br><br> to separate the sections for readability.
    Introduction: Briefly introduce the service or product.
    Core Question Identification: Identify the core question or topic the explanation will address.
    Direct Answer: Provide a straightforward answer or definition for the service or product.
    Key Features and Benefits: Elaborate on the key features and benefits of the service or product. Highlight what sets it apart and how it adds value.
    Follow-up Questions: Anticipate and answer likely follow-up questions to provide deeper insights into the service or product's value.
    Comparison with Similar Offerings: Compare and contrast the service or product with similar ones in the market, focusing on its unique selling points.
    Practical Use Cases: Describe practical use cases or scenarios where the service or product would be particularly beneficial.
    Guidance for Further Inquiry: Offer guidance on where to find more information or whom to consult for more complex or technical queries regarding the service or product.
    Perspective Advice: From a seller's or provider's perspective, offer advice on understanding and effectively communicating the benefits of the service or product to potential customers.
    Conclusion: Summarize the goal of the explanation, emphasizing the importance of understanding the service or product's value.

    Ensure each section is clearly marked and separated by for readability. 
    The content should be concise, informative, and tailored to assist in understanding and decision-making.
    Take your time with the response, if you do not have the information, please inform the user you are not able to answer fully due to lack of insight, and remember, the goal is to help the customer understand the value of Azure Services.
"""

def generate_streaming_response(user_message):
    print('in generate_streaming_response')        
    try:                
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_prompt},{"role": "user", "content": user_message}],
            temperature=0.9,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6,
            stream=True
        )
        # Iterate over the stream
        for chunk in stream:
            # Check if there are any choices
            if chunk.choices:
                # Access the first `Choice` object
                choice = chunk.choices[0]

                # Access the `ChoiceDelta` object
                choice_delta = choice.delta

                # Access the `content` property
                content = choice_delta.content
                #print(choice)

                # Format the message as a server-sent event
                yield f"data: {content}\n\n"
    except openai.APIConnectionError as e:
        print("The server could not be reached")
        print(e.__cause__)  # an underlying Exception, likely raised within httpx.
    except openai.RateLimitError as e:
        print("A 429 status code was received; we should back off a bit.")
    except openai.APIStatusError as e:
        print("Another non-200-range status code was received")
        print(e.status_code)
        print(e.response)
    except openai.OpenAIError as e:
        print("An error occurred")
    except Exception as e:
        print(e)

        
    
def generate_response(user_message):
    response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": user_message}],
            temperature=0.9,
            top_p=1,
            frequency_penalty=0.0,
            presence_penalty=0.6, 
        )
       
    # Extract the relevant data from the response
    # This is an example, adjust according to your actual response structure
    extracted_data = {
        "response": response.choices[0].message.content,  # Adjust based on actual response structure            
    }
    return extracted_data
