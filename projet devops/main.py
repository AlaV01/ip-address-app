"""Point d'entree : relie IPClient -> IPInfo -> Display.

Lancer le programme :  python main.py
"""
from ip_client import IPClient, APIError
from ip_info import IPInfo
from display import Display


class Application:
    """Controle le programme : menu, appels a l'API et affichage."""

    def __init__(self):
        self._client = IPClient()
        self._display = Display()

    def show_ipv4(self):
        ip = self._client.get_ipv4()
        self._display.show_ip(4, ip)

    def show_ipv6(self):
        ip = self._client.get_ipv6()
        # api64.ipify.org renvoie une IPv4 si le reseau n'a pas d'IPv6
        if IPInfo(ip).ip_version != 6:
            self._display.show_message("Aucune adresse IPv6 disponible sur ce reseau.")
            return
        self._display.show_ip(6, ip)

    def show_details(self):
        ip = self._client.get_ipv4()
        data = self._client.get_details(ip)
        # ipinfo.io appelle le fournisseur "org" ; IPInfo l'appelle "isp"
        info = IPInfo(
            ip=ip,
            city=data.get("city"),
            region=data.get("region"),
            country=data.get("country"),
            isp=data.get("org"),
            timezone=data.get("timezone"),
            loc=data.get("loc"),
        )
        self._display.show_table(info.to_dict())

    def run(self):
        actions = {
            "1": self.show_ipv4,
            "2": self.show_ipv6,
            "3": self.show_details,
        }
        while True:
            self._display.show_menu()
            choice = self._display.ask_choice()
            if choice == "0":
                self._display.show_message("Au revoir !")
                break
            action = actions.get(choice)
            if action is None:
                self._display.show_error("Choix invalide, reessayez.")
                continue
            try:
                action()
            except (APIError, ValueError) as error:
                self._display.show_error(error)


if __name__ == "__main__":
    Application().run()
