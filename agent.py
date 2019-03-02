import urllib.request, shutil, os, time
import re, sys
import json, csv
import re
import time
from threading import Thread
from selenium import webdriver

class Agent(object):
    """docstring for Agent."""
    count = 0
    def __init__(self, jsonAgent, driver):
        self.name = jsonAgent["contact"]["summary"]["profileLink"]["text"]
        self.companyName = jsonAgent["map"]["businessName"]
        self.address = ""
        self.city = ""
        self.stateAbbreviation = ""
        self.zipcode = ""
        self.cellPhone = jsonAgent["contact"]["summary"]["phone"]
        self.email = ""
        self.website = ""
        self.profile = jsonAgent["href"]
        self.sold = ""
        self.driver = driver
        self.getAdditionalInfo()
        Agent.count += 1
        print("Agent Count: {}".format(Agent.count))
        # self.thread = Thread(target = self.getAdditionalInfo)
        # self.thread.start()

    def getAdditionalInfo(self):
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
        headers = {'User-Agent': user_agent}

        # print("Zillow Data")
        try:

            self.driver.get("https://zillow.com/"+self.profile)
            time.sleep(1)
            page_source = self.driver.page_source

            # geting sold
            self.sold = self.findItemInHTML(page_source, "ctcd-item ctcd-item_sales\">", " ")
            self.address = self.findItemInHTML(page_source, "class=\"street-address\">")
            self.city = self.findItemInHTML(page_source, "class=\"locality\">")
            self.stateAbbreviation = self.findItemInHTML(page_source, "class=\"region\">")
            self.zipcode = self.findItemInHTML(page_source, "class=\"postal-code\">")

            websiteHtml = self.findItemInHTML(page_source, "zsg-lg-3-5 profile-information-websites", "</dd>")
            self.website = self.findItemInHTML(websiteHtml, "href=\"", '"')
        except Exception as e:
            print("Zillow Info Error: {}".format(e))
            pass

        # print("Email Data")

        try:
            self.driver.get(self.website)
            self.driver.get(self.website)
            time.sleep(1)
            page_source = self.driver.page_source

            self.email = re.findall(r"[A-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[A-z0-9](?:[A-z0-9-]*[A-z0-9])?\.)+[A-z0-9](?:[A-z0-9-]*[A-z0-9])?", page_source)
        except Exception as e:
            print("Email Error: {}".format(e))
            pass


    def findItemInHTML(self, html, startText, endText="<"):
        start = html.find(startText) + len(startText)
        end = html[start:].find(endText) + start

        return html[start:end]

    def __iter__(self):
        # return "Name: {}\nCompany: {}\nAddress: {}\n{}\n{}\n{}\nPhone: {}\nEmail: {}\nWebsite: {}\nSold: {}\n\n".format(self.name, self.companyName, self.address, self.city, self.stateAbbreviation, self.zipcode, self.cellPhone, self.email, self.website, self.sold)
        return iter([self.name, self.companyName, self.address, self.city, self.stateAbbreviation, self.zipcode, self.cellPhone, self.email, self.website, self.sold])
