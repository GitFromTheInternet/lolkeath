import os
import time
import datetime
from playwright.sync_api import Playwright, sync_playwright, expect
from selenium.common import TimeoutException
import random
import requests

def generate_numbers():
    def generate_single():
        for max_current in range(16, 7, -1):
            for keath_current in range(max_current - 1, 0, -1):
                yield [max_current], [keath_current]

    def generate_double():
        for first_max in range(15, 7, -1):
            second_max = 16
            second_keath = 15
            for first_keath in range(first_max - 1, 0, -1):
                yield [first_max, second_max], [first_keath, second_keath]

    def generate_triple():
        for first_max in range(14, 7, -1):
            second_max, third_max = first_max + 1, 16
            second_keath, third_keath = first_max, 15
            for first_keath in range(first_max - 1, 0, -1):
                yield [first_max, second_max, third_max], [first_keath, second_keath, third_keath]

    # Generate single values
    yield from generate_single()

    # Generate double values
    yield from generate_double()

    # Generate triple values
    yield from generate_triple()

# Usage


def run(playwrite: Playwright) -> None:
    app_data_path = os.getenv("LOCALAPPDATA")
    user_data_path = os.path.join(app_data_path, 'Chromium\\User Data\\Default')
    context = playwrite.chromium.launch_persistent_context(user_data_path, headless=False, slow_mo=50)
    page = context.new_page()
    page.goto("https://football.fantasysports.yahoo.com/f1/189974/7")

    for max_current, keath_current in generate_numbers():
        print(f"max_current: {max_current}, keath_current: {keath_current}")
        wait_for_found = True
        while wait_for_found:
            found_trade = page.locator("text=You have proposed a trade to JIVE ASS TURKEYS")
            if found_trade.count() >= 1:
                print(f"{datetime.datetime.now()} - trade was found, going to sleep")
                time.sleep(15)
                found_trade.wait_for(timeout=3500)
            else:
                print(f"{datetime.datetime.now()} - trade was not found, sending new trade")
                wait_for_found = False
                pass
            page.reload()
            time.sleep(15)
        page.goto("https://football.fantasysports.yahoo.com/f1/189974/7/proposetrade?stage=1&mid2=12&tpids2[]=34344")
        for kval in keath_current:
            page.click(selector=f"input#select-pick-12-{kval}") #keaths picks
        page.click(selector='input#checkbox-31977')
        for mval in max_current:
            page.click(selector=f"input#select-pick-7-{mval}") #my pick
        page.click(selector='a.Btn-primary.ysf-cta.ysf-cta-main.ysf-cta-small:has-text("Continue")')
        time.sleep(45)
        textarea = page.wait_for_selector("#tradenote", state="visible", timeout=5000)
        quote_types = ["inspirational", "movies", "funny", "courage", "failure"]
        quote_type = random.choice(quote_types)
        text = ""
        try:
            r = requests.get(f"https://api.api-ninjas.com/v1/quotes?category={quote_type}",
                             headers={'X-Api-Key': '<APIKEY>'})
            if r.ok:
                print(r.json())
                quote = r.json()[0].get('quote')
                author = r.json()[0].get('author')
                text = f"\"{quote}\" -{author}"
        except Exception as e:
            print(f"Exception: {e}")
            pass
        if not text:
            text = "The ghost of Chad compels you! GO BROWNS"
        print(text)
        textarea.fill(text)
        time.sleep(15)
        page.click(selector='a.Btn-primary.ysf-cta.ysf-cta-main.ysf-cta-small:has-text("Send Trade Proposal")')
        page.goto("https://football.fantasysports.yahoo.com/f1/189974/7")
        print(f"{datetime.datetime.now()} - Send new trade offer. Entering main loop again")
        time.sleep(180)



if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)

