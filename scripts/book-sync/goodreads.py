"""Playwright automation for Goodreads CSV import."""
from pathlib import Path
from playwright.sync_api import Page, BrowserContext

import config

GOODREADS_URL = "https://www.goodreads.com"


def _ensure_dirs():
    config.GOODREADS_AUTH.parent.mkdir(parents=True, exist_ok=True)


def get_context(playwright):
    """Get a browser context, reusing saved auth if available."""
    _ensure_dirs()
    browser = playwright.chromium.launch(headless=config.HEADLESS)
    if config.GOODREADS_AUTH.exists():
        context = browser.new_context(storage_state=str(config.GOODREADS_AUTH))
    else:
        context = browser.new_context()
    return context


def save_auth(context: BrowserContext):
    _ensure_dirs()
    context.storage_state(path=str(config.GOODREADS_AUTH))


def ensure_logged_in(page: Page) -> bool:
    """Navigate to Goodreads and check login. Pauses for manual login if needed."""
    page.goto(GOODREADS_URL)
    page.wait_for_load_state("networkidle")

    logged_in_selectors = [
        "nav.siteHeader__primaryNavInline",
        "[data-testid='userMenu']",
        "a[href*='/review/list']",
        ".dropdown__trigger--profileButton",
        ".personalNav",
    ]
    for sel in logged_in_selectors:
        if page.locator(sel).count() > 0:
            print("  Goodreads: logged in ✓")
            return True

    if config.HEADLESS:
        print("  ERROR: Goodreads not logged in. Run ./login.sh first.")
        return False

    print("\n  Goodreads: not logged in.")
    print("  Please log in manually in the browser window.")
    print("  Press Enter here once done...")
    input()
    return True


def import_csv(page: Page, csv_path: Path):
    """Upload a CSV file to Goodreads import."""
    page.goto(f"{GOODREADS_URL}/review/import")
    page.wait_for_load_state("networkidle")

    file_input = page.locator("input[type='file']").first
    if file_input.count() == 0:
        print("  ERROR: Could not find file input on Goodreads import page")
        return False

    file_input.set_input_files(str(csv_path))
    print(f"  Uploaded {csv_path.name} to Goodreads")

    page.wait_for_timeout(2000)

    submit = page.locator(
        "input[type='submit'], "
        "button:has-text('Import'), "
        "button:has-text('Upload')"
    ).first
    if submit.count() > 0:
        submit.click()
        print("  Submitted import")

    page.wait_for_timeout(5000)
    print("  Goodreads import submitted.")
    return True
