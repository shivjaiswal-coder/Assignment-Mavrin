import requests
from collections import Counter
import re
import json
from fastapi.responses import JSONResponse
import random
from schema import WikipediaTopicRequest, WikipediaTopicResponse, WikipediaTopicPastHistoryResponse

#This is important. We should omit non relevant words including html code as much as we can. Just mention here
word_to_omit = {
    'the', 'is', 'are', 'am', 'on', 'and', 'in', 'it', 'with', 'for', 'as', 'of', 'to', 'an', 'at',
    'I', 'you', 'he', 'she', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
    'my', 'your', 'his', 'its', 'our', 'their',
    'mine', 'yours', 'hers', 'ours', 'theirs',
    'this', 'that', 'these', 'those',
    'a', 'an', 'some', 'any', 'each', 'every', 'all',
    'be', 'been', 'being',
    'have', 'has', 'had',
    'do', 'does', 'did',
    'will', 'would', 'shall', 'should', 'can', 'could', 'may', 'might', 'must',
    'was', 'were', 'been',
    'there', 'here',
    'now', 'then',
    'when', 'where', 'how', 'why',
    'am', 'is', 'are', 'was', 'were', 'be', 'been',
    'can', 'could', 'will', 'would', 'shall', 'should',
    'do', 'does', 'did', 'have', 'has', 'had', 'may', 'might', 'must',
    'p', 'b', 'n', 'while', 'where', 'a', 'i', 'the', 'is', 'are', 'am', 'on', 'and', 'in', 'it', 'with',
    'for', 'as', 'of', 'to', 'an', 'at', 'p', 'b', 'n', 'while', 'where', 'a', 'i', 'but', 'may', 'over',
    'can', 'who', 'used', 'also', 'about', 'which', 'when',
    'based', 'or', 'used', 'use', 'uses',
    'span', 'style', 'link', 'alt'
}

def fetch_wikipedia_data(topic: str):

    """A function to fetch topic data from Wikipedia

    Args:
        topic (str): topic of the search

    Returns:
        _type_: HTML text 
    """

    base_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": topic,
        "prop": "extracts",
        "exintro": True
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    try:
        page = next(iter(data["query"]["pages"].values()))
        # HTML Text containign some html tags. We need to filter out
        return page["extract"]
    except Exception as e:
        return None

def count_word_frequency(text):
    """A function to count the word frequency

    Args:
        text (_type_): HTML text 

    Returns:
        _type_: dict of word vs frequency
    """
    #Regex to match the word
    words = re.findall(r'\b\w+\b', text.lower())
    # filtering out the irrelevant words
    filtered_words = [word for word in words if word not in word_to_omit]
    #Couting the word frequency and converting into a dict
    return Counter(filtered_words)

def fetch_and_process_wikipedia_data(topic: str, word_count: int):
    """A function to get the data from wikipedia, process and store it as a json file.

    Args:
        topic (str): topic of the search
        word_count (int): no of word to return

    Returns:
        _type_: Json object containing topic and word vs count result
    """
    result = fetch_wikipedia_data(topic)
    if not result:
        # If no result is fetch, return None
        return None
    word_with_frequency = count_word_frequency(result)
    sorted_word_count = dict(sorted(word_with_frequency.items(), key=lambda item: item[1], reverse=True))

    # Save the word count in a JSON file (data.json)
    existing_data = {}
    try:
        with open('data.json', 'r') as json_file:
            existing_data = json.load(json_file)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        pass

    existing_data[topic] = sorted_word_count

    # The latest search result should be on the top

    with open('data.json', 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)

    top_words = dict(list(sorted_word_count.items())[:min(len(sorted_word_count), word_count)])

    return WikipediaTopicResponse(
        topic=topic,
        top_words=top_words
    )


def get_history(word_count: int):
    """A function to get all the past history result

    Args:
        word_count (int): A query parameter to get the lenght of top relevant words

    Returns:
        _type_: Json object representing all topic and its result
    """
    existing_data = {}
    try:
        with open('data.json', 'r') as json_file:
            existing_data = json.load(json_file)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        pass
    if not existing_data:
        return None
    
    # reverse the data to return the recent search at top
    existing_data = {k: v for k, v in reversed(list(existing_data.items()))}

    history = []
    for key, value in existing_data.items():
        history.append({"topic": key, "top_words":dict(list(value.items())[:min(len(value), word_count)])})
        
    return WikipediaTopicPastHistoryResponse(
        history=history
    )
