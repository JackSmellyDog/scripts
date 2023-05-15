import requests
from bs4 import BeautifulSoup

BASE_URL = 'https://petition.president.gov.ua'


def build_petition_url(base_url, status, sort, order):
    return f'{base_url}/?status={status}&sort={sort}&order={order}'


def scrape_petitions(url, base_url=BASE_URL):
    # Send a GET request to the website
    response = requests.get(url)

    # Parse the HTML content of the website using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all the links to the petitions
    links = soup.find_all('a', class_='pet_link')

    # Create an empty list to store the petition data
    petition_data = []

    # Loop through each link and extract its data
    for link in links:
        # Extract the petition title

        href = link.get('href')
        full_href = f'{base_url}/{href}'
        title = link.text.strip()

        # Append the petition data to the list
        petition_data.append({'title': title, 'href': full_href})

    # Return the list of petitions sorted by number of votes (in descending order)
    return petition_data


if __name__ == '__main__':
    # Build a URL for active petitions sorted by number of votes (in descending order)
    url = build_petition_url(BASE_URL, 'active', 'votes', 'desc')

    # Scrape the list of petitions from the website
    petitions = scrape_petitions(url)

    # Print the list of petitions
    for petition in petitions:
        print(petition['title'] + ' ' + petition['href'])
