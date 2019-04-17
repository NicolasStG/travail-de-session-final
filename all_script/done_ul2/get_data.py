#!/bin/python3
import argparse
import json
import os
import sys
from operator import itemgetter

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import (
    presence_of_element_located,
)
from selenium.webdriver.support.ui import Select, WebDriverWait

timeout = 3


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--download", action="store_true", default=False)
    parser.add_argument("-e", "--erase", action="store_true", default=False)
    parser.add_argument("-c", "--clean", action="store_true", default=False)
    parser.add_argument(
        "-n", "--no-headless", action="store_true", default=False
    )
    return parser.parse_args()


#################
# data download #
#################


def get_browser(no_headless: bool):
    if not no_headless:
        os.environ["MOZ_HEADLESS"] = "1"
    browser = webdriver.Firefox()
    print("Opened browser.".ljust(80), end="\r")
    return browser


def close_browser(browser, err=True):
    browser.close()
    try:
        os.remove("geckodriver.log")
    except FileNotFoundError:
        pass
    if err:
        sys.exit()
    print("Closed browser.".ljust(80))


def download_data(browser, url, erase):
    if erase:
        erase_downloaded_data()

    current_expertise_idx = get_current_expertise_idx()

    browser.get(url)

    try:
        select = Select(
            WebDriverWait(browser, timeout).until(
                presence_of_element_located((By.NAME, "p_seq_expertise_root"))
            )
        )
    except TimeoutException:
        print("Could not find element or page took too long to load.")
        close_browser(browser)

    expertises = [
        o.text for o in select.options if o.text != "Choisir une expertise"
    ]
    for i, expertise in enumerate(expertises):
        if i < current_expertise_idx:
            continue
        download_expertise_professors(browser, expertise)

    print("Data downloaded.".ljust(80))
    close_browser(browser, err=False)


def download_expertise_professors(browser, expertise):
    try:
        select = Select(
            WebDriverWait(browser, timeout).until(
                presence_of_element_located((By.NAME, "p_seq_expertise_root"))
            )
        )
    except TimeoutException:
        print("Could not find element or page took too long to load.")
        close_browser(browser)

    select.select_by_visible_text(expertise)

    try:
        select = Select(
            WebDriverWait(browser, timeout).until(
                presence_of_element_located((By.NAME, "p_seq_expertise"))
            )
        )
    except TimeoutException:
        print("Could not find element or page took too long to load.")
        close_browser(browser)

    sub_expertises = [
        o.text
        for o in select.options
        if o.text != "Choisir une expertise spécifique"
    ]
    #  sub_expertises = [
    #  o.text for o in select.options if o.text == "Analyse des durées de vie"
    #  ]
    professors = [
        {
            "sub_expertise": sub_expertise,
            "professors": get_sub_expertise_professors(
                browser, expertise, sub_expertise, i, len(sub_expertises)
            ),
        }
        for i, sub_expertise in enumerate(sub_expertises)
    ]

    browser.find_element_by_link_text("Accueil").click()

    save_expertise_to_json({"expertise": expertise, "professors": professors})


def get_sub_expertise_professors(
    browser, expertise, sub_expertise, idx, total
):
    print(
        f"Downloading data for {expertise} ({idx + 1}/{total})...".ljust(80),
        end="\r",
    )

    try:
        select = Select(
            WebDriverWait(browser, timeout).until(
                presence_of_element_located((By.NAME, "p_seq_expertise"))
            )
        )
    except TimeoutException:
        print("Could not find element or page took too long to load.")
        close_browser(browser)

    select.select_by_index(idx + 1)

    try:
        main_table = (
            WebDriverWait(browser, timeout)
            .until(presence_of_element_located((By.TAG_NAME, "tbody")))
            .find_elements_by_xpath("tr")[2]
            .find_element_by_tag_name("tbody")
        )
    except TimeoutException:
        print("Could not find student or page took too long to load.")
        close_browser(browser)

    names = [
        table.find_element_by_xpath("tr").find_element_by_tag_name("h1").text
        for table in main_table.find_elements_by_tag_name("tbody")[1:]
    ]

    professors = [get_professor_info(browser, name) for name in names]

    browser.find_element_by_link_text("Retour à la liste").click()

    return professors


def get_professor_info(browser, name):
    try:
        link = (
            WebDriverWait(browser, timeout)
            .until(presence_of_element_located((By.LINK_TEXT, name)))
            .get_attribute("href")
        )
    except TimeoutException:
        print("Could not find element or page took too long to load.")
        close_browser(browser)

    browser.get(link)

    try:
        main_table = (
            WebDriverWait(browser, timeout)
            .until(presence_of_element_located((By.TAG_NAME, "tbody")))
            .find_elements_by_xpath("tr")[2]
            .find_element_by_tag_name("tbody")
            .find_elements_by_tag_name("tbody")[1]
            .find_element_by_tag_name("tbody")
            #  .find_elements_by_tag_name("tr")
        )
    except TimeoutException:
        print("Could not find student or page took too long to load.")
        close_browser(browser)

    info = {
        "name": name,
        "email": main_table.find_element_by_xpath(
            "//td[text()='Courriel']/following-sibling::td/"
            "following-sibling::td/a"
        ).text,
        "number": main_table.find_element_by_xpath(
            "//td[text()='Téléphone']/following-sibling::td/"
            "following-sibling::td"
        ).text.replace("<br>", ""),
        "role": main_table.find_element_by_xpath(
            "//td[text()='Fonction']/following-sibling::td/"
            "following-sibling::td"
        ).text.replace("<br>", ""),
    }

    browser.find_element_by_link_text("Retour à la liste").click()

    return info


def save_expertise_to_json(expertise):
    path = "data"
    if not os.path.exists(path):
        os.mkdir(path)
    path = os.path.join(path, "downloaded_data.json")

    with open(path, "ab+") as f:
        f.seek(0, 2)
        if f.tell() == 0:
            f.write(json.dumps([expertise]).encode())
        else:
            f.seek(-1, 2)
            f.truncate()
            f.write(", ".encode())
            f.write(json.dumps(expertise).encode())
            f.write("]".encode())


def erase_downloaded_data():
    path = os.path.join("data", "downloaded_data.json")
    if os.path.exists(path):
        os.remove(path)


def get_current_expertise_idx():
    path = os.path.join("data", "downloaded_data.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
        return len(data)
    else:
        return 0


#################
# data cleaning #
#################


def clean_data():
    path = os.path.join("data", "downloaded_data.json")
    if not os.path.exists(path):
        raise FileNotFoundError("The data has to be downloaded first.")
    with open(path, "r") as f:
        data = json.load(f)

    cleaned_data = list(
        sorted(
            (
                {
                    "name": f"{professor['name'].split(', ')[1].title()} "
                    f"{professor['name'].split(', ')[0].title()}",
                    "email": professor["email"].lower(),
                    "number": professor["number"],
                    "role": professor["role"],
                    "sub_expertise": sub_expertise["sub_expertise"],
                    "expertise": expertise["expertise"],
                }
                for expertise in data
                for sub_expertise in expertise["sub_expertises"]
                for professor in sub_expertise["professors"]
            ),
            key=itemgetter("name"),
        )
    )
    save_cleaned_data(cleaned_data)


def save_cleaned_data(data):
    json_path = os.path.join("data", "cleaned_data.json")
    csv_path = os.path.join("data", "cleaned_data.csv")

    with open(json_path, "w") as f:
        json.dump(data, f)

    with open(csv_path, "w") as f:
        columns = [
            "name",
            "role",
            "expertise",
            "sub_expertise",
            "email",
            "number",
        ]
        f.write(f"{','.join(columns)}\n")
        for row in data:
            f.write(f"{','.join(row[c] for c in columns)}\n")


if __name__ == "__main__":
    url = "https://oraweb.ulaval.ca/pls/vrr/gexp_dap.html"
    args = read_args()
    if args.download:
        browser = get_browser(args.no_headless)
        download_data(browser, url, args.erase)
    if args.clean:
        clean_data()
