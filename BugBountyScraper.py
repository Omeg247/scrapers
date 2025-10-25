import requests
from tabulate import tabulate

def scrape_bugcrowd_programs():
    url_1 = "https://bugcrowd.com/engagements.json?category=bug_bounty&sort_by=starts&sort_direction=desc&page=1"
    url_2 = "https://bugcrowd.com/engagements.json?category=bug_bounty&page=1&rewards_amount=20000&rewards_operator=gte&rewards_priority=all&sort_by=promoted&sort_direction=desc"

    print("BUGCROWD BUG BOUNTY TABLE")
    print("Select Sorting Format")
    sorting = str(input("1. Most Recent Programs\n2. Highest Payouts($20,000+)\n: "))
    if sorting == '1':
        try:
            print(  "Loading Table...............")
            response = requests.get(url_1, timeout=15)
            response.raise_for_status()
            data = response.json()
        #Catching errors
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return
    elif sorting == '2':
        try:
            print(  "Loading Table...............")
            response = requests.get(url_2, timeout=15)
            response.raise_for_status()
            data = response.json()
        #Catching errors
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return
    else:
        print("Invalid input!!!")
        exit()        

    #Getting engagements data
    programs_list = []
    if isinstance(data, dict):
        programs_list = data.get('engagements')
    elif isinstance(data, list):
        programs_list = data

    if not programs_list:
        print("Error: Could not find the list of bug bounty programs in the JSON response.")
        return

    #Extractig data from different keys
    extracted_data = []
    for program in programs_list:
        name = program.get('name')
        tagline = program.get('tagline')
        industry_name = program.get('industryName')
        brief_url = program.get('briefUrl')
        reward_summary = program.get('rewardSummary', {})
        summary = reward_summary.get('summary')
        compensation = reward_summary.get('compensationSummary')
        product_type = program.get('productEngagementType', {})
        label = product_type.get('label')
       

        #Adding brief url to main url
        if brief_url: 
            if not brief_url.startswith('http'):
                brief_url = f"https://bugcrowd.com{brief_url}"
       

        final_row = [name, tagline, label, industry_name, summary, compensation, brief_url]
        cleaned_row = []
        for v in final_row:
            if v is None:
                cleaned_row.append('N/A')
            elif isinstance(v, str):
                cleaned_row.append(v.strip())
            else:
                cleaned_row.append(v)

        extracted_data.append(cleaned_row)

    #Tabulating
    headers = [
        'Name',
        'Tagline',
        'Label',
        'Industry Name',
        'Summary',
        'Compensation',
        'Brief URL'
    ]

    print(tabulate(
        extracted_data,
        headers=headers,
        tablefmt="fancy_grid",
        #Adjust according to screen size
        maxcolwidths=[25, 30, 15, 15, 15, 15, 50]
    ))

if __name__ == "__main__":
    scrape_bugcrowd_programs()