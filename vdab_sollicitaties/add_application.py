import asyncio
from playwright.async_api import async_playwright, Page, Playwright
import logging
import os # Import the os module

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def add_single_application(page: Page, app_data: dict):
    """
    Adds a single external application using the provided page object and data.
    Retries clicking the 'Add' button once if it fails initially.
    Returns True on success, False on failure for this specific application.
    """
    job_title = app_data['job_title']
    company_name = app_data['company_name']
    location = app_data['location']

    logging.info(f"--- Starting application for: {company_name} - {job_title} ---")

    try:
        # 1. Click "Voeg externe vacature toe"
        logging.info("Attempting to click 'Voeg externe vacature toe'...")
        add_button_selector = "button:has-text('Voeg externe vacature toe')"
        try:
            await page.wait_for_selector(add_button_selector, timeout=15000)
            await page.locator(add_button_selector).click()
            logging.info("Add button clicked.")
        except Exception as click_error:
            logging.warning(f"Initial click failed: {click_error}. Refreshing and retrying once.")
            await page.reload(wait_until="domcontentloaded") # Reload the page
            await page.wait_for_selector(add_button_selector, timeout=20000) # Longer wait after reload
            await page.locator(add_button_selector).click()
            logging.info("Add button clicked on retry.")

        # Wait for the modal to appear
        modal_title_selector = "h2:has-text('Voeg een externe vacature toe')"
        logging.info("Waiting for modal...")
        await page.wait_for_selector(modal_title_selector, timeout=15000)
        logging.info("Modal detected.")

        # 2. Fill in the details
        logging.info(f"Typing Functiebeschrijving: {job_title}")
        await page.get_by_role('textbox', name='Functiebeschrijving').fill(job_title)

        logging.info(f"Typing Bedrijfsnaam: {company_name}")
        await page.get_by_role('textbox', name='Bedrijfsnaam').fill(company_name)

        logging.info(f"Typing Plaats bedrijf: {location}")
        await page.get_by_role('textbox', name='Plaats bedrijf').fill(location)

        # 3. Select status
        logging.info("Selecting status 'Ik heb gesolliciteerd'...")
        status_selector = "select[id='select-soll-activiteit-code']"
        await page.locator(status_selector).select_option(label="Ik heb gesolliciteerd")
        logging.info("Status selected.")

        await page.wait_for_timeout(1000) # Wait for date field

        # 4. Click "Bewaar"
        # Use get_by_role with exact name matching the successful MCP run.
        # Playwright's click action includes built-in waits for the element to be ready.
        logging.info("Clicking 'Bewaar' button...")
        await page.get_by_role('button', name='Bewaar', exact=True).click()
        logging.info("Save button clicked.")

        # Wait for the main page elements to confirm modal closed and list updated
        logging.info("Waiting for page update after save...")
        await page.wait_for_selector(add_button_selector, timeout=15000) # Wait for the 'Add' button to be visible again
        logging.info(f"Successfully added application for: {company_name} - {job_title}")
        return True

    except Exception as e:
        logging.error(f"Failed to add application for {company_name} - {job_title}: {e}")
        logging.warning("Taking a screenshot for debugging...")
        try:
            # Ensure the screenshot path is relative to the script
            screenshot_path = f"error_{company_name.replace(' ', '_')}.png"
            await page.screenshot(path=screenshot_path)
            logging.info(f"Screenshot saved as {screenshot_path}")
        except Exception as screen_err:
            logging.error(f"Could not save screenshot: {screen_err}")
        return False

async def main():
    # --- Configuration ---
    FIXED_JOB_TITLE = "Growth Engineer"
    FIXED_LOCATION = "European Economic Area"
    COMPANY_LIST_FILE = "company_list.txt"

    # --- Read Company List ---
    company_names = []
    if not os.path.exists(COMPANY_LIST_FILE):
        logging.error(f"Error: Company list file '{COMPANY_LIST_FILE}' not found.")
        return
    
    try:
        with open(COMPANY_LIST_FILE, 'r', encoding='utf-8') as f:
            company_names = [line.strip() for line in f if line.strip()] # Read non-empty lines
        logging.info(f"Read {len(company_names)} company names from {COMPANY_LIST_FILE}.")
    except Exception as e:
        logging.error(f"Error reading company list file: {e}")
        return

    if not company_names:
        logging.warning("Company list file is empty. No applications to add.")
        return

    # --- Playwright Setup and Login ---
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        start_url = "https://www.vdab.be/vindeenjob/prive/bewaarde-vacatures-en-sollicitaties"
        logging.info(f"Navigating to {start_url} ...")
        await page.goto(start_url, wait_until="domcontentloaded")

        # --- Manual Login Step (Once) ---
        input("\nPlease log in manually in the browser window and navigate to the \"Bewaarde vacatures en sollicitaties\" page.\nPress Enter here when you are ready to continue the script...")
        logging.info("Login confirmed by user. Starting bulk add...")

        successful_adds = 0
        failed_adds = 0

        # --- Loop through companies ---        
        for company_name in company_names:
            app_data = {
                "job_title": FIXED_JOB_TITLE,
                "company_name": company_name,
                "location": FIXED_LOCATION
            }
            success = await add_single_application(page, app_data)
            if success:
                successful_adds += 1
            else:
                failed_adds += 1
                # Optional: Add a pause or different handling for failures
                # input("An error occurred. Check the browser and logs. Press Enter to attempt the next application...")
            
            logging.info("Waiting a short time before next application...")
            await page.wait_for_timeout(2000) # 2 second pause between attempts

        # --- Summary and Cleanup ---
        logging.info("--- Bulk Add Summary ---")
        logging.info(f"Successfully added: {successful_adds}")
        logging.info(f"Failed attempts:    {failed_adds}")
        logging.info("------------------------")

        # Keep browser open at the end
        input("Script finished processing all applications. Press Enter to close the browser...")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main()) 