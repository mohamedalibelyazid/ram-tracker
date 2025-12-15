from fastapi import FastAPI, HTTPException, Query
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import time

app = FastAPI(
    title="RAM Flight Tracker API",
    description="API pour suivre les vols Royal Air Maroc. Utilisez ?d=YYYY-MM-DD"
)


# --- FONCTIONS UTILITAIRES ---

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
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    url = f"https://airportinfo.live/fr/vol/{flight_code.lower()}?d={target_date}"

    # Structure de données mise à jour avec 'planned_local'
    data = {
        "flight_code": flight_code.upper(),
        "query_date": target_date,
        "scraped_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "url": url,
        "status": "N/A",
        "origin": "N/A",
        "destination": "N/A",
        "departure": {
            "planned": "N/A",
            "planned_local": "N/A",  # Nouveau champ
            "actual": "N/A",
            "delay_min": None
        },
        "arrival": {
            "planned": "N/A",
            "planned_local": "N/A",  # Nouveau champ
            "actual": "N/A",
            "delay_min": None
        }
    }

    try:
        driver.get(url)
        time.sleep(2.5)  # Idéalement, remplacez ceci par WebDriverWait pour plus de rapidité

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

        # 3. Horaires (Départ)
        try:
            data["departure"]["planned"] = driver.find_element(By.CSS_SELECTOR,
                                                               "div.c1_3.planned_dep div.important_time").text.strip()
        except:
            pass

        # --- NOUVEAU : Heure locale de départ ---
        try:
            # Basé sur l'image image_a02673.png
            data["departure"]["planned_local"] = driver.find_element(By.CLASS_NAME,
                                                                     "departureScheduledTimeLocal").text.strip()
        except:
            pass

        try:
            data["departure"]["actual"] = driver.find_element(By.CSS_SELECTOR,
                                                              "div.c1_3.actual_dep div.important_time").text.strip()
        except:
            pass

        # 4. Horaires (Arrivée)
        try:
            data["arrival"]["planned"] = driver.find_element(By.CSS_SELECTOR,
                                                             "div.c3_5.planned_arr div.important_time").text.strip()
        except:
            pass

        # --- NOUVEAU : Heure locale d'arrivée ---
        try:
            # Basé sur l'image image_a02635.png
            data["arrival"]["planned_local"] = driver.find_element(By.CLASS_NAME,
                                                                   "arrivalScheduledTimeLocal").text.strip()
        except:
            pass

        try:
            data["arrival"]["actual"] = driver.find_element(By.CSS_SELECTOR,
                                                            "div.c3_5.actual_arr div.important_time").text.strip()
        except:
            pass

        # 5. Calculs
        data["departure"]["delay_min"] = calculate_delay(data["departure"]["planned"], data["departure"]["actual"])
        data["arrival"]["delay_min"] = calculate_delay(data["arrival"]["planned"], data["arrival"]["actual"])

        if data["origin"] == "N/A" and data["destination"] == "N/A":
            data["status"] = "Vol non trouvé ou date invalide"

    except Exception as e:
        print(f"Erreur: {e}")
        data["status"] = "Erreur technique"
    finally:
        driver.quit()

    return data


# --- ROUTE ---

@app.get("/flight/{flight_number}")
def read_flight(
        flight_number: str,
        d: str = Query(None, description="Date au format YYYY-MM-DD (ex: 2025-01-31).")
):
    code = flight_number.replace(" ", "").upper()
    if not code.startswith("AT") and code.isdigit():
        code = f"AT{code}"

    if d:
        try:
            datetime.strptime(d, "%Y-%m-%d")
            target_date = d
        except ValueError:
            return {"error": "Format invalide pour 'd'. Utilisez YYYY-MM-DD"}
    else:
        target_date = datetime.now().strftime("%Y-%m-%d")

    return get_flight_data(code, target_date)