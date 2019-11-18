from bs4 import BeautifulSoup as bs
from random import randint
from time import sleep
from pprint import pprint
import requests

job_title=input("Type the job title you are looking for: ")
pages_number=input("Type the number of pages you would like to get: ")
header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
main_link='https://www.superjob.ru'
jobs_super=[]

full_link = f'{main_link}/vacancy/search/?keywords={job_title}&?geo%5Bc%5D%5B0%5D=1'
html = requests.get(full_link, headers=header)
parsed_html = bs(html.content, 'lxml')

for i in range(0, (int(pages_number))):
    next_button = parsed_html.find('a', {'rel': 'next'})['href']
    next_link = f'{main_link}{next_button}'
    if i!=0:
        html = requests.get(next_link, headers=header)
        parsed_html = bs(html.content, 'lxml')
    else:
        pass

    job_block=parsed_html.find('div',{'style':'display:block'})

    for job in job_block:
        hh_data={}
        #print(job)
        try:
            empty_employer=job.find('a', {'target': '_blank'})
            non_empty_employer = job.find('a', {'target': '_self'})

            job_title = job.find('a').getText()

            if job.find('a')['href'].startswith('/vakansii'):
                job_link=job.find('a')['href']
            else:
                pass

            job_salary= job.find('span',{'class':'_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'}).getText()
            job_salary = job_salary.replace('\xa0', ' ')
            job_salary = job_salary.replace('₽', ' ')

            if job_salary == 'По договорённости':
                salary_from = ''
                salary_to = ''
            elif '—' in job_salary:
                splitted = job_salary.split('-')
                salary_from, salary_to = splitted[0], splitted[1]
            elif 'от' in job_salary:
                salary_from = job_salary.replace('от', '')
                salary_to = ''
            else:
                salary_from = job_salary
                salary_to = job_salary

            hh_data['link']=f'{main_link}{job_link}'
            hh_data['salary_from'] = salary_from.strip()
            hh_data['salary_to'] = salary_to.strip()
            hh_data['title'] = job_title
            if not non_empty_employer.getText:
                hh_data['employer']=''
            else:
                hh_data['employer']=non_empty_employer.getText()
            hh_data['taken_from'] = 'SuperJob'

            jobs_super.append(hh_data)
        except:
            pass

pprint(jobs_super)
