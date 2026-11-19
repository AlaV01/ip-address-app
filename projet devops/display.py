class Display:
    """Gère tout l'affichage console."""

    WIDTH = 44

    def __init__(self, title="IP Address Application"):
        self._title = title

    def show_menu(self):
        print("=" * self.WIDTH)
        print(self._title.center(self.WIDTH))
        print("=" * self.WIDTH)
        print("1. Afficher mon IPv4 publique")
        print("2. Afficher mon IPv6 publique")
        print("3. Afficher les informations de localisation")
        print("0. Quitter")

    def ask_choice(self):
        return input("Votre choix : ").strip()

    def show_ip(self, version, ip):
        print(f"\nIPv{version} publique : {ip}")

    def show_table(self, data):
        """Affiche un dict sous forme de tableau."""
        if not data:
            print("Aucune donnée.")
            return
        key_w = max(len(str(k)) for k in data)
        line = "+" + "-" * (key_w + 2) + "+" + "-" * (self.WIDTH - key_w) + "+"
        print(line)
        for key, value in data.items():
            print(f"| {str(key):<{key_w}} | {str(value):<{self.WIDTH - key_w - 2}} |")
        print(line)

    def show_error(self, message):
        print(f"\n[ERREUR] {message}")

    def show_message(self, message):
        print(f"\n{message}")