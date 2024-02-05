**This Project is build on FastAPI**



**Instruction to run the project**

1. Build on python 3.9.
2. Install the requirement in a virtual env preferably
3. Run the main file
4. Clean data.json file
5. Hit the API to get the result.
6. API Description
   ***/word-frequency-analysis***
   Its a POST request. The request body is like this.

   {"topic": "Sachin_Tendulkar","word_count": 10}

** *
    /search-history***

    Its a GET request The query parameter is word_count or we can use the url as
	/api/v1/marvin/assignment/search-history?word_count=10


**Assumption made**

1. For history of past search, we need not to return all relevant words, but can be decided as query parameter
   (word_count). By default its value is 5
2. The recent search topic should come at the top
3. Here to store the data, we have used data format and we are storing it in file. We can also use dedicated table to store the data.
4. There are no restriction on storing the amount of words. But we are returning as much asked in the request.
5. We are returning None in case of not getting any result from wikipedia. And returnning None if there is no data available.
6. We need to omit the irrelevant words like prepostition, verbs, etc. For that, I have mentioned a dict and have included few words. We need to add more such words there to filter out the result.
7. For test case, we are storing the data in the same json file and not deleting. For that we can do this in a different env.
8. data.json file is present always (IMP).


Example of Request and Response (From local server)

***API -: search-history***


Case 1 If data is not present

Request: curl --location 'http://0.0.0.0:5000/api/v1/marvin/assignment/search-history?word_count=10'

Response: None

Case 2 If data is present

Response: {
    "history": [
        {
            "topic": "Sachin_Tendulkar",
            "top_words": {
                "tendulkar": 13,
                "cricket": 11,
                "world": 7,
                "time": 6,
                "s": 5,
                "test": 5,
                "international": 4,
                "team": 4,
                "batsman": 4,
                "match": 4
            }
        }
    ]
}

***API -: word-frequency-analysis***

Request: curl --location 'http://0.0.0.0:5000/api/v1/marvin/assignment/word-frequency-analysis'
--header 'Content-Type: application/json'
--data '{
    "topic": "Sachin_Tendulkar",
    "word_count": 10
}'

Response: {
    "topic": "Sachin_Tendulkar",
    "top_words": {
        "tendulkar": 13,
        "cricket": 11,
        "world": 7,
        "time": 6,
        "s": 5,
        "test": 5,
        "international": 4,
        "team": 4,
        "batsman": 4,
        "match": 4
    }
}
