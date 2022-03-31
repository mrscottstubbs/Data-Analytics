import csv
from re import search
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def connect_to_site(search_term):
    base = 'https://www.glassdoor.com/Job/jobs.htm?context=Jobs&clickSource=searchBox&locId=1132200&locT=C&sc.keyword={}'
    search_term = search_term.replace(' ', '+')
    url = base.format(search_term)
    url += '&page{}'
    return url

def get_data(item):
    atag = item.find(class_='jobLink job-search-key-1rd3saf eigr9kq1')
    url = 'https://www.glassdoor.com' + item.find(class_='job-search-key-l2wjgv e1n63ojh0 jobLink').get('href')

    try:
        salary = item.find('span', {'data-test':'detailSalary'}).text.replace('(Glassdoor est.)', '')
        company = item.find(class_='job-search-key-l2wjgv e1n63ojh0 jobLink').text
    except AttributeError:
        return

    try:
        description = atag.span.text
        job_age = item.find('div', {'data-test':'job-age'}).text
        borough = item.find('span', {'class':'css-1buaf54 pr-xxsm job-search-key-iii9i8 e1rrn5ka4'}).text
    except AttributeError:
        description = ' '
        job_age = ' '
        borough = ' '

    result = (company, description, salary, job_age, borough, url)
    return result

def main(search_term):
    driver = webdriver.Chrome('chromedriver/path')
    records =[] 
    url = connect_to_site(search_term)

    for page in range(1,16):
        print("working on page " + str(page))
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        results = soup.find_all('li', {'data-test':'jobListing'})

        for item in results:
            record = get_data(item)
            if record:
                records.append(record)

    driver.close()

    with open(search, 'w', newline='', encoding='utf-8') as f :
        writer = csv.writer(f)
        writer.writerow(['Company', 'Description', 'Salary', 'Job Age', 'Borough', 'URL'])
        writer.writerows(records)

search = input("What Job Title do you want ? ")+' jobs.csv'
main(search)