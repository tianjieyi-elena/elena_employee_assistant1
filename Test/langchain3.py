from dotenv import load_dotenv, find_dotenv
from langchain.chat_models import init_chat_model

_ = load_dotenv(find_dotenv())

model = init_chat_model("deepseek-chat", model_provider="DeepSeek")

from typing import Optional
from pydantic import BaseModel, Field

class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: Optional[int] = Field(
        default=None, description="How funny the joke is, from 1 to 10"
    )

structured_llm = model.with_structured_output(Joke)

result = structured_llm.invoke("Tell me a joke about programmer")
print(result)