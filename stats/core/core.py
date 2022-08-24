from array import array
from urllib.error import HTTPError
import requests
import math
from stats.core import errors
from stats.core import utils

MAX_PAGE_COUNT = 5
CUSTOM_FILTER = "!)qRpaqDpV9K1pIm65pog"
DEFAULT_URL = "https://api.stackexchange.com/2.3/answers"

def stats(since: int, until: int, development_url=None, custom_filter=None, max_page_count=None, enable_logging=False) -> dict:
    """**Calculates stats**
    The main application method. Makes all calculations and returns 
    the final result.
    
    Args:
        since (int): Stats period start date (timestamp -> milliseconds).
        until (int): Stats period end date (timestamp -> milliseconds).
        development_url (str): If not equals to None, overrides the default Stackexchange API url.
        custom_filter (str):If not equals to None, overrides the default custom filter.
        max_page_count (int): If not equals to None, overrides the default max page permitted count.
        enable_logging (bool): Enables logging with package loguru. Default `False`.

    Returns:
        dict: The final_results in dictionary format.
    ``` json
    {
        "total_accepted_answers": 5,
        "accepted_answers_average_score": 3,
        "average_answers_per_question": 2.3,
        "top_answers_comments_count": {
            "789128198": 1,
            "783482848": 4,
            "789121238": 3,
            "783474818": 6,
            "789112348": 0,
            "324482838": 0,
            "654128198": 9,
            "632482838": 4,
            "712328198": 1,
            "123482838": 0
        }
    }
    ```
    Raises:
        errors.DangerousRemoteData: If data coming from the server can cause unwanted behavior to the user
        ZeroDivisionError: If data is wrong.
    """
    url = development_url if development_url else DEFAULT_URL
    custom_filter = custom_filter if custom_filter else CUSTOM_FILTER
    max_page_count = max_page_count if max_page_count else MAX_PAGE_COUNT

    final_result = {
        "total_accepted_answers": 0,
        "accepted_answers_average_score": 0,
        "average_answers_per_question": 0,
        "top_answers_comments_count": {}
    }
    
    total_answers_per_question = {}
    total_accepted_answers_score = 0
    top_answers_ids = {}
    total_answers = 0
    
    counter = 0
    total_pages_count = 1
    current_page = 1
    
    params = {
        'fromdate': since,
        'todate': until,
        'order': "desc",
        "sort": "activity",
        "site": "stackoverflow",
        "page": 1,
        "pagesize": 100,
        "filter": custom_filter
    }
    
    headers = {'content-type': 'application/json'}
    
    utils.logger("Beginning stats calcutation", enable_logging)

    while True:
        if current_page > total_pages_count:
            break
        params["page"] = current_page
        [result, requested_url, status] = request(url, params, headers)
        
        # On first iteration:
        #   Calculate the total_pages_count and the total results_count
        #   Check if total pages count is smaller or equal to the specified limit
        if counter == 0:
            total_answers = result["total"]
            total_pages_count = math.ceil(result["total"] / result["page_size"])
            if total_pages_count > max_page_count:
                utils.logger(f"Page count to visit, too large! Exiting.", enable_logging, "error")
                raise errors.DangerousRemoteData(f"Dangerous remote data. Max page count is {max_page_count} but got {total_pages_count}.")
 
            utils.logger(f"Total answers {total_answers} for period {since} to {until}", enable_logging)
            utils.logger(f"Total page count to visit {total_pages_count}", enable_logging)
        
        utils.logger(f"Fetched url {requested_url} with status {status}", enable_logging)
        
        [
            total_answers_per_question, 
            top_answers_ids, 
            total_accepted_answers_score,
            final_result["total_accepted_answers"]
        ] = process_results(
                result['items'], 
                total_answers_per_question, 
                top_answers_ids, total_accepted_answers_score,
                final_result["total_accepted_answers"])
                   
        current_page +=1
        counter+=1
   
    try:
        final_result["accepted_answers_average_score"] = total_accepted_answers_score/final_result["total_accepted_answers"]
    except ZeroDivisionError:
        final_result["accepted_answers_average_score"] = 0
        
    try:
        final_result["average_answers_per_question"] = total_answers/len(total_answers_per_question)
    except ZeroDivisionError:
        final_result["average_answers_per_question"] = 0
        
    final_result["top_answers_comments_count"] = calculate_top_answers_comments(top_answers_ids)
    
    utils.logger(f"Total accepted answers: {final_result['total_accepted_answers']}", enable_logging)
    utils.logger(f"Accepted answers average score: {final_result['accepted_answers_average_score']}", enable_logging)
    utils.logger(f"Average answer count per question: {final_result['average_answers_per_question']}", enable_logging)
    utils.logger(f"Top 10 answers comment count: {final_result['top_answers_comments_count']}", enable_logging)

    return final_result

def calculate_top_answers_comments(answers_id: dict) -> dict:
    """**Calculate top answers**
    Args:
        answers_id (dict): keys -> all possible scores values -> array with the answer ids having the specific score.

    Returns:
        result (dict): keys -> answer id, values -> the corresponding answer's comment count.
    """
    scores_sorted = [*answers_id]
    scores_sorted.sort(reverse=True)
    result = {}
    for key in scores_sorted:
        for answer in answers_id[key]:
            if len(result) == 10:
                return result
            
            result[answer["answer"]] = answer["comment_count"]
            
    return result
            
def request(url: str, params: dict, headers: dict) -> array:
    """**Http Client**
    Args:
        url (str): Stackexchange url.
        params (dict): Query parameters.
        headers (dict): Request headers.

    Returns:
        [body, url, status] (array):
            [0] the response body <br/>
            [1] the final url <url+params> <br/>
            [2] response status code <br/>
    
    Raises:
        requests.exceptions.JSONDecodeError: If response cannot be decoded to JSON.
        requests.exceptions.ConnectionError: If server cannot be reached.
        requests.Timeout: If request times out.
        HTTPError: If any error occures during the request. The program terminates with a generic error message.
    """
    try:
        response = requests.get(url, params=params, headers=headers, timeout=8)
    except requests.exceptions.JSONDecodeError as e:
        utils.exit_app(f"Invalid remote data. Error: {e}")
    except requests.exceptions.ConnectionError as e:
        utils.exit_app(f"Server connection error. Error: {e}")
    except requests.Timeout as e:
        utils.exit_app(f"Request timed out with error. Error: {e}")
    except HTTPError as e:
        utils.exit_app(f"Generic HTTP error. Error: {e}")
    return [response.json(), response.url, response.status_code]


def process_results(results: array, tapq: dict, taids: dict, taas: int, taa: int) -> array:
    """**Calculates cases 1-3 of the assignment**
    Args:
        results (dict): Response body->items.
        tapq (dict): Total answers per question.
        taids (dict): Top answers ids.
        taas (int): Total score.
        taa (int): Total accpeted answers.

    Returns:
        [tapq, taids, ts ,taa] (array): 
            [0] Modified top_answers_per_question <br/>
            [1] Modified top_answers_ids <br/>
            [2] Modified total_accepted_answers_score <br/>
            [3] Modified final_result["total_accepted_answers"] <br/>
    """
    for item in results:
        # Basically we only need the length of total_answers_per_question since it's the total questions length  
        tapq[item["question_id"]] = tapq[item["question_id"]] + 1 if item["question_id"] in tapq else 1 # CASE 3 
        
        if item["score"] in taids:
            taids[item['score']].append({"answer": item["answer_id"], "comment_count": item["comment_count"]})
        else:
            taids[item['score']] = [{"answer": item["answer_id"], "comment_count": item["comment_count"]}]
        if item["is_accepted"] == 1:
            taas += item["score"]  # CASE 2
            taa += 1 # CASE 1
    return [tapq, taids, taas ,taa]