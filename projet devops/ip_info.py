
import ipaddress
import json


class IPInfo:

    def __init__(self, ip, city=None, region=None, country=None,
                 isp=None, timezone=None, loc=None):

        # Validation de l'adresse IP
        try:
            self.__ip = str(ipaddress.ip_address(ip))
        except ValueError:
            raise ValueError("Adresse IP invalide")

        # Attributs privés
        self.__city = city
        self.__region = region
        self.__country = country
        self.__isp = isp
        self.__timezone = timezone
        self.__loc = loc

    # Properties
    @property
    def ip(self):
        return self.__ip

    @property
    def city(self):
        return self.__city

    @property
    def region(self):
        return self.__region

    @property
    def country(self):
        return self.__country

    @property
    def isp(self):
        return self.__isp

    @property
    def timezone(self):
        return self.__timezone

    @property
    def loc(self):
        return self.__loc

    @property
    def ip_version(self):
        return ipaddress.ip_address(self.__ip).version

    # Affichage des informations
    def __str__(self):
        return (
            f"IP Address : {self.__ip}\n"
            f"City      : {self.__city}\n"
            f"Region    : {self.__region}\n"
            f"Country   : {self.__country}\n"
            f"ISP       : {self.__isp}\n"
            f"Timezone  : {self.__timezone}\n"
            f"Location  : {self.__loc}\n"
            f"IP Version: IPv{self.ip_version}"
        )

    # Conversion en dictionnaire
    def to_dict(self):
        return {
            "ip": self.__ip,
            "city": self.__city,
            "region": self.__region,
            "country": self.__country,
            "isp": self.__isp,
            "timezone": self.__timezone,
            "loc": self.__loc
        }

    # Conversion en JSON
    def to_json(self):
        return json.dumps(self.to_dict(), indent=4, ensure_ascii=False)
