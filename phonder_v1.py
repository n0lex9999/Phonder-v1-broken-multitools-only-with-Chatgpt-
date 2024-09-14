import os
import shodan
import socket
import pywifi
from pywifi import const
import requests
import logging
import traceback

# Setup logging to capture detailed crash reports
logging.basicConfig(filename='debug_log.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    print("""
        ██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗██████╗ ███████╗██████╗     ██╗   ██╗ ██╗
        ██╔══██╗██║  ██║██╔═══██╗████╗  ██║██╔══██╗██╔════╝██╔══██╗    ██║   ██║███║
        ██████╔╝███████║██║   ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝    ██║   ██║╚██║
        ██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗    ╚██╗ ██╔╝ ██║
        ██║     ██║  ██║╚██████╔╝██║ ╚████║██████╔╝███████╗██║  ██║     ╚████╔╝  ██║
        ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝      ╚═══╝   ╚═╝
                    --𝐁𝐲 𝐍𝟎𝐥𝐞𝐱𝟙𝟡𝟡𝟡--
    """)

# Function to run Shodan search with consistent error handling
def run_shodan():
    while True:
        try:
            api_key = input("Entrez votre clé API Shodan : ").strip()
            if not api_key:
                print("La clé API ne peut pas être vide. Veuillez entrer une clé API valide.")
                continue

            # Initialize Shodan API
            api = shodan.Shodan(api_key)
            api.info()  # Test API key validity
            break  # If API key is valid, exit loop
        except shodan.APIError as e:
            logging.error(f"Erreur API Shodan: {e}")
            print("Clé API invalide. Veuillez réessayer.")
        except Exception as e:
            logging.error(f"Unexpected error in run_shodan: {e}")
            print(f"Une erreur inattendue s'est produite : {e}")
            logging.error(traceback.format_exc())

    # Domain scan with Shodan
    domain = input("Entrez le nom de domaine pour la recherche Shodan : ")
    try:
        response = api.host(domain)
        print(f"Résultats pour '{domain}':")
        print(f"IP: {response['ip_str']}")
        print(f"Organisation: {response.get('org', 'Non spécifié')}")
        print(f"Ville: {response.get('city', 'Non spécifié')}")
        print(f"Pays: {response.get('country_name', 'Non spécifié')}")
        print(f"Ports ouverts: {', '.join(str(port) for port in response.get('ports', []))}")
        print(f"Hostname: {', '.join(response.get('hostnames', []))}")
        print(f"Data: {response.get('data', 'Aucune donnée')}")
    except shodan.APIError as e:
        logging.error(f"Erreur lors de la recherche Shodan: {e}")
        print(f"Erreur Shodan: {e}")
    except Exception as e:
        logging.error(f"Erreur inattendue dans run_shodan: {e}")
        print(f"Une erreur inattendue s'est produite : {e}")
        logging.error(traceback.format_exc())

# Function for WiFi scanning with error handling
def scan_wifi():
    try:
        wifi = pywifi.PyWiFi()
        iface = wifi.interfaces()[0]  # Get first wireless interface
        iface.scan()  # Start scan
        results = iface.scan_results()

        print("Réseaux WiFi trouvés :")
        for network in results:
            print(f"SSID: {network.ssid}, Signal: {network.signal}, Auth: {network.auth}")
    except IndexError:
        print("Erreur: Aucun adaptateur WiFi trouvé.")
        logging.error("Erreur: Aucun adaptateur WiFi trouvé.")
    except Exception as e:
        logging.error(f"Erreur dans le scan WiFi: {e}")
        print(f"Erreur dans le scan WiFi: {e}")
        logging.error(traceback.format_exc())

# Function for IP scan
def scan_ip():
    try:
        ip = input("Entrez l'adresse IP à scanner : ")
        for port in range(20, 1025):  # Scan ports 20 to 1024
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(f"Port {port}: Ouvert")
            sock.close()
    except socket.error as e:
        logging.error(f"Erreur lors de la connexion: {e}")
        print(f"Erreur de connexion à l'IP : {e}")
        logging.error(traceback.format_exc())

# Function for IntelX scanning
def scan_site_intelx():
    try:
        intelx_key = input("Entrez votre clé API IntelX : ").strip()
        domain = input("Entrez le nom de domaine à analyser : ")

        url = f"https://2.intelx.io/intelx/search?k={intelx_key}&q={domain}&maxresults=10"
        response = requests.get(url)
        data = response.json()

        print(f"Données récupérées pour {domain}: {data}")
    except requests.RequestException as e:
        logging.error(f"Erreur lors de la requête IntelX : {e}")
        print(f"Erreur lors de la requête IntelX : {e}")
        logging.error(traceback.format_exc())
    except Exception as e:
        logging.error(f"Erreur inattendue dans scan_site_intelx: {e}")
        print(f"Erreur inattendue lors de l'analyse IntelX: {e}")
        logging.error(traceback.format_exc())

# Function for SQL injection scan
def scan_sql():
    try:
        url = input("Entrez l'URL pour tester l'injection SQL : ")
        payloads = ["'", "' OR '1'='1", "' OR '1'='1' --", '"', '" OR "1"="1', '" OR "1"="1" --']

        for payload in payloads:
            full_url = url + payload
            response = requests.get(full_url)
            if "error" in response.text.lower() or "sql" in response.text.lower():
                print(f"Possibilité d'injection SQL avec le payload : {payload}")
    except requests.RequestException as e:
        logging.error(f"Erreur lors de la requête SQL : {e}")
        print(f"Erreur lors de la requête SQL : {e}")
        logging.error(traceback.format_exc())
    except Exception as e:
        logging.error(f"Erreur inattendue dans scan_sql: {e}")
        print(f"Erreur inattendue lors du scan SQL: {e}")
        logging.error(traceback.format_exc())

# Function for Discord account scan
def scan_discord_account():
    try:
        token = input("Entrez votre token Discord : ")
        headers = {"Authorization": token}
        response = requests.get("https://discord.com/api/v9/users/@me", headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            print(f"Utilisateur: {user_data['username']}#{user_data['discriminator']}")
            print(f"ID: {user_data['id']}")
            print(f"Email:
