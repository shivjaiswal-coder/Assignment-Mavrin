from fastapi.routing import APIRouter
from service import fetch_and_process_wikipedia_data, get_history
from schema import WikipediaTopicRequest, WikipediaTopicResponse, WikipediaTopicPastHistoryResponse
from typing import Union

# endpoint branching from here for this module
router = APIRouter(prefix="/api/v1/marvin/assignment")

@router.post("/word-frequency-analysis", response_model=Union[WikipediaTopicResponse, None])
async def process_wikipedia_data(request: WikipediaTopicRequest):
    
    """API to fetch topic detail from wikipedia. Process it and store relevant word count in a json file


    Args:
        reuest: WikipediaTopicRequest (topic and relevant word count)
        {
            topic: str
            word_count: int
        }
    Return: Dict (topic and relevant words with count)

    """ 
    
    response = fetch_and_process_wikipedia_data(request.topic, request.word_count)
    return response


@router.get("/search-history", response_model=Union[WikipediaTopicPastHistoryResponse, None])
def get_past_search_history(word_count: int = 5):
    """API to fetch all the history of past search

    Args: 
        result_count: A query parameter just to filter the result length

    Return: Dict (All topic and relevant words with count). By default it resturn top 5 relevant words. But can ne changed as query parameter.

    """
    response = get_history(word_count)
    return response