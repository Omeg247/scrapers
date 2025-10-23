#This is a sample web scraping script
#That gets the response of a url e.g https://example.com/hotels?page=1
#Scrapes certain data found in <a> tags e.g <a href="https://example.com/hotels/hotelsample">
#Saves "hotelsample" into a text file.

import requests
from bs4 import BeautifulSoup

base_url = "https://example.com/hotels?page={}"
headers = {
    "Cookie": "cookies_here",  #Replace with your cookie data
}

#File to store the scraped data
output_file = "scraped_data.txt"

with open(output_file, "w") as file:
    total_entries = 0

    for page in range(1, 11):
        #Inserting page number into base_url
        url = base_url.format(page)
        print(f"Scraping page {page}...")

        response = requests.get(url, headers=headers)

        # Check for a successful response
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            
            #Goal: Find all <a> tags with the required href structure
            links = soup.find_all("a", href=True)

            #Extract and save data from the current page
            for link in links:
                href = link["href"]
                if "https://example.com/hotels/" in href:
                    #Extract data between "/hotels/" and the closing tag ">"
                    data_to_be_scraped = href.split("/hotels/")[-1]
                    file.write(data_to_be_scraped + "\n")
                    total_entries += 1
        else:
            print(f"Failed to scrape page {page}. Status code: {response.status_code}")

print(f"Scraping complete. {total_entries} entries saved to '{output_file}'.")
