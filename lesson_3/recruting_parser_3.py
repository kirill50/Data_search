from bs4 import BeautifulSoup as bs
from random import randint
from time import sleep
from pprint import pprint
import requests
from pymongo import MongoClient

header={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'}
job_title=input("Type the job title you are looking for: ")
pages_number=input("Type the number of pages you would like to get: ")

def hh_parser(header,job_title,pages_number):
    l = job_title.split()
    prepared_job_title = '+'.join(l)

    main_link='https://hh.ru/'
    jobs_hh=[]

    for i in range(0, (int(pages_number))):
        full_link=f'{main_link}search/vacancy?L_is_autosearch=false&area=1&clusters=true&enable_snippets=true&text={prepared_job_title}&page={str(i)}'
        html=requests.get(full_link, headers=header)
        if html.ok:
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
                    #job_html = requests.get(job_link, headers=header)
                    #job_parsed_html = bs(job_html.content, 'lxml')
                    #currency=job_parsed_html.find('meta', {'itemprop': 'currency'})['content']

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

            return jobs_hh

def super_parser(header,job_title,pages_number):
    main_link = 'https://www.superjob.ru'
    full_link = f'{main_link}/vacancy/search/?keywords={job_title}&geo%5Bc%5D%5B0%5D=1'

    jobs_super = []

    html = requests.get(full_link, headers=header)
    if html.ok:
        parsed_html = bs(html.content, 'lxml')
        for i in range(0, (int(pages_number))):
            try:
                next_button = parsed_html.find('a', {'rel': 'next'})['href']
                next_link = f'{main_link}{next_button}'
                if i != 0:
                    html = requests.get(next_link, headers=header)
                    parsed_html = bs(html.content, 'lxml')
                else:
                    pass

                job_block = parsed_html.find('div', {'style': 'display:block'})

                for job in job_block:
                    hh_data = {}
                    # print(job)
                    try:
                        empty_employer = job.find('a', {'target': '_blank'})
                        non_empty_employer = job.find('a', {'target': '_self'})
                        job_title = job.find('a').getText()

                        if job.find('a')['href'].startswith('/vakansii'):
                            partial_link = job.find('a')['href']

                        else:
                            pass

                        job_salary = job.find('span', {
                            'class': '_3mfro _2Wp8I f-test-text-company-item-salary PlM3e _2JVkc _2VHxz'}).getText()
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

                        job_link=f'{main_link}{partial_link}'

                        hh_data['link'] = job_link
                        hh_data['salary_from'] = salary_from.strip()
                        hh_data['salary_to'] = salary_to.strip()
                        hh_data['title'] = job_title
                        if not non_empty_employer.getText:
                            hh_data['employer'] = ''
                        else:
                            hh_data['employer'] = non_empty_employer.getText()
                        hh_data['taken_from'] = 'SuperJob'

                        jobs_super.append(hh_data)
                    except:
                        pass

                return jobs_super
            except:
                return list(jobs_super)
                break

hh_jobs=hh_parser(header,job_title,pages_number)
super_jobs=super_parser(header,job_title,pages_number)

#store data in monodb
client=MongoClient('localhost', 5555)
db=client['RECRUTING_DB']
superjob=db.superjob
headhunter=db.headhunter


#add unique values in mongo dataset
for job in super_jobs:
    if job['link'] in superjob.distinct('link'):
        pass
    else:
        superjob.insert_one(job)

for job in hh_jobs:
    if job['link'] in headhunter.distinct('link'):
        pass
    else:
        headhunter.insert_one(job)

#getting jobs with salary equal or more than #value#
def search_by_salary_from(value):
    objects=superjob.find({'salary_from':{'$gte':str(value)}})
    objects2=headhunter.find({'salary_from':{'$gte':str(value)}})
    for obj in objects:
        pprint(obj)
    for obj2 in objects2:
        pprint(obj2)

search_by_salary_from(50000)