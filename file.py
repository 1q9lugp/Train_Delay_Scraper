from playwright.sync_api import sync_playwright, Playwright
import time

def run(playwright: Playwright):
    # Launch Firefox with GUI
    browser = playwright.firefox.launch(headless=False, slow_mo=500)    
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
        print(f"Found {count} results in the dropdown.")

    # 5. Loop through results
        for i in range(count):
        # We use .nth(i) to grab each specific result
            result_text = results.nth(i).inner_text()
            print(f"Processing result {i+1}: {result_text}")
        
        # If you need to click each one to see details:
        # NOTE: Clicking usually closes the dropdown. 
        # For debugging, let's just highlight them.
        results.nth(i).evaluate("node => node.style.border = '2px solid red'")


        
        page.get_by_text("Os", exact=True).click()
        print("Success: Terms accepted. Browser will remain open.")
        #debugging        
        while True:
            
            time.sleep(1) 
            
    except Exception as e:
        print(f"An error occurred: {e}")
        # This keeps the terminal open so you can read the error 
        # before the browser closes.
        input("Press Enter to close the browser after error...")

with sync_playwright() as playwright:
    run(playwright)