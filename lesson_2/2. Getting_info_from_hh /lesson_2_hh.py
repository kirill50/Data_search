from bs4 import BeautifulSoup as bs
from random import randint
from time import sleep
from pprint import pprint
import requests

header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}

job_title=input("Type the job title you are looking for: ")
l = job_title.split()
prepared_job_title = '+'.join(l)

pages_number=input("Type the number of pages you would like to get: ")

main_link='https://hh.ru/'
jobs_hh=[]

for i in range(0, (int(pages_number))):
    full_link=f'{main_link}search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text={prepared_job_title}&page={str(i)}'
    html=requests.get(full_link, headers=header)
    parsed_html=bs(html.content,'lxml')

    job_block=parsed_html.find('div',{'data-qa':'vacancy-serp__vacancy'}).find_parent()
    #pprint(job_block.find_parent())

    for job in job_block:
        hh_data={}
        job_list=job.find('a',{'class':'bloko-link HH-LinkModifier'})
        #pprint(job_list)
        try:
            job_title=job_list.getText()

            job_salary=job.find('div',{'class':'vacancy-serp-item__sidebar'}).getText()
            job_salary=job_salary.replace('\xa0', ' ')
            job_salary = job_salary.replace('руб.', ' ')

            if job_salary=='':
                salary_from=''
                salary_to=''
            elif '-' in job_salary:
                splitted=job_salary.split('-')
                salary_from,salary_to=splitted[0],splitted[1]
            elif 'от' in job_salary:
                salary_from=job_salary.replace('от','')
                salary_to =''
            elif 'до' in job_salary:
                salary_from =''
                salary_to = job_salary.replace('до','')

            job_link=job_list['href']

            employer=job.find('div',{'class':'vacancy-serp-item__meta-info'}).getText()
            employer=employer.replace('\xa0', ' ')

            hh_data['employer']=employer
            hh_data['title']=job_title
            hh_data['salary_from']=salary_from.strip()
            hh_data['salary_to'] = salary_to.strip()
            hh_data['link']=job_link
            hh_data['taken_from']='HH'

            jobs_hh.append(hh_data)

            position = job_list['data-position']
            total_number=job_list['data-totalVacancies']
            position_updated=int(position)+1

            if int(position)==int(total_number):
                break
            if position_updated%20==0:
                sleep(randint(1, 5))
        except:
            pass

pprint(jobs_hh)

