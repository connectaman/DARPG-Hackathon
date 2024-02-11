import requests 
from urllib import request
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from functools import lru_cache

@lru_cache
def scrape_faq_from_pgportal(url):
    """
    Scrapes the FAQ from the given PGPortal URL.

    Args:
        url (str): The URL of the PGPortal.

    Returns:
        list: A list of dictionaries containing FAQ question and answer pairs.
            Each dictionary has a "text" key with the formatted FAQ pair.
    """
    # Fetch HTML content
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch the content from {url}. Status code: {response.status_code}")
        return None

    # Parse HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all FAQ card elements
    faq_cards = soup.find_all('div', class_='card card-light mt-2')

    # Store FAQ question and answer pairs
    faq_list = []

    # Iterate through each FAQ card
    for faq_card in faq_cards:
        # Extract question and answer
        question_element = faq_card.find('a', class_='text-primary')
        answer_element = faq_card.find('div', class_='card-body')

        if question_element and answer_element:
            question = question_element.get_text(strip=True)
            answer = answer_element.get_text(strip=True)

            # Format the FAQ pair
            faq_pair = "Question: {}\nAnswer: {}".format(question[2:].strip(), answer)
            faq_list.append({"text": faq_pair})

    return faq_list

@lru_cache
def scrape_table_with_pagination(url):
    """
    Scrapes a table from a given URL with pagination support.
    
    Args:
        url (str): The URL of the page containing the table.
        
    Returns:
        list: A list of contact information extracted from the table.
    """
    contact_infos = []
    
    while url:
        # Send an HTTP GET request to the URL
        response = requests.get(url)
        
        if response.status_code != 200:
            # If the request fails, print an error message and return None
            print(f"Failed to fetch the page. Status code: {response.status_code}")
            return None
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Call a function to extract and process the table data
        contact_infos.extend(extract_table_data(soup))
        
        # Check if there is a next page link
        next_page_link = soup.find('li', class_='paginate_button next')
        
        if next_page_link:
            # If a next page link is found, update the URL and continue scraping
            next_page_url = next_page_link.find('a')['href']
            url = urljoin(url, next_page_url)
        else:
            # If no next page link is found, exit the loop
            url = None
    
    return contact_infos

@lru_cache
def extract_table_data(soup):
    """
    Extracts data from an HTML table and returns a list of dictionaries containing the extracted data.

    Args:
        soup (bs4.BeautifulSoup): The BeautifulSoup object representing the HTML.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row in the table.
    """
    # Identify the HTML elements containing the table data
    table = soup.find('table')

    if table:
        table_extracts = []
        # Extract and process the table data
        rows = table.find_all('tr')
        headers = [col.text.strip() for col in rows[0].find_all(['th'])]

        for row in rows[1:]:
            columns = row.find_all(['td', 'th'])
            row_data = {headers[i]: col.text.strip() for i, col in enumerate(columns)}
            text = ""
            for k,v in row_data.items():
                text += f" {k} : {v} \n"

            table_extracts.append({
                "text": text
            })

            return table_extracts
    else:
        return []

@lru_cache
def scrape_about_paragraphs(url):
    """
    Scrape the paragraphs from the given URL.

    Args:
        url (str): The URL to scrape.

    Returns:
        list: A list of paragraphs extracted from the URL.

    Raises:
        requests.exceptions.RequestException: If there is an error fetching the URL.
    """

    try:
        # Fetch the HTML content of the URL
        response = requests.get(url)
        response.raise_for_status()

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the div tag with class "card-body"
        card_body_div = soup.find('div', class_='card-body')

        # If the div is found, find all the p tags inside it
        if card_body_div:
            p_tags = card_body_div.find_all('p')

            # Extract the text content of each p tag and store in a list
            paragraphs = [p.get_text().strip() for p in p_tags]

            return paragraphs
        else:
            print('No div with class "card-body" found on the page.')
            return []

    except requests.exceptions.RequestException as e:
        print(f'Error fetching the URL: {e}')
        return []


# Example usage
# print(scrape_table_with_pagination(url="https://pgportal.gov.in/Home/NodalPgOfficers"))
# print(scrape_table_with_pagination(url="https://pgportal.gov.in/Home/NodalPgOfficersState"))
# print(scrape_table_with_pagination(url="https://pgportal.gov.in/Home/NodalAuthorityForAppeal"))


#print(scrape_faq_from_pgportal(url='https://pgportal.gov.in/Home/Faq'))
    

# print(scrape_about_paragraphs(url="https://pgportal.gov.in/Home/AboutUs"))