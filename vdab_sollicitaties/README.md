# VDAB External Application Adder

This script automates adding external job applications to your VDAB profile using Playwright.

## Prerequisites

*   Python installed
*   `uv` package manager installed (`pip install uv`)

## Setup

1.  **Install Dependencies:**
    ```bash
    uv sync
    ```
2.  **Install Browsers:** (Only needs to be done once)
    ```bash
    uv run playwright install
    ```

## How to Use

1.  **Edit Job Details:**
    Open `add_application.py` in a text editor.
    Find the `main()` function near the bottom.
    Modify the values for `job_title_to_add`, `company_name_to_add`, and `location_to_add` with the details of the application you want to add.

2.  **Run the Script:**
    ```bash
    uv run python add_application.py
    ```

3.  **Manual Login:**
    A browser window will open and navigate to the VDAB login page.
    Log in manually using your credentials.
    Navigate to the **Bewaarde vacatures en sollicitaties** page.

4.  **Confirm Login:**
    Switch back to the terminal where you ran the script.
    Press `Enter` to confirm you have logged in and are on the correct page.

5.  **Automation:**
    The script will now automatically perform the steps to add the application:
    *   Click "Voeg externe vacature toe"
    *   Fill in the job title, company, and location
    *   Select the status "Ik heb gesolliciteerd"
    *   Click "Bewaar"

6.  **Review & Close:**
    The script will pause after saving, allowing you to check the result in the browser.
    Press `Enter` in the terminal again to close the browser and end the script.

## Notes

*   The script uses CSS selectors (like `button:has-text(...)` and `input[id=...]`) to find elements. If VDAB updates their website structure, these selectors might need to be adjusted.
*   Timeouts are included, but if your internet connection is very slow or the VDAB site is unresponsive, the script might time out. You may need to adjust the `timeout` values (in milliseconds) in the `wait_for_selector` calls.
