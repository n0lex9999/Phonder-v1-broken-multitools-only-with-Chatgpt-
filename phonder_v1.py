import os
import shodan
import socket
import pywifi
import requests

# Clear the console based on the operating system
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

# Display the banner
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

# Shodan scanner
def run_shodan():
    while True:
        api_key = input("Entrez votre clé API Shodan : ").strip()
        
        if not api_key:
            print("La clé API ne peut pas être vide. Veuillez entrer une clé API valide.")
            continue
        
        try:
            api = shodan.Shodan(api_key)
            api.info()  # Test the API key
            break

        except shodan.APIError:
            print("Clé API invalide. Veuillez réessayer.")
    
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
        print(f"Erreur Shodan: {e}")

# WiFi scanner using pywifi
def scan_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]  # Get the first wireless interface
    iface.scan()  # Start scanning
    results = iface.scan_results()
    
    print("Réseaux WiFi trouvés :")
    for network in results:
        print(f"SSID: {network.ssid}, Signal: {network.signal}, Auth: {network.auth}")

# IP scanner (scans for open ports)
def scan_ip():
    ip = input("Entrez l'adresse IP à scanner : ")
    try:
        for port in range(20, 1025):  # Scanning ports from 20 to 1024
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(f"Port {port} est ouvert.")
            sock.close()
    except socket.error:
        print("Erreur de connexion à l'IP.")

# Website scanner using requests
def scan_website():
    url = input("Entrez l'URL du site Web à analyser (ex: http://example.com) : ")
    try:
        response = requests.get(url)
        print(f"Statut HTTP pour {url}: {response.status_code}")
        print(f"En-têtes HTTP: {response.headers}")
    except requests.RequestException as e:
        print(f"Erreur lors de l'accès au site Web : {e}")

# Main menu
def menu():
    print("""
        ╔════════════(1) Shodan
        ║════════════(2) Scan WiFi
        ║════════════(3) Scan IP
        ║════════════(4) Scan de site Web
        ║
        ╚═══(99) exit
    """)

# Start program based on user's choice
def start_program(option):
    if option == "1":
        run_shodan()
    elif option == "2":
        scan_wifi()
    elif option == "3":
        scan_ip()
    elif option == "4":
        scan_website()
    elif option == "99":
        print("Fermeture du programme...")
        exit()
    else:
        print(f"'{option}' ne correspond à aucune commande. Veuillez réessayer.")


# Main loop
def main():
    clear_console()
    banner()
    while True:
        menu()
        choice = input("╚═════> ")
        start_program(choice)

# Entry point
if __name__ == "__main__":
    main()
