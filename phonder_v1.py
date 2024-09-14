import os
import shodan
import nmap  # Assure-toi d'avoir le module python-nmap installé

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_colored_text(text):
    """Imprime le texte avec un dégradé de couleurs horizontal."""
    num_chars = len(text)
    # Dégradé de couleurs : Orange, Violet clair, Violet foncé
    colors = [208, 135, 55]  # Codes de couleur ANSI
    num_colors = len(colors)
    
    color_index = 0
    color_step = num_chars / (num_colors - 1) if num_colors > 1 else 1

    for i, char in enumerate(text):
        # Déterminer la couleur en fonction de la position
        if i >= color_step * (color_index + 1):
            color_index += 1
            if color_index >= num_colors:
                color_index = num_colors - 1
        color_code = colors[color_index]
        print(f"\033[38;5;{color_code}m{char}\033[0m", end="")
    print("\033[0m")  # Réinitialiser la couleur

def banner():
    text = """
        ██████╗ ██╗  ██╗ ██████╗ ███╗   ██╗██████╗ ███████╗██████╗     ██╗   ██╗ ██╗
        ██╔══██╗██║  ██║██╔═══██╗████╗  ██║██╔══██╗██╔════╝██╔══██╗    ██║   ██║███║
        ██████╔╝███████║██║   ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝    ██║   ██║╚██║
        ██╔═══╝ ██╔══██║██║   ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗    ╚██╗ ██╔╝ ██║
        ██║     ██║  ██║╚██████╔╝██║ ╚████║██████╔╝███████╗██║  ██║     ╚████╔╝  ██║
        ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝      ╚═══╝   ╚═╝
                    --𝐁𝐲 𝐍𝟎𝐥𝐞𝐱𝟙𝟗𝟗𝟗--
    """
    print_colored_text(text)

def menu():
    """Affiche le menu avec un dégradé de couleurs horizontal."""
    menu_text = """\
        ╔════════════(1) Shodan
        ║
        ╔════════════(2) Scanner IP
        ║
        ╔════════════(3) Identifier un Wi-Fi
        ║
        ╚═══(99) exit
    """
    print_colored_text(menu_text)

def run_shodan():
    api_key = input("Entrez votre clé API Shodan : ")
    domain = input("Entrez le nom de domaine pour la recherche Shodan : ")
    try:
        api = shodan.Shodan(api_key)
        response = api.host(domain)
        
        # Afficher la réponse brute pour déboguer
        print("Réponse brute de Shodan:")
        print(response)
        
        # Afficher les résultats
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
    except ValueError as e:
        print(f"Erreur de traitement des données : {e}")

def scan_ip(ip_address):
    """Scanner les ports d'une IP."""
    nm = nmap.PortScanner()
    print(f"Scanning IP: {ip_address}...")
    nm.scan(ip_address, arguments='-T4 -F')  # Utilisation d'arguments pour scanner les ports
    print(f"Scan complet pour IP {ip_address}:")
    print(nm.csv())

def identify_wifi():
    """Identifier les réseaux Wi-Fi disponibles."""
    if os.name == 'nt':  # Pour Windows
        os.system('netsh wlan show networks mode=Bssid')
    else:  # Pour Linux
        os.system('nmcli dev wifi list')

def start_program(option):
    if option == "1":
        run_shodan()
    elif option == "2":
        ip_address = input("Entrez l'adresse IP à scanner : ")
        scan_ip(ip_address)
    elif option == "3":
        identify_wifi()
    elif option == "99":
        exit()
    else:
        print(f"'{option}' ne correspond à aucune commande. Merci de retenter avec autre chose.")
        main()

def main():
    clear_console()
    banner()
    while True:
        menu()
        choice = input("╚═════> ")
        start_program(choice)

if __name__ == "__main__":
    main()
