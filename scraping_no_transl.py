from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import os
import json

# === Setup Chrome session ===
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"
service = Service("C:/chromedriver/chromedriver.exe")
# if using macOS:
# service = Service("/opt/homebrew/bin/chromedriver")
# if using Linux:
# service = Service("/usr/bin/chromedriver")

driver = webdriver.Chrome(service=service, options=options)

# Run Chrome beforehand using (in terminal):
# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir=\"C:\selenium\chrome"

# if using macOS:
# /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug"

# if using Linux:
# google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome-debug"


# === Initialize seen dates ===
seen_dates_file = "seen_dates.txt"
if os.path.exists(seen_dates_file):
    with open(seen_dates_file, "r") as f:
        seen_dates = set(f.read().splitlines())
else:
    seen_dates = set()

# === Initialize JSONL checkpoint file ===
# select between one of the seven terms
# parliament_transcripts_94_99.jsonl
# parliament_transcripts_99_04.jsonl
# parliament_transcripts_04_09.jsonl
# parliament_transcripts_09_14.json
# parliament_transcripts_14_19.jsonl
# parliament_transcripts_19_24.json
# parliament_transcripts_24_25.jsonl
jsonl_file = "parliament_transcripts_19_24.jsonl"
if not os.path.exists(jsonl_file):
    open(jsonl_file, "w", encoding="utf-8").close()

# === Helper function to click "Full text" ===
def click_full_text():
    try:
        full_text_btn = driver.find_element(By.XPATH, "//a[contains(@title, 'Full text')]")
        full_text_btn.click()
        time.sleep(3)
    except:
        print("Full text button not found.")

# === Helper to extract sections and paragraphs (raw only) ===
def extract_sections():
    sections = []
    current_topic = None
    current_paragraphs = []

    rows = driver.find_elements(By.XPATH, "//table//tr")

    for row in rows:
        try:
            topic_cells = row.find_elements(By.CSS_SELECTOR, "td.doc_title")
            if topic_cells:
                # Always save the previous section (even if empty)
                sections.append({
                    "topic": current_topic,
                    "paragraphs": current_paragraphs
                })
                current_paragraphs = []
                current_topic = topic_cells[0].text.strip()
                continue

            paragraph_elements = row.find_elements(By.CSS_SELECTOR, "p.contents")
            for p in paragraph_elements:
                text = p.text.strip()
                if text:
                    current_paragraphs.append(text)
        except:
            continue

    # Save the last section too
    sections.append({
        "topic": current_topic,
        "paragraphs": current_paragraphs
    })

    return sections

# === Main scraping loop ===
while True:
    time.sleep(2)
    items = driver.find_elements(By.CSS_SELECTOR, "div.notice")
    found_new_date = False

    for item in items:
        try:
            link_tag = item.find_element(By.CSS_SELECTOR, "p.title a")
            date_tag = item.find_element(By.CSS_SELECTOR, "div.date_reference span.date")

            link = link_tag.get_attribute("href")
            date = date_tag.text.strip()

            if date not in seen_dates:
                print(f"Processing new date: {date}")
                seen_dates.add(date)

                driver.execute_script(f"window.open('{link}', '_blank');")
                time.sleep(2)
                while len(driver.window_handles) <= 1:
                    time.sleep(1)
                driver.switch_to.window(driver.window_handles[-1])

                click_full_text()
                sections = extract_sections()

                if sections:
                    record = {
                        "date": date,
                        "link": link,
                        "sections": sections
                    }
                    with open(jsonl_file, "a", encoding="utf-8") as f:
                        f.write(json.dumps(record, ensure_ascii=False) + "\n")
                    print(f"Saved discussion for {date} ({sum(len(s['paragraphs']) for s in sections)} paragraphs)")
                else:
                    print(f"No text found for {date}")

                with open(seen_dates_file, "a") as f:
                    f.write(date + "\n")

                driver.close()
                driver.switch_to.window(driver.window_handles[0])
                time.sleep(2)

                found_new_date = True
                break
        except:
            continue

    if not found_new_date:
        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "a.next_page[title='Display the next page']")
            next_button.click()
            time.sleep(3)
        except:
            print("No next button found. Done scraping.")
            break

print("Scraping complete.")
driver.quit()
