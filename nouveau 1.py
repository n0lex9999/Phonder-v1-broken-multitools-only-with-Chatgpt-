import requests
import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor
from time import sleep

# Fonction pour envoyer la commande HTTP au projecteur
def send_command(projector_ip, command):
    try:
        url = f"http://{projector_ip}/control?command={command}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Si la réponse HTTP est une erreur, une exception sera levée
        if response.status_code == 200:
            print(f"Commande '{command}' envoyée au projecteur {projector_ip} avec succès.")
        else:
            print(f"Erreur lors de l'envoi de la commande au projecteur {projector_ip}. Code: {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"Erreur de connexion : Timeout lors de la tentative de connexion à {projector_ip}.")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'envoi de la commande au projecteur {projector_ip}: {e}")


# Fonction pour effectuer un ping à l'adresse IP et vérifier si l'hôte est actif
def ping(host):
    try:
        # Adaptation en fonction du système d'exploitation
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", host]
        subprocess.check_call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

# Fonction pour découvrir les appareils actifs sur le réseau local avec multithreading
def discover_projectors(network_range):
    print(f"Scanne le réseau pour trouver les projecteurs sur le réseau {network_range}...")
    projectors = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        # Lancer un thread pour chaque IP
        futures = {executor.submit(ping, f"{network_range}.{i}"): i for i in range(1, 255)}
        for future in futures:
            ip = f"{network_range}.{futures[future]}"
            if future.result():  # Si l'IP répond au ping
                print(f"Dispositif trouvé à l'adresse IP {ip}")
                projectors.append(ip)
    return projectors

# Fonction pour afficher et choisir la marque du projecteur
def choose_projector_brand():
    print("\n--- Choisissez une marque de projecteur ---")
    brands = [
        "Acer", "Epson", "BenQ", "ViewSonic", "Optoma", "Sony", "LG", "Panasonic", 
        "Samsung", "Philips", "Hitachi", "Casio", "Sharp", "Vivitek"
    ]  # Liste des marques possibles
    for idx, brand in enumerate(brands, 1):
        print(f"{idx}. {brand}")

    choice = input("\nEntrez le numéro de la marque de projecteur ou 'q' pour quitter : ")

    if choice.lower() == 'q':
        print("Quitter le programme.")
        return None
    try:
        choice = int(choice)
        if 1 <= choice <= len(brands):
            return brands[choice - 1]
        else:
            print("Choix invalide.")
            return None
    except ValueError:
        print("Veuillez entrer un numéro valide.")
        return None

# Fonction principale pour exécuter le programme
def main():
    brand = choose_projector_brand()
    if not brand:
        return

    network_range = "192.168.1"  # Remplacez par le sous-réseau correct si nécessaire
    projectors = discover_projectors(network_range)

    if not projectors:
        print("Aucun projecteur trouvé sur le réseau.")
        return
    
    # Affiche la liste des projecteurs trouvés
    print("\n--- Projecteurs disponibles ---")
    for idx, ip in enumerate(projectors, 1):
        print(f"{idx}. {ip}")
    
    # Demande à l'utilisateur de choisir un projecteur
    choice = input("\nChoisissez un projecteur par son numéro (ou 'q' pour quitter, 'all' pour tout éteindre) : ")

    if choice.lower() == 'q':
        print("Quitter le programme.")
        return
    elif choice.lower() == 'all':
        # Envoie la commande "power_off" à tous les projecteurs
        for ip in projectors:
            send_command(ip, "power_off")
        return

    try:
        choice = int(choice)
        if 1 <= choice <= len(projectors):
            selected_ip = projectors[choice - 1]
            print(f"Vous avez sélectionné : {selected_ip}")
            
            # Menu de commandes pour le projecteur sélectionné
            while True:
                print("\n--- Commandes pour le projecteur ---")
                print("1. Allumer le projecteur")
                print("2. Éteindre le projecteur")
                print("3. Quitter")
                command_choice = input("Choisissez une commande : ")

                if command_choice == "1":
                    send_command(selected_ip, "power_on")
                elif command_choice == "2":
                    send_command(selected_ip, "power_off")
                elif command_choice == "3":
                    print("Quitter le programme.")
                    break
                else:
                    print("Option invalide. Essayez à nouveau.")
        else:
            print("Choix invalide.")
    except ValueError:
        print("Veuillez entrer un numéro valide.")
    except Exception as e:
        print(f"Erreur inattendue : {e}")

if __name__ == "__main__":
    main()
