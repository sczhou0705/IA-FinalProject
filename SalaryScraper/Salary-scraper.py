import csv
from time import sleep
import json
import requests
from bs4 import BeautifulSoup
import re

def extract_salary_info(job_title, job_city):
    """The salary website has different url patterns."""
    # URL pattern 1
    template = 'https://www.salary.com/research/salary/posting/{}-salary/{}'

    # Build the url based on search criteria
    url = template.format(job_title, job_city) 
    # print(url)
    
    try:
        response = requests.get(url)
        if response.status_code != 200:
            # URL pattern 2
            template = 'https://www.salary.com/research/salary/alternate/{}-salary/{}'
            url = template.format(job_title, job_city)
            response = requests.get(url)
            if response.status_code != 200:
                # URL pattern 3
                template = 'https://www.salary.com/research/salary/benchmark/{}-salary/{}'
                url = template.format(job_title, job_city)
                response = requests.get(url)
                if response.status_code != 200:
                    return None
    except requests.exceptions.ConnectionError:
        return None
   
    # Parse the html and extract json data
    soup = BeautifulSoup(response.text, 'html.parser')
    pattern = re.compile(r'Occupation')
    script = soup.find('script', {'type': 'application/ld+json'}, text=pattern)
    json_raw = script.contents[0]
    json_data = json.loads(json_raw)

    # Extract salary data
    job_title = json_data['name']
    location = json_data['occupationLocation'][0]['name']
    description = json_data['description']

    ntile_10 = json_data['estimatedSalary'][0]['percentile10']
    ntile_25 = json_data['estimatedSalary'][0]['percentile25']
    ntile_50 = json_data['estimatedSalary'][0]['median']
    ntile_75 = json_data['estimatedSalary'][0]['percentile75']
    ntile_90 = json_data['estimatedSalary'][0]['percentile90']

    data = (job_title, location, description, ntile_10, ntile_25, ntile_50, ntile_75, ntile_90)
    return data

def main():
    job_titles = ['entry-data-analyst','data-scientist-i','machine-learning-engineer','business-intelligence-bi-developer',
              'entry-level-python-developer','ux-design-intern','data-architect-i','big-data-architect',
              'database-administrator-entry','Entry-Business-Systems-Analyst']

    # Get the list of largest us cities.
    # The csv file is saved in salary scraper file.
    with open('largest_cities.csv', newline='') as f:
        reader = csv.reader(f)
        cities = [city for row in reader for city in row]
        #print（cities)
    # Extract salary data for corresponding city
    salary_data = []
    for city in cities:
        for job_title in job_titles:
            result = extract_salary_info(job_title, city)
            if result:
                salary_data.append(result)
                sleep(0.5)
            
    # Save data to csv file
    with open('salary-results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Title','Location', 'Description', 'nTile10', 'nTile25', 'nTile50', 'nTile75', 'nTile90'])
        writer.writerows(salary_data)
        
    return salary_data
    # Call function
main()

