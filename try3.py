
import requests
import json

"""
This function sends a GET request to a specified URI to retrieve job listings data in JSON format. It then decodes the JSON response, extracts relevant information such as listings, departments, locations, and types, and passes them to the 'decoded_jobs' function for further processing. Finally, it prints the decoded job information in a formatted JSON string.

Returns:
    None
"""


def main():
    # main url
    uri = 'https://www.tesla.com/cua-api/apps/careers/state'

    # Separate these dict to "reduce" search up time
    listings = {}
    departments = {}
    locations = {}
    types = {}

    headers = {
        # Identifies the client software initiating the request
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS 10.15; rv:124.0)',
        # Specifies the media types that are acceptable for the response
        'Accept': "application/json, tex/plain, */*",
        # Indicates the preferred languages for the response
        'Accept-Language': 'en-US,en;q=0.5',
        # Instructs the server to maintain the connection for multiple requests
        'Connection': 'keep-alive',
        # Provides the URL of the referring page
        'Referer': 'https://www.tesla.com/careers/search',
        # Indicates the destination of the fetch request (e.g., document, image)
        'Sec-Fetch-Dest': 'empty',
        # Specifies the mode of the fetch request (e.g., cors, no-cors)
        'Sec-Fetch-Mode': 'cors',
        # Indicates the relationship between the origin of the request initiator and the request destination
        "Sec-Fetch-Site": 'same-origin'
    }

    res = requests.get(uri, headers=headers, timeout=10)
    if res.status_code == 200:

        # Decodes the response content from bytes to a UTF-8 string
        res_str = res.content.decode('utf-8')

        # Parses the decoded string into a JSON object
        json_data = json.loads(res_str)

        # Loads dicts
        listings = json_data['listings']
        departments = json_data['lookup']['departments']
        locations = json_data['lookup']['locations']
        types = json_data['lookup']['types']

        # Parse listed jobs and pretty print it
        result = decoded_jobs(listings, departments, locations, types)
        # print(json.dumps(result, indent=4))
        return result

    else:
        print('Failed to get response from the API.')


def decoded_jobs(listings, departments, locations, types):
    """
    Decode the job listings by extracting relevant information such as id, title, department, location, and type.

    Parameters:
    - listings (list): A list of job listings to be decoded.
    - departments (dict): A dictionary mapping department codes to department names.
    - locations (dict): A dictionary mapping location codes to location names.
    - types (dict): A dictionary mapping type codes to type names.

    Returns:
    - list: A list of dictionaries, where each dictionary represents a decoded job listing with keys 'id', 'title', 'department', 'location', and  type'.
    """
    result = []
    for job in listings:
        decoded_job = {
            "id": getId(job),
            'title': getTitle(job),
            'department': getDepartment(job, departments),
            'location': getLocations(job, locations),
            'type': getTypes(job, types)
        }
        result.append(decoded_job)
    return result


def getId(job):
    """
    Retrieve the job ID from a job listing.

    Parameters:
    - job (dict): A dictionary representing a job listing.

    Returns:
    - str: The job ID if it exists in the job dictionary, otherwise 'Updated required...'.
    """
    return job['id'] if ('id' in job) else 'Updated required...'


def getTitle(job):
    """
    Retrieve the job title from a job listing.

    Parameters:
    - job (dict): A dictionary representing a job listing.

    Returns:
    - str: The job title if it exists in the job dictionary, otherwise 'Updated required...'.
    """
    return job['t'] if ('t' in job) else 'Updated required...'


def getDepartment(job, departments):
    """
    Retrieve the department name from a job listing.

    Parameters:
    - job (dict): A dictionary representing a job listing.
    - departments (dict): A dictionary mapping department codes to department names.

    Returns:
    - str: The department name if it exists in the job dictionary and is found in the departments dictionary, otherwise 'Updated required....'.
    """
    if 'dp' in job:
        if job['dp'] in departments:
            return departments[job['dp']]
    return 'Updated required....'


def getLocations(job, locations):
    """
    Retrieve the location name from a job listing.

    Parameters:
    - job (dict): A dictionary representing a job listing.
    - locations (dict): A dictionary mapping location codes to location names.

    Returns:
    - str: The location name if it exists in the job dictionary and is found in the locations dictionary, otherwise 'Updated required....'.
    """
    if 'l' in job:
        if job['l'] in locations:
            return locations[job['l']]
    return 'Updated required....'


def getTypes(job, types):
    """
    Retrieve the type name from a job listing.

    Parameters:
    - job (dict): A dictionary representing a job listing.
    - types (dict): A dictionary mapping type codes to type names.

    Returns:
    - str: The type name if it exists in the job dictionary and is found in the type dictionary, otherwise 'Updated required....'.
    """
    if 'y' in job:
        if str(job['y']) in types:
            return types[str(job['y'])]
    return 'Updated required....'


if __name__ == "__main__":
    main()
