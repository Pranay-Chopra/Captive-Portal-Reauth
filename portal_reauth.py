import time
import logging
import subprocess
import requests
from systemd.journal import JournalHandler

# ---- CONFIG ----
CHECK_URL = "http://connectivitycheck.gstatic.com/generate_204"
CHECK_INTERVAL = 60
LOGIN_URL = "https://172.22.2.6/connect/PortalMain"
USERNAME = "USERNAME_PLACEHOLDER"
PASSWORD = "PASSWORD_PLACEHOLDER"

# ---- LOGGING SETUP ----
logger = logging.getLogger("portal-reauth")
logger.setLevel(logging.INFO)

journal_handler = JournalHandler()
journal_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logger.addHandler(journal_handler)

# ---- CONNECTIVITY CHECK ----
def is_connected():
    try:
        r = requests.get(CHECK_URL, timeout=5)
        if r.status_code == 204:
            return True
        else:
            logger.warning(f"Unexpected status: {r.status_code}")
            return False
    except Exception as e:
        logger.warning(f"Connectivity check failed: {e}")
        return False

# ---- REAUTH USING PLAYWRIGHT ----
def reauthenticate():
    logger.info("Starting reauthentication")

    try:
        subprocess.run([
            "python3", "-c",
            f"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()
    page.goto("{LOGIN_URL}")
    page.wait_for_timeout(2000)
    
    # page.click("#UserCheck_Logoff_Button")
    # page.wait_for_timeout(2000)
    # page.click(".portal_link")
    # page.wait_for_timeout(2000)

    page.fill("#LoginUserPassword_auth_username", "{USERNAME}")
    page.fill("#LoginUserPassword_auth_password", "{PASSWORD}")

    page.click("#UserCheck_Login_Button")
    page.wait_for_timeout(5000)

    browser.close()
"""
        ], check=True)

        logger.info("Reauthentication completed")

    except subprocess.CalledProcessError as e:
        logger.error(f"Reauthentication failed: {e}")

# ---- MAIN LOOP ----
def main():
    logger.info("Portal reauth daemon started")

    while True:
        if not is_connected():
            logger.warning("Connection lost. Attempting reauth...")
            reauthenticate()
        else:
            logger.debug("Connection OK")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
