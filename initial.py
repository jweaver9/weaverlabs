import requests
import os
import json

# Define your helper functions as before
def sanitize_filename(title):
    invalid = '<>:"/\\|?*'
    for char in invalid:
        title = title.replace(char, '_')
    return title[:50]  # Truncate long titles to ensure they fit as filenames

def download_article_details(identifier, api_key, output_folder):
    download_url = f"https://api.core.ac.uk/v3/outputs/{identifier}?api_key={api_key}"
    response = requests.get(download_url)
    if response.status_code == 200:
        data = response.json()
        title = sanitize_filename(data.get("title", "NoTitle"))
        file_path = os.path.join(output_folder, f"{title}_{identifier}.json")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Article {identifier} saved to {file_path}")
    else:
        print(f"Failed to download article {identifier}, status code: {response.status_code}")

# Function to cycle through each search term and download related articles
def search_and_download_each_term(api_key, search_terms, output_folder):
    os.makedirs(output_folder, exist_ok=True)  # Ensure the output directory exists
    entityType = 'outputs'

    for term in search_terms.split(", "):  # Split the search query string into individual terms
        print(f"Searching for: {term}")
        search_url = f"https://api.core.ac.uk/v3/search/{entityType}?api_key={api_key}&q={term}&limit=100"
        response = requests.get(search_url)
        
        if response.status_code == 200:
            results = response.json().get('results', [])
            print(f"Found {len(results)} articles for '{term}'.")
            for article in results:
                identifier = article.get('id')
                if identifier:
                    download_article_details(identifier, api_key, output_folder)
        else:
            print(f"Failed to search for term '{term}', status code: {response.status_code}")

# Define your API key and search terms
api_key = 'gxvHozSQWOcn7wPsMI1KJl2mVdkZTADU'
search_terms = "Cultural influences on LGBTQ+ rights, LGBTQ+ activism impact analysis, Community-driven LGBTQ+ initiatives, Policy effects on transgender rights, LGBTQ+ narratives in media, Queer theory and social change, Historical trends in LGBTQ+ acceptance, LGBTQ+ representation in politics, Economic effects of LGBTQ+ discrimination, LGBTQ+ and racial intersectionality, Gender identity recognition laws, Sexual orientation discrimination studies, LGBTQ+ families and societal acceptance, Public opinion on LGBTQ+ rights, LGBTQ+ advocacy and legal challenges, Social determinants of LGBTQ+ health, LGBTQ+ individuals in sports, Queer spaces and community safety, LGBTQ+ aging and societal support, Education policies and LGBTQ+ students, LGBTQ+ experiences in rural vs. urban areas, Impact of technology on LGBTQ+ connections, LGBTQ+ refugees and asylum seekers, Intersection of LGBTQ+ rights and disability, LGBTQ+ veterans and military policies, Global influences on US LGBTQ+ acceptance"

# Specify the output folder
output_folder = './seed_data_1'

# Execute the search and download process
search_and_download_each_term(api_key, search_terms, output_folder)
