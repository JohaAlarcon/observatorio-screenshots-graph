import os
import shutil
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Load configurations from `credentials.json`.
with open("credentials.json", "r") as file:
    config = json.load(file)

USERNAME = config["username"]
PASSWORD = config["password"]
CARPETA_DESTINO = config["ruta_destino"]
URLS = config["urls"]

# Chrome service settings
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

def iniciar_sesion():
    """Inicia sesión en la página web."""
    driver.get(URLS[0]["url"])  # Open the first URL to login
    time.sleep(3)
    username_input = driver.find_element(By.NAME, "username")
    password_input = driver.find_element(By.NAME, "password")
    sign_in_button = driver.find_element(By.CSS_SELECTOR, 'button[title="Sign in"]')

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    sign_in_button.click()
    print("Inicio de sesión exitoso.")
    time.sleep(5)  # Additional wait to fully charge after login

def capturar_screenshot(name, url, container_type):
    """Captura el screenshot de la gráfica en la página especificada."""
    driver.get(url)
    time.sleep(5) # Wait for the page to load completely

    # Determine the selector according to the type of container
    if container_type == "chart-container":
        selector = '[data-testid="chart-container"]'
    elif container_type == "scalar-container":
        selector = '[data-testid="scalar-container"]'
    elif container_type == "chart-legend":
        selector = '[data-testid="chart-legend"]'
    else:
        print(f"Contenedor desconocido para la gráfica '{name}'")
        return

   # Wait for the graphic container to be present
    try:
        chart_container = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

        # Construct the file name based on the name provided in the JSON
        nombre_archivo = f"{name.replace(' ', '_').replace('/', '_')}.png"
        ruta_temporal = f"/tmp/{nombre_archivo}"
        ruta_guardado = os.path.join(CARPETA_DESTINO, nombre_archivo)

        # Take the screenshot and save it in the temp folder
        chart_container.screenshot(ruta_temporal)
        print(f"Captura temporal guardada en: {ruta_temporal}")

        # Create the destination folder if it does not exist
        if not os.path.isdir(CARPETA_DESTINO):
            os.makedirs(CARPETA_DESTINO, exist_ok=True)

         # Create the destination folder if it does not exist
        shutil.move(ruta_temporal, ruta_guardado)
        print(f"Captura movida a: {ruta_guardado}")

    except Exception as e:
        print(f"Error al capturar la gráfica '{name}': {e}")

def main():
    """Función principal para ejecutar el script."""
    iniciar_sesion()
    for item in URLS:
        name = item["name"]
        url = item["url"]
        container_type = item["container_type"]
        capturar_screenshot(name, url, container_type)

    # Close the browser
    driver.quit()
    print("Capturas completadas y navegador cerrado.")

if __name__ == "__main__":
    main()
