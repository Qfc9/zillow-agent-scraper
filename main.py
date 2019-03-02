import urllib.request, shutil, os, time
import re, sys
import json, csv
from selenium import webdriver
from agent import Agent

def main():

    # Variable Location, Space sensitive do %20
    location = "renton,wa"
    page = 1
    count = 1
    agents = []
    threads = []
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(20)
    drivers = []
    for i in range(10):
        drivers.append(webdriver.Chrome())
        drivers[-1].set_page_load_timeout(20)

    while True:
        print("Page: {}".format(page))
        url = "https://www.zillow.com/ajax/directory/DirectoryContent.htm?apiVer=1&jsonVer=1&page={}&locationText={}&profession=real-estate-agent-reviews&proType=real-estate-agent&large=true".format(page, location)

        try:
            driver.get(url)
            page_source = json.loads(driver.find_element_by_tag_name("pre").text)
        except Exception as e:
            print("Again Error: {}".format(e))
            time.sleep(60)
            continue


        count = page_source["count"]
        if count == 0:
            break

        print("Agent Creation")
        for idx, item in enumerate(page_source["model"]["viewModel"]["boards"]["boards"]):
            agents.append(Agent(item, drivers[idx]))

        time.sleep(30)
        page += 1

    driver.close()
    for driver in drivers:
        driver.close()

    print(len(agents))

    with open("agents.csv", 'w+') as csv_file:
        wr = csv.writer(csv_file, delimiter=',', lineterminator="\n")
        wr.writerow(["Name", "Company Name", "Address", "City", "State", "Zipcode", "Phone", "Email", "Website", "Sold this year"])
        for agent in agents:
            wr.writerow(list(agent))


if __name__ == '__main__':
    main()
