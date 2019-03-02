import urllib.request, shutil, os, time
from pathlib import Path
import re, sys
import json, csv
from selenium import webdriver
from agent import Agent
from tkinter import *

def main():

    # Variable Location, Space sensitive do %20
    location = "renton,wa"
    fileName = "agents.csv"

    master = Tk()
    master.title("Zillow Agent Scraper")
    Label(master, text="Location:").grid(row=0)
    e1 = Entry(master, width=50)
    e1.grid(row=0, column=1, pady=5)

    Label(master, text="File Name:").grid(row=1)
    e2 = Entry(master, width=50)
    e2.insert(0, "agents.csv")
    e2.grid(row=1, column=1, pady=5)

    Label(master, text="Start on page:").grid(row=2)
    e3 = Entry(master, width=50)
    e3.insert(0, "1")
    e3.grid(row=2, column=1, pady=5)

    Button(master, text='Start Scraping!', command= lambda: program(e1.get(), e2.get(), e3.get())).grid(row=3, column=1, pady=4)
    master.mainloop()


def program(location, fileName, startPage):

    print(location)
    print(fileName)
    print(startPage)

    fileExsist = Path(fileName)
    if not fileExsist.is_file():
        with open(fileName, 'w+') as csv_file:
            wr = csv.writer(csv_file, delimiter=',', lineterminator="\n")
            wr.writerow(["Name", "Company Name", "Address", "City", "State", "Zipcode", "Phone", "Email", "Website", "Sold this year"])

    page = int(startPage)
    count = 1
    agents = []
    threads = []
    driver = webdriver.Chrome()
    driver.set_page_load_timeout(20)

    while True:
        print("Page: {}".format(page))
        url = "https://www.zillow.com/ajax/directory/DirectoryContent.htm?apiVer=1&jsonVer=1&page={}&locationText={}&profession=real-estate-agent-reviews&proType=real-estate-agent&large=true".format(page, location)

        try:
            driver.get(url)
            page_source = json.loads(driver.find_element_by_tag_name("pre").text)
        except Exception as e:
            print("Solve the Captcha: {}".format(e))
            time.sleep(90)
            continue


        count = page_source["count"]
        if count == 0:
            break

        # print("Agent Creation")
        for idx, item in enumerate(page_source["model"]["viewModel"]["boards"]["boards"]):
            agents.append(Agent(item, driver))
            with open(fileName, 'a') as csv_file:
                wr = csv.writer(csv_file, delimiter=',', lineterminator="\n")
                wr.writerow(list(agents[-1]))

        page += 1

    driver.close()

if __name__ == '__main__':
    main()
