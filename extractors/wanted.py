from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time

root_url="https://www.wanted.co.kr"

class Job:
  def __init__(self, title, company, reward, link):
    self.title = title
    self.company = company
    self.reward = reward
    self.link = link

  def get_info(self):
    return [self.title, self.company, self.reward, self.link]


def auto_scroll(page):
  last_height = page.evaluate("document.body.scrollHeight")

  while True:
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(1)

    new_height = page.evaluate("document.body.scrollHeight")
    if new_height == last_height:
      break
    last_height = new_height


def scrape_wanted(keyword):
  url = f"{root_url}/search?query={keyword}&tab=position"

  jobs_list = []

  with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(url)

    auto_scroll(page)
    
    content = page.content()

  soup = BeautifulSoup(content, "html.parser")
  jobs = soup.find_all("div", class_="JobCard_container__FqChn")

  for job in jobs:
    title = job.find("strong", class_="JobCard_title__ddkwM").text
    company = job.find("span", class_="JobCard_companyName__vZMqJ").text
    reward = job.find("span", class_="JobCard_reward__sdyHn").text
    link = f'{root_url}{job.find("a")["href"]}'
    
    job_instance = Job(title, company, reward, link)
    jobs_list.append(job_instance)
  
  return jobs_list