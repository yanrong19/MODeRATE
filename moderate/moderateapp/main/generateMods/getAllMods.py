from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
PATH = 'C:/Orbital/Orbital_Moderate/moderate/moderateapp/main'
sys.path.insert(1, PATH)
from WebScraping import scrapeReddit

from urllib import parse
import csv

# CONSTANTS ====================================================================
#MODULE_PAGE = "https://nusmods.com/modules?sem[0]=1&sem[1]=2&sem[2]=3&sem[3]=4"
MODULE_PAGE = "https://nusmods.com/modules?&sem[0]=1&sem[1]=2&level[0]=1000&level[1]=2000&level[2]=3000&level[3]=4000&mcs[0]=4_5"
CLIENT_ID = "HJFREmWRT9QTnbohyZup6w"
CLIENT_SECRET = "S__YD99jhRGHnwWjzMFZTDlQeT18RA"
USER_AGENT = "Orbital"
nus_sub = scrapeReddit.create_subreddit(CLIENT_ID, CLIENT_SECRET, USER_AGENT, "nus")
# ==============================================================================

class Mod:
    #def __init__(self, code, title, link):
    def __init__(self, code):
        self.code = code 
        #self.title = title
        #self.link = link
# ================================================================================================================

def getBrowser():
    ser = Service("./chromedriver")
    opt = webdriver.ChromeOptions()
    opt.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(service=ser, options=opt)
    return browser
# ================================================================================================================

def getMaxPages():
    browser = getBrowser()
    browser.get(MODULE_PAGE)

    LAST_PAGE_XPATH = '//*[@id="app"]/div/div[1]/main/div/div/div[1]/nav/ul/li[last()]/button'
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, LAST_PAGE_XPATH))).click()

    url = browser.current_url
    max_page_num =parse.parse_qs(parse.urlparse(url).query)['p'][0]
    browser.close()
    return int(max_page_num)
# ================================================================================================================

def getPageMods(browser):
    # Wait for page to be hydrated
    first_mod_xpath = '//*[@id="app"]/div/div[1]/main/div/div/div[1]/div[2]/ul/li[1]/div/div[1]/header/h2/a'
    WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.XPATH, first_mod_xpath)))

    # List to store mod info
    pageModsList = []

    # Find all mod headers
    all_mods = browser.find_elements(by=By.CLASS_NAME, value="ZaN0o9av")
    for mod in all_mods:
        anchorElem = mod.find_element(by=By.XPATH, value="a")
        
        modCode = anchorElem.find_element(by=By.XPATH, value="span[1]").text
        #print(modCode)
        # check if mod has posts on reddit 
        posts = nus_sub.search(modCode)
        #print(len(list(posts)))
        if len(list(posts)) == 0:
            #print(modCode + " got no reviews")
            continue

        #modTitle = anchorElem.find_element(by=By.XPATH, value="span[2]").text
        #modLink = anchorElem.get_attribute("href")
        newMod = Mod(modCode)
        pageModsList.append(newMod)
    
    return pageModsList
# ================================================================================================================
def addModsToCSV(modList):
    with open('./mods.csv', 'a', newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Module Code"])
        for mod in modList:
            writer.writerow([mod.code])

def clearCSV():
    # Truncates the csv file
    f = open('./mods.csv', 'w+')
    f.close()

# ================================================================================================================

def getModList(max_page_num):
    browser = getBrowser()

    # Go through to the last page, and find mods
    i = 1
    while(i <= max_page_num):
        browser.get(MODULE_PAGE + f'&p={i}')
        pageModsList = getPageMods(browser)
        addModsToCSV(pageModsList)
        print(i , " page")
        i += 1
# ================================================================================================================

if __name__ == '__main__':
    # Clears CSV file before scraping through again
    # clearCSV()
    # # Find last page number
    lastPageNum = getMaxPages()
    # print(lastPageNum)
    # # Loop through to get all mods
    # getModList(lastPageNum)
    print(lastPageNum)