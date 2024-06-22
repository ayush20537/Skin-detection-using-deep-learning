import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape LinkedIn profiles
def scrape_linkedin_profiles(search_query, num_pages=1):
    base_url = 'https://www.google.com/search?q=site:linkedin.com/in/ AND "{}"'
    profiles = []

    for page in range(num_pages):
        url = base_url.format(search_query)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract LinkedIn profile URLs
        links = soup.find_all('a', {'class': 'BVG0Nb'})
        linkedin_urls = [link['href'] for link in links if 'linkedin.com/in/' in link['href']]

        # Scrape each LinkedIn profile
        for linkedin_url in linkedin_urls:
            profile_data = scrape_profile(linkedin_url)
            profiles.append(profile_data)

    return profiles

# Function to scrape LinkedIn profile
def scrape_profile(linkedin_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(linkedin_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract relevant information from the profile
    name = soup.find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'}).text.strip()
    job_title = soup.find('p', {'class': 'text-body-medium break-words'}).text.strip()
    company = soup.find('ul', {'class': 'pv-text-details_right-panel'}).text.strip() if soup.find('ul', {'class': 'pv-text-details_right-panel'}) else 'None'
    location = soup.find('span', {'class': 'text-body-small inline t-black-light break-words'}).text.strip()

    profile_data = {'Name': name, 'Job Title': job_title, 'Company': company, 'Location': location, 'URL': linkedin_url}
    return profile_data

# Example usage
search_query = 'Python developer'
num_pages = 1
profiles = scrape_linkedin_profiles(search_query, num_pages)

# Create a DataFrame from the collected data and save to Excel
df = pd.DataFrame(profiles)
df.to_excel('Linkedin_profiles.xlsx', index=False)
