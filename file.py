from playwright.sync_api import sync_playwright, Playwright
import time
import re
import requests

NTFY_TOPIC = "ixwbeibxowbxb8exn8e9nwxqbi"
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"
INTERVAL_MINUTES = 3

def run(playwright: Playwright):
    # Launch Firefox in headless mode
    browser = playwright.firefox.launch(headless=True)    
    context = browser.new_context()
    page = context.new_page()
    
    try:
        page.goto("https://mapa.zsr.sk/index.aspx")
        
        button_selector = "#termsModalSk .modal-footer button"
        page.wait_for_selector(button_selector)
        page.click(button_selector)

        main_menu_selector = "#mainMenuBtn"
        page.click(main_menu_selector)
        page.click("label.checkbox-custom-label:has-text('Všetky')")
        page.get_by_text("Os", exact=True).click()
        page.click("a.btn:nth-child(1)")
        page.locator("#searchByTrainText-selectized").fill("30") 

        dropdown_container = page.locator(".selectize-dropdown-content")
        results = dropdown_container.locator("div.option" or "div.option:nth-child(1)")
        count = results.count()

        def extract_numbers():
            clean_numbers = []
            for i in range(count):
                option_text = results.nth(i).inner_text()
                numbers = re.findall(r'\d+', option_text)
                for number in numbers:
                    num = int(number)
                    if 3000 <= num <= 3080:
                        clean_numbers.append(num)
            return clean_numbers

        clean_list = extract_numbers()
        for train_number in clean_list:
            page.locator("#searchByTrainText-selectized").fill(str(train_number))
            page.locator('#searchByTrainText-selectized').press('Enter')
            delay = page.locator(".popupContent > table:nth-child(1) > tbody:nth-child(1) > tr:nth-child(1) > td:nth-child(1) > span:nth-child(1)").text_content()
            if "meškal" in delay:
                send_notification(delay)

        browser.close()

    except Exception as e:
        print(f"An error occurred: {e}")


def send_notification(message):
    requests.post(NTFY_URL, data=message.encode('utf-8'))

if __name__ == "__main__":
    while True:
        with sync_playwright() as playwright:
            run(playwright)
        time.sleep(INTERVAL_MINUTES * 60)