import requests
from requests.auth import HTTPBasicAuth
from typing import Literal
import time


def get_jira_api_auth(email: str, api_token: str) -> HTTPBasicAuth:
    """Uses HTTPBasicAuth to create an authentication object"""
    return HTTPBasicAuth(email, api_token)


def run_request_with_error_handling(method: Literal['POST', 'GET'], url: str, headers: dict, params: dict,
                                    auth: HTTPBasicAuth, num_tries_if_error: int = 25, timeout_secs: int = 15) -> dict:
    """
    Runs a request with an error handling loop.
    Handles both GET and POST requests.

    :param method: The request method, can be one of: GET or POST
    :param url: The url of the request
    :param headers: The request headers
    :param params: The request body/ parameters
    :param auth: The authentication object
    :param num_tries_if_error: The number of tries the function will use for consecutive fails
    :param timeout_secs: The timeout for the request, if the number of seconds here reached, the code will stop the request

    :return: The data received back from the api as JSON
    """
    request_dict = {
        "method": method,
        "url": url,
        "headers": headers,
        "auth": auth,
        "timeout": timeout_secs
    }

    if method == 'POST':
        request_dict['json'] = params
    else:
        request_dict['params'] = params

    for i in range(num_tries_if_error):
        try:
            response = requests.request(**request_dict)
            if response.status_code == 429:
                retry_time = response.headers.get("Retry-After")
                if retry_time:
                    print(f"Rate limit exceeded. Sleeping {retry_time} seconds")
                    time.sleep(int(retry_time))
                else:
                    print("Rate limit exceeded")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Print the exact response body if available for easier debugging
            print(f"❌ API Error during fetch: {e}")
            try:
                print(f"Response body: {response.text}")
            except:
                pass
            if i == num_tries_if_error - 1:
                raise Exception(f"API failed too many times in a row ({num_tries_if_error})")
