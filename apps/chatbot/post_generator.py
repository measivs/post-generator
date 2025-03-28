from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import os


llm = OpenAI(
    model="gpt-3.5-turbo-instruct",
    temperature=0.7,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

post_generation_prompt = """
Generate a {platform} post about: {topic}
IGNORE phrases like "I want about" or "hmm".
Key Requirements:
- LinkedIn: Professional, 300-500 chars
- Instagram: Casual + emojis
- Twitter: <280 chars
- Facebook: Friendly tone

Post Content:
"""

prompt = PromptTemplate(
    input_variables=["topic", "platform"],
    template=post_generation_prompt
)
llm_chain = LLMChain(llm=llm, prompt=prompt)


def generate_response(topic: str, platform: str) -> str:
    """Generates post while preserving raw inputs"""
    try:
        return llm_chain.run(topic=topic, platform=platform)
    except Exception as e:
        return f"Failed to generate post: {str(e)}"
    