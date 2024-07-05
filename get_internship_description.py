from try3 import main as getJobs
import json
import requests
from bs4 import BeautifulSoup
import html
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed


def main():
    """
    Main function to fetch internship job listings and their descriptions,
    then print the results in a pretty JSON format.
    """
    internship = getInternship()
    result = getDescription(internship)
    print(json.dumps(result, indent=4))


def getInternship():
    """
    Fetches job listings and filters them to return only internships.

    Returns:
        list: A list of internship job dictionaries.
    """
    result = getJobs()
    internship = [job for job in result if job['type'] == 'intern']
    return internship


def getDescription(internship):
    """
    Fetches detailed descriptions for each internship job concurrently.

    Args:
        internship (list): A list of internship job dictionaries.

    Returns:
        list: A list of internship job dictionaries with detailed descriptions.
    """
    result = []
    # Create a ThreadPoolExecutor to manage concurrent threads.
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Submit tasks to the executor to fetch job descriptions concurrently.
        future_to_job = {executor.submit(
            getRequest, job): job for job in internship}
        # Iterate over the completed futures as they finish.
        for future in as_completed(future_to_job):
            # Get the job associated with the completed future.
            job = future_to_job[future]
            # Retrieve the result (job description) from the future.
            description = future.result()
            if description:  # Check if the description is not None.
                # Parse the HTML content to plain text.
                description = parseHTML(description)
                # Add the parsed description to the job dictionary.
                job['description'] = description
                # Append the updated job dictionary to the result list.
                result.append(job)
    # Return the list of job dictionaries with detailed descriptions.
    return result


def parseHTML(description):
    """
    Parses HTML content to plain text.

    Args:
        description (str): HTML content as a string.

    Returns:
        str: Plain text extracted from the HTML content.
    """
    soup = BeautifulSoup(description, 'html.parser')
    plain_text = html.unescape(soup.get_text(separator=' '))
    plain_text = unicodedata.normalize('NFKD', plain_text)
    return plain_text


def getRequest(job):
    """
    Makes a GET request to fetch the job description for a given job.

    Args:
        job (dict): A dictionary containing job details, including the job ID.

    Returns:
        str or None: The job description if the request is successful, otherwise None.
    """
    uri = 'https://www.tesla.com/cua-api/careers/job/' + job['id']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS 10.15; rv:124.0)',
        'Accept': "application/json, tex/plain, */*",
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Referer': 'https://www.tesla.com/careers/search',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        "Sec-Fetch-Site": 'same-origin'
    }

    res = requests.get(uri, headers=headers, timeout=2)

    if res.status_code == 200:
        res_str = res.content.decode('utf-8')
        json_data = json.loads(res_str)
        return json_data['jobDescription']
    else:
        print(
            f'Failed to get response from the API for job ID {job["id"]}. Status code: {res.status_code}')
        return None


if __name__ == '__main__':
    main()
