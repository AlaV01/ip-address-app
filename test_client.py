
from ip_client import IPClient, APIError

client = IPClient()

try:
    print("===== PUBLIC IP INFORMATION =====")

    # Test IPv4
    ipv4 = client.get_ipv4()
    print("\nIPv4 :", ipv4)

    # Test IPv6-compatible endpoint
    ip_from_ipv6_endpoint = client.get_ipv6()
    print("IP returned by IPv6-compatible endpoint :",
          ip_from_ipv6_endpoint)

    # Test IP details
    details = client.get_details(ipv4)

    print("\n===== IP DETAILS =====")

    for key, value in details.items():
        print(f"{key} : {value}")

except APIError as e:
    print("\nAPI Error :", e)

except Exception as e:
    print("\nUnexpected Error :", e)
