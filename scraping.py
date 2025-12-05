from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from datetime import datetime, timedelta
import time
import random


def calculate_delay(scheduled_str, actual_str):
    if not scheduled_str or not actual_str or "N/A" in [scheduled_str, actual_str]:
        return None
    try:
        fmt = "%H:%M"
        t_sched = datetime.strptime(scheduled_str, fmt)
        t_act = datetime.strptime(actual_str, fmt)
        if t_act < t_sched and (t_sched.hour - t_act.hour) > 12:
            t_act += timedelta(days=1)
        elif t_sched < t_act and (t_act.hour - t_sched.hour) > 12:
            t_sched += timedelta(days=1)
        return int((t_act - t_sched).total_seconds() / 60)
    except:
        return None


def clean_status(text):
    if not text: return "N/A"
    if ":" in text:
        return text.split(":")[-1].strip().replace('"', '')
    return text.strip()


def get_flight_data(flight_code: str, target_date: str):
    # --- CONFIGURATION SPÉCIALE POUR STREAMLIT CLOUD ---
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")

    # User-Agent pour passer inaperçu
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")

    # Installation automatique du bon Chromium
    try:
        service = Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        # Fallback si webdriver_manager échoue (parfois sur le cloud)
        driver = webdriver.Chrome(options=chrome_options)

    url = f"https://airportinfo.live/fr/vol/{flight_code.lower()}?d={target_date}"

    data = {
        "flight_code": flight_code.upper(),
        "query_date": target_date,
        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "url": url,
        "status": "N/A",
        "origin": "N/A",
        "destination": "N/A",
        "departure": {"planned": "N/A", "actual": "N/A", "delay_min": None},
        "arrival": {"planned": "N/A", "actual": "N/A", "delay_min": None}
    }

    try:
        driver.get(url)
        time.sleep(2)  # Attente courte mais nécessaire

        # 1. Aéroports
        try:
            data["origin"] = driver.find_element(By.CLASS_NAME, "landingCounter_from").text.strip()
        except:
            pass
        try:
            data["destination"] = driver.find_element(By.CLASS_NAME, "landingCounter_to").text.strip()
        except:
            pass

        # 2. Statut
        try:
            stat_el = driver.find_element(By.CLASS_NAME, "flightstatusvalue")
            data["status"] = clean_status(stat_el.text)
        except:
            pass

        # 3. Horaires
        try:
            data["departure"]["planned"] = driver.find_element(By.CSS_SELECTOR,
                                                               "div.c1_3.planned_dep div.important_time").text.strip()
        except:
            pass
        try:
            data["departure"]["actual"] = driver.find_element(By.CSS_SELECTOR,
                                                              "div.c1_3.actual_dep div.important_time").text.strip()
        except:
            pass
        try:
            data["arrival"]["planned"] = driver.find_element(By.CSS_SELECTOR,
                                                             "div.c3_5.planned_arr div.important_time").text.strip()
        except:
            pass
        try:
            data["arrival"]["actual"] = driver.find_element(By.CSS_SELECTOR,
                                                            "div.c3_5.actual_arr div.important_time").text.strip()
        except:
            pass

        # 4. Calculs
        data["departure"]["delay_min"] = calculate_delay(data["departure"]["planned"], data["departure"]["actual"])
        data["arrival"]["delay_min"] = calculate_delay(data["arrival"]["planned"], data["arrival"]["actual"])

        if data["origin"] == "N/A" and data["destination"] == "N/A":
            data["status"] = "Vol non trouvé ou date invalide"

    except Exception as e:
        data["status"] = f"Erreur: {str(e)}"

    finally:
        driver.quit()

    return data