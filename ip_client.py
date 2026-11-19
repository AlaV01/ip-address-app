
import requests


class APIError(Exception):
    """Exception personnalisée pour les erreurs de l'API."""
    pass


class IPClient:
    """Classe responsable de la communication avec les API REST."""

    def __init__(self):
        self.__base_url = "https://ipinfo.io"

    def get_ipv4(self):
        """Récupérer l'adresse IPv4 publique."""
        try:
            response = requests.get(
                "https://api.ipify.org?format=json",
                timeout=10
            )

            response.raise_for_status()
            data = response.json()

            return data["ip"]

        except requests.ConnectionError:
            raise APIError("Erreur de connexion Internet.")

        except requests.Timeout:
            raise APIError("Le délai de connexion est dépassé.")

        except requests.HTTPError as e:
            raise APIError(f"Erreur HTTP : {e}")

        except (ValueError, KeyError):
            raise APIError("Réponse IPv4 invalide.")

    def get_ipv6(self):
        """Récupérer une adresse IP via l'API IPv6-compatible."""
        try:
            response = requests.get(
                "https://api64.ipify.org?format=json",
                timeout=10
            )

            response.raise_for_status()
            data = response.json()

            return data["ip"]

        except requests.ConnectionError:
            raise APIError("Erreur de connexion Internet.")

        except requests.Timeout:
            raise APIError("Le délai de connexion est dépassé.")

        except requests.HTTPError as e:
            raise APIError(f"Erreur HTTP : {e}")

        except (ValueError, KeyError):
            raise APIError("Réponse IP invalide.")

    def get_details(self, ip):
        """Récupérer les informations détaillées d'une adresse IP."""
        try:
            url = f"{self.__base_url}/{ip}/json"

            response = requests.get(url, timeout=10)

            response.raise_for_status()
            data = response.json()

            if data.get("bogon"):
                raise APIError("Adresse IP privée ou réservée.")

            return data

        except requests.ConnectionError:
            raise APIError("Erreur de connexion Internet.")

        except requests.Timeout:
            raise APIError("Le délai de connexion est dépassé.")

        except requests.HTTPError as e:
            raise APIError(f"Erreur HTTP : {e}")

        except ValueError:
            raise APIError("Réponse JSON invalide.")
