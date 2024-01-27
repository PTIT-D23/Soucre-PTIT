import os
from bs4 import BeautifulSoup as bs
from requests import Session
from time import sleep

from dotenv import load_dotenv
load_dotenv()

import custom_settings

lang ={
    '190': 'cpp',
    '326': 'py',
    '329': 'java',
    '337': 'cpp',
}

def main():
    print('getting storage path...')
    storage_path = os.environ.get('storage_path')
    if not os.path.exists(storage_path):
        try:
            print('creating folder for you lazy -.-')
            os.makedirs(storage_path)
        except:
            print('please defina a valid folder path (for example: D:/CODE/Python)')
            return

    #save time and avoid GET requests limit
    existing_solutions = set()
    if custom_settings.CACHE:
        for solution in os.listdir(storage_path):
            if solution.startswith('.'): continue
            id, name = solution.rsplit('.', 1)[0].split(' - ', 1)
            existing_solutions.add(id)

    #this is amount of time for waiting to reset GET requests limit
    time_sleep = int(os.environ.get('timesleep', '60'))

    session = Session()
    print('get login form...')
    login_site = session.get('https://code.ptit.edu.vn/login')

    login_soup = bs(login_site.content, 'html.parser')

    print('logging in...')
    CSRF_token = login_soup.find('input', {'name': '_token'})['value']
    login_data = {"username": os.environ.get('PTIT_username'),
                  "password": os.environ.get('PTIT_password'),
                  "_token": CSRF_token}

    session.post('https://code.ptit.edu.vn/login', login_data)

    print('collecting problems...')
    home = session.get('https://code.ptit.edu.vn/student/question?course='+os.environ.get('course'))
    home_soup = bs(home.content, 'html.parser')
    number_of_page = len(home_soup.find_all('a', {'class': 'page-link'}))

    ac_problem_links = []
    for i in range(number_of_page):
        problem_page = session.get('https://code.ptit.edu.vn/student/question?page=' + str(i+1))
        problem_page_soup = bs(problem_page.content, 'html.parser') 
        for data in problem_page_soup.find_all('tr', {'class': 'bg--10th'}):
            a_tag = data.find('a')
            ac_problem_id, ac_problem_link = a_tag.contents[0], a_tag['href']
            if ac_problem_id in existing_solutions:
                continue
            ac_problem_links.append(ac_problem_link)

    crawled_problems = []
    for ac_link in ac_problem_links:
        print('getting best submission for ' + ac_link + '...')
        problem_detail = session.get(ac_link)
        while problem_detail.status_code == 429:
            print(f'watting {time_sleep}s for reseting GET requests limit')
            sleep(time_sleep)
            problem_detail = session.get(ac_link)
        problem_detail_soup = bs(problem_detail.content, 'html.parser')
        submission_pages = len(problem_detail_soup.find_all('a', {'class': 'page-link'})) or 1

        ac_submission_links = []
        for i in range(submission_pages): 
            submission_page = session.get(ac_link + '?page=' + str(i+1))
            while submission_page.status_code == 429:
                print(f'watting {time_sleep}s for reseting GET requests limit')
                sleep(time_sleep)
                submission_page = session.get(ac_link + '?page=' + str(i+1))
            submission_page_soup = bs(submission_page.content, 'html.parser')

            table = submission_page_soup.find('table', {'class': 'status__table'})
            for submisson in table.find('tbody').find_all('tr'):
                status = ''.join(submisson.find('span').contents)
                if status == 'AC':
                    submisson_link = submisson.find_all('a')[1]['href']
                    submission_id, submission_time, \
                    submission_memory, submission_lang = submisson.find_all('td', {'class': 'text--middle'})
                    ac_submission_links.append((submisson_link, float(submission_time.contents[0][:-1]), int(submission_memory.contents[0][:-2])))
        
        best_submission_link = sorted(ac_submission_links, key=lambda x: (x[1], x[2]))[0][0]
        print(best_submission_link)

        print('crawling code...')
        source_page = session.get(best_submission_link)
        while source_page.status_code == 429:
            print(f'watting {time_sleep}s for reseting GET requests limit')
            sleep(time_sleep)
            source_page = session.get(best_submission_link)
        source_page_soup = bs(source_page.content, 'html.parser')
        problem_title = source_page_soup.find('a', {'class': 'link--red'}).contents[0]
        source_code = source_page_soup.find('input', {'id': 'source_code'})['value']

        source_storage_path = os.path.join(storage_path, problem_title + '.' + lang[os.environ.get('course')])
        with open(source_storage_path, 'w', encoding='utf-8') as f:
            for line in source_code.splitlines():
                f.write(line + '\n')
            f.close()
        
        result = problem_title + ' ✔️'
        print(result + '\n')
        crawled_problems.append(result)
        sleep(int(os.environ.get('timedelay', 0)))
        if len(crawled_problems)%10 == 0: 
            if os.environ.get('timeperten'):
                print(f'sleep ' + os.environ.get('timeperten')+'s after crawling 10 problems')
            sleep(int(os.environ.get('timeperten', 0)))
    
    print('Done!')
    print('\n'.join(crawled_problems))

if __name__ == '__main__':
    main()
