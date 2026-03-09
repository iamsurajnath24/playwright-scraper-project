# Playwright browser automation ke liye import
from playwright.sync_api import sync_playwright

# HTML parse karne ke liye BeautifulSoup import
from bs4 import BeautifulSoup

# Data ko table format (DataFrame) me handle karne ke liye pandas
import pandas as pd

# Multiple images ko ek PDF me convert karne ke liye library
import img2pdf

# OS library folder create karne ke liye
import os


# Agar screenshots ya output folder exist nahi karta to create kar do
os.makedirs("screenshots", exist_ok=True)
os.makedirs("output", exist_ok=True)


# Screenshots ke file paths store karne ke liye list
screenshots = []


# Playwright automation start karne ke liye context
with sync_playwright() as p:

    # Chromium browser launch karo (headless=False matlab browser visible rahega)
    browser = p.chromium.launch(headless=False)

    # Naya browser page open karo
    page = browser.new_page()


    # Login page open karo
    page.goto("https://quotes.toscrape.com/login", wait_until="domcontentloaded")

    # Username input field load hone ka wait karo
    page.wait_for_selector('input[name="username"]')


    # Login page ka screenshot lo
    page.screenshot(path="screenshots/login_page.png", full_page=True)

    # Screenshot path list me add karo (later PDF banane ke liye)
    screenshots.append("screenshots/login_page.png")


    # Username field me text fill karo
    page.fill('input[name="username"]', "admin")

    # Password field me text fill karo
    page.fill('input[name="password"]', "admin")


    # Filled login form ka screenshot lo
    page.screenshot(path="screenshots/form_filled.png", full_page=True)

    # Screenshot path list me store karo
    screenshots.append("screenshots/form_filled.png")


    # Login button click karo
    page.click('input[type="submit"]')


    # 2 second wait karo (page load hone ke liye)
    page.wait_for_timeout(2000)


    # Login ke baad page ka screenshot lo
    page.screenshot(path="screenshots/after_login.png", full_page=True)

    # Screenshot path store karo
    screenshots.append("screenshots/after_login.png")


    # Quotes listing page open karo
    page.goto("https://quotes.toscrape.com/", wait_until="domcontentloaded")


    # Quotes page ka screenshot lo
    page.screenshot(path="screenshots/quotes_page.png", full_page=True)

    # Screenshot path store karo
    screenshots.append("screenshots/quotes_page.png")


    # Page ka complete HTML content lo
    html = page.content()


    # BeautifulSoup ko HTML parse karne ke liye use karo
    soup = BeautifulSoup(html, "html.parser")


    # Saare quotes elements find karo
    quotes = soup.find_all("div", class_="quote")


    # Extracted data store karne ke liye list
    data = []


    # Har quote element par loop chalao
    for q in quotes:

        # Quote text extract karo
        text = q.find("span", class_="text").text

        # Author name extract karo
        author = q.find("small", class_="author").text

        # Har quote ke tags extract karo
        tags = [tag.text for tag in q.find_all("a", class_="tag")]


        # Extracted data dictionary form me list me add karo
        data.append({
            "quote": text,
            "author": author,
            "tags": ", ".join(tags)
        })


    # Extracted data ko pandas DataFrame me convert karo
    df = pd.DataFrame(data)


    # Terminal me first 5 rows show karo
    print(df.head())


    # DataFrame ko CSV file me save karo
    df.to_csv("output/quotes_data.csv", index=False)


    # Browser close karo
    browser.close()


# Screenshots ko ek single PDF report me convert karo
with open("output/report.pdf", "wb") as f:
    f.write(img2pdf.convert(screenshots))


# Final message print karo
print("Done")