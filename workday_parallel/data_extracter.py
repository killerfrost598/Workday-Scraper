from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,TimeoutException
from selenium.webdriver.chrome.options import Options
import utils, ctypes

# import time
from datetime import datetime


class jobdata_extracter():
    def __init__(self):
        chrome_options = Options()
        chrome_options.headless = False
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000002)
        self.driver = webdriver.Chrome()


    def data_extracter(self,link):
        self.driver.get(link)
        keyword = utils.key_extracter(link)
        try:
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"css-1q2dra3")))
            jobspanel = self.driver.find_element(By.CLASS_NAME,"css-8j5iuw")
            jobcount = jobspanel.find_element(By.CLASS_NAME,"css-12psxof")

            jobs = jobspanel.find_elements(By.CLASS_NAME,"css-1q2dra3")


            
            

            try:
                count = 0
                listofjobs = []
                for job in jobs:
                    # implement python dictionary to store jobname, joblink, joblocation, postingdate, postingid, keyword, timestamp, job_count
                    jobinfo = {"jobname":"","joblink":"", "joblocation":"", "postingdate":"", "postingid":"","keyword":"","timestamp":"","job_count":""}
                    jobname = job.find_element(By.CLASS_NAME,"css-b3pn3b")
                    joblink = jobname.find_element(By.TAG_NAME,"a").get_attribute("href")
                    joblocation = job.find_element(By.CLASS_NAME,"css-248241")
                    postingdate = job.find_element(By.CLASS_NAME,"css-zoser8")
                    postingid = job.find_element(By.CLASS_NAME,"css-14a0imc")
                    jobinfo["jobname"] = str(jobname.text)
                    jobinfo["joblink"] = str(joblink)
                    jobinfo["joblocation"] = joblocation.find_element(By.CLASS_NAME,"css-129m7dg").text
                    jobinfo["postingdate"] = postingdate.find_element(By.CLASS_NAME,"css-129m7dg").text
                    jobinfo["postingid"] = postingid.text
                    jobinfo["keyword"] = str(keyword)
                    jobinfo["timestamp"] = str(datetime.now())
                    jobinfo["job_count"] = jobcount.text.replace('JOBS FOUND','')
                    listofjobs.append(jobinfo)
                    count += 1
                # Think about logging the data scraped
                # log  = {"keyword":keyword,"Jobs_posted":count,"job_count":jobcount.text.replace('JOBS FOUND',''),"timestamp":datetime.now(),"link":link}
                return listofjobs
            
            except NoSuchElementException:
                exception = {"Exception": "No Such Element Exception" ,"link":link,"keyword":keyword,"timestamp":str(datetime.now())}
                return exception
        except TimeoutException:
            exception = {"Exception": "Timeout Exception" ,"link":link,"keyword":keyword,"timestamp":str(datetime.now())}
            return exception
        
    def close(self):
        self.driver.quit()