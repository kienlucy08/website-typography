from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()
URL = os.getenv("FIELDSYNC_URL")
EMAIL = os.getenv("MS_EMAIL")
PASSWORD = os.getenv("MS_PASSWORD")

# Set up Chrome browser
options = Options()
# options.add_argument("--headless")  # Uncomment if running in background
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 30)

# STEP 1: Go to login page
driver.get(URL)
time.sleep(1)

# STEP 2: Click "Sign in with Microsoft"
ms_button = wait.until(EC.element_to_be_clickable(
    (By.XPATH, "//button[contains(text(),'Microsoft')]")))
ms_button.click()
time.sleep(1)

# STEP 3: Enter Email
email_input = wait.until(EC.presence_of_element_located((By.NAME, "loginfmt")))
email_input.send_keys(EMAIL)
driver.find_element(By.ID, "idSIButton9").click()  # Click Next
time.sleep(1)

# STEP 4: Enter Password
password_input = wait.until(
    EC.presence_of_element_located((By.NAME, "passwd")))
password_input.send_keys(PASSWORD)
driver.find_element(By.ID, "idSIButton9").click()  # Click Sign In
time.sleep(1)

# STEP 5: Accept permissions prompt (if shown)
try:
    # Wait for the Accept button to be present and clickable
    accept_btn = wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//input[@type='submit' and @value='Accept']"))
    )
    accept_btn.click()
    print("✅ Permissions accepted.")
    time.sleep(5)
except:
    print("ℹ️ No permissions screen appeared (already accepted or skipped).")


# Final Wait: Let app fully load
time.sleep(10)

print("✅ Logged in and app loaded!")

# STEP: Click the first "Plumb & Twist" survey link
# STEP: Click the first "Plumb & Twist" link
try:
    plumb_link = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//a[contains(text(),'Plumb & Twist')]")
    ))
    print("✅ Found and clicking 'Plumb & Twist' link...")
    plumb_link.click()
    time.sleep(6)  # Adjust as needed to ensure the new page loads
except Exception as e:
    print(f"❌ Couldn't find or click 'Plumb & Twist' link: {e}")
    driver.quit()


# Optionally keep open or scrape from here
# driver.quit()

# Define the output file
output_file = "typography.txt"

# Open file in append mode (create if not exists)
with open("typography.txt", "a", encoding="utf-8") as f:
    elements = driver.find_elements(
        By.CSS_SELECTOR, "h1, h2, h3, p, div, span, button, label, td, th")

    for el in elements:
        try:
            text = el.text.strip()
            if not text:
                continue

            font = driver.execute_script(
                "return getComputedStyle(arguments[0]).fontFamily;", el)
            size_px = driver.execute_script(
                "return getComputedStyle(arguments[0]).fontSize;", el)
            weight = driver.execute_script(
                "return getComputedStyle(arguments[0]).fontWeight;", el)
            style = driver.execute_script(
                "return getComputedStyle(arguments[0]).fontStyle;", el)
            line_height_px = driver.execute_script(
                "return getComputedStyle(arguments[0]).lineHeight;", el)
            color = driver.execute_script(
                "return getComputedStyle(arguments[0]).color;", el)

            padding_top = driver.execute_script(
                "return getComputedStyle(arguments[0]).paddingTop;", el)
            padding_right = driver.execute_script(
                "return getComputedStyle(arguments[0]).paddingRight;", el)
            padding_bottom = driver.execute_script(
                "return getComputedStyle(arguments[0]).paddingBottom;", el)
            padding_left = driver.execute_script(
                "return getComputedStyle(arguments[0]).paddingLeft;", el)

            def px_to_float(val):
                try:
                    return float(val.replace('px', ''))
                except:
                    return None

            size_val = px_to_float(size_px)
            line_val = px_to_float(line_height_px)
            line_ratio = round(line_val / size_val,
                               2) if size_val and line_val else "N/A"

            f.write(f"--- Plumb & Twist Survey Typography ---\n")
            f.write(f"Text: {text[:40]}\n")
            f.write(f"  Font Family: {font}\n")
            f.write(f"  Font Size: {size_px}\n")
            f.write(f"  Font Weight: {weight}\n")
            f.write(f"  Font Style: {style}\n")
            f.write(f"  Line Height: {line_height_px} (Ratio: {line_ratio})\n")
            f.write(f"  Color: {color}\n")
            f.write(
                f"  Padding: top {padding_top}, right {padding_right}, bottom {padding_bottom}, left {padding_left}\n")
            f.write("-" * 60 + "\n")

        except Exception as e:
            f.write(f"Error extracting element: {e}\n")
            continue


driver.quit()
