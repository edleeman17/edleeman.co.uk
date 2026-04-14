"""Playwright automation for Fable CSV import."""
from pathlib import Path
from playwright.sync_api import Page, BrowserContext

import config

FABLE_URL = "https://fable.co"


def _ensure_dirs():
    config.FABLE_AUTH.parent.mkdir(parents=True, exist_ok=True)


def get_context(playwright):
    """Get a browser context, reusing saved auth if available."""
    _ensure_dirs()
    browser = playwright.chromium.launch(headless=config.HEADLESS)
    if config.FABLE_AUTH.exists():
        context = browser.new_context(storage_state=str(config.FABLE_AUTH))
    else:
        context = browser.new_context()
    return context


def save_auth(context: BrowserContext):
    _ensure_dirs()
    context.storage_state(path=str(config.FABLE_AUTH))


def ensure_logged_in(page: Page) -> bool:
    """Navigate to Fable and check login."""
    page.goto(f"{FABLE_URL}/goodreads-import")
    page.wait_for_load_state("networkidle")

    if "login" in page.url or "sign" in page.url:
        if config.HEADLESS:
            print("  ERROR: Fable not logged in. Run ./login.sh first.")
            return False
        print("\n  Fable: not logged in.")
        print("  Please log in manually in the browser window.")
        print("  Press Enter here once done...")
        input()

    print("  Fable: logged in ✓")
    return True


def import_csv(page: Page, csv_path: Path):
    """Upload a Goodreads-format CSV to Fable's CSV import (beta)."""
    page.goto(f"{FABLE_URL}/goodreads-import")
    page.wait_for_load_state("networkidle")

    file_input = page.locator("input[type='file']").first
    if file_input.count() == 0:
        print("  ERROR: Could not find file input on Fable import page")
        print(f"  Current URL: {page.url}")
        return False

    file_input.set_input_files(str(csv_path))
    print(f"  Uploaded {csv_path.name} to Fable")

    page.wait_for_timeout(1000)

    submit = page.locator(
        "input[type='submit'], "
        "button:has-text('Import'), "
        "button:has-text('Upload'), "
        "button:has-text('Submit')"
    ).first
    if submit.count() > 0:
        submit.click()
        print("  Submitted import")

    page.wait_for_timeout(5000)
    print("  Fable import submitted.")
    return True
