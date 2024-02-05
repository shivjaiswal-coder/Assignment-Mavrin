from pydantic import BaseModel, Field, validator

# Request body mention here
class WikipediaTopicRequest(BaseModel):
    topic: str
    word_count: int
    
#Response body mention here
class WikipediaTopicResponse(BaseModel):
    topic: str
    top_words: dict


class WikipediaTopicPastHistoryResponse(BaseModel):
    history: list[WikipediaTopicResponse]