from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver):
    username = ""  # <username here>
    password = ""  # <password here>

    # Load page
    driver.get("https://www.instagram.com/accounts/login/")

    # Login
    driver.find_element_by_xpath("//div/input[@name='username']").send_keys(username)
    driver.find_element_by_xpath("//div/input[@name='password']").send_keys(password)
    driver.find_element_by_xpath("//span/button").click()

    # Wait for the login page to load
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.LINK_TEXT, "See All")))


def scrape_followers(driver, account):
    # Load account page
    driver.get("https://www.instagram.com/{0}/".format(account))

    # Click the 'Follower(s)' link
    # driver.find_element_by_partial_link_text("follower").click()

    # driver.find_element_by_partial_link_text("following").click()

    # Wait for the followers modal to load
    xpath = "//div[@style='position: relative; z-index: 1;']/div/div[2]/div/div[1]"
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

    # You'll need to figure out some scrolling magic here. Something that can
    # scroll to the bottom of the followers modal, and know when its reached
    # the bottom. This is pretty impractical for people with a lot of followers

    dialog=driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]')
    allfoll=long(driver.find_element_by_xpath("//li[2]/a/span").text) 
    print ('Total Followers: ', allfoll)

    for i in range(long(allfoll)):
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
        # time.sleep(random.randint(500,1000)/1000)
        # print("Extract friends %",round((i/(allfoll/2)*100),2),"from","%100")

    # Finally, scrape the followers
    xpath = "//div[@style='position: relative; z-index: 1;']//ul/li/div/div/div/div/a"
    followers_elems = driver.find_elements_by_xpath(xpath)
    # print (followers_elems)

    return [e.text for e in followers_elems]


if __name__ == "__main__":
    driver = webdriver.Chrome('/media/dhruv/OS/Python27/Scripts/chromedriver.exe')
    try:
        login(driver)
        followers = scrape_followers(driver, "charitharth_reddi")
        print(followers)
    finally:
        driver.quit()