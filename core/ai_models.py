import google.generativeai as genai
from openai import OpenAI
import os
from mistralai import Mistral
import cohere
from groq import Groq
# Load environment variables

#OPENAI
gpt_client = OpenAI()
OPENAI_API_KEY  = os.getenv('OPENAI_API_KEY')



#Gemini Api Key
Gemini_api_key=os.getenv("GOOGLE_API_KEY")
#MISTRAL
MISTRAL_api_key = os.getenv("MISTRAL_API_KEY")
mist_client = Mistral(api_key=MISTRAL_api_key)


#COHERE
CO_API_KEY=os.getenv("CO_API_KEY")
co = cohere.ClientV2(api_key=CO_API_KEY)

#llama
groq_client = Groq(
            api_key=os.environ.get("GROQ_API_KEY"),
        )





# OpenAI GPT-4o-mini
def gpt(query):
    try:
        response = gpt_client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        response_text = response.choices[0].message.content
        return response_text
    except Exception as e:
        return f"An error occurred: {e}"
        

# Gemini
def gem(query):
    try:
        genai.configure(api_key=Gemini_api_key)
        model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
        response = model.generate_content(query)
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"



    

#MISTRAL
def mist(query):
    try:
     chat_response = mist_client.chat.complete(
    model = "pixtral-12b-2409",
    messages = [
        {
            "role": "user",
            "content": query,
        },
    ]
)
     return chat_response.choices[0].message.content
    except Exception as e:
        return f"An error occurred: {e}"



#LLAMA
def llama(query):
    try:
        chat_completion = groq_client.chat.completions.create(
        messages=[
          {
            "role": "user",
            "content": query,
            }
         ],
         model="llama-3.3-70b-versatile",
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
     print(f"An error occurred: {e}")
     return f"An error occurred: {e}"
    




# Compare responses from different AI models
#final_response = gem(f"Compare these 4 responses from 4 different AIs and just tell me which one is best. Also assign a score out of 10 to each response based on Accuracy, Relevance, Clarity, Depth. Answer in short: {gpt_response}, {gemini_response}, {mist_response} , {llama_response}")


def compare_responses(gpt_response, gemini_response, mist_response ,  llama_response):
    try: 
        prompt=f"Compare these responses from different AIs and just tell me which one is best. Also assign a score out of 10 to each response based on Accuracy, Relevance, Clarity, Depth. Answer in short: {gpt_response}, {gemini_response}, {mist_response} , {llama_response}"
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel("gemini-2.5-flash-preview-05-20")
        response = model.generate_content(prompt)
        return response.text
    

    except Exception as e:
        return f"Error comparing responses: {e}"