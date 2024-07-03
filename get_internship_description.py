from try3 import main as getJobs
import json
import requests
from bs4 import BeautifulSoup
import html
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed


def main():
    internship = getInternship()
    # print(len(internship))
    result = getDescription(internship)
    # print(json.dumps(result, indent=4))


def getInternship():
    result = getJobs()
    intership = [job for job in result if job['type'] == 'intern']

    return intership


def getDescription(internship):
    # index = 10
    result = []

    # description = getRequest(internship[index])
    # description = parseHTML(description)
    # internship[index]['description'] = description
    # print(json.dumps(internship[index], indent=4))

    for job in internship:
        description = getRequest(job)
        description = parseHTML(description)
        # Add description to job
        job['description'] = description
        result.append(job)

    # for i in range(100):
    #     description = getRequest(internship[i])
    #     description = parseHTML(description)
    #     internship[i]['description'] = description
    #     result.append(internship[i])

    return result


def parseHTML(description):
    # # Parse HTML using BeautifulSoup with 'html.parser'
    # soup = BeautifulSoup(description, 'html.parser')

    # # Use str() to convert the parsed soup object back to a string
    # plain_text = str(soup)

    # # Convert HTML entities to corresponding characters
    # plain_text = html.unescape(plain_text)

    # # Strip any remaining HTML tags
    # plain_text = BeautifulSoup(
    #     plain_text, 'html.parser').get_text(separator=' ')

    # # Replace non-breaking space and other special characters with regular spaces
    # plain_text = unicodedata.normalize(
    #     'NFKD', plain_text)  # Normalize Unicode characters
    # return plain_text

    soup = BeautifulSoup(description, 'html.parser')
    plain_text = html.unescape(soup.get_text(separator=' '))
    plain_text = unicodedata.normalize('NFKD', plain_text)
    return plain_text


def getRequest(job):
    uri = 'https://www.tesla.com/cua-api/careers/job/' + job['id']
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

    res = requests.get(uri, headers=headers, timeout=2)

    if res.status_code == 200:

        # Decodes the response content from bytes to a UTF-8 string
        res_str = res.content.decode('utf-8')

        # Parses the decoded string into a JSON object
        json_data = json.loads(res_str)

        return json_data['jobDescription']
    else:
        print(
            f'Failed to get response from the API for job ID {job["id"]}. Status code: {res.status_code}')
        return None


if __name__ == '__main__':
    main()
