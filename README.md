# IP Address Application

Python project for Cisco DevNet 4.9.4 (Option 2).
The program shows the public IPv4 and IPv6 address of your computer
and some info about it (city, country, ISP), using the ipify and ipinfo.io APIs.

## How to run
```
pip install requests
python main.py
```

## Files
- ip_client.py : sends the requests to the API
- ip_info.py : class that stores the IP data
- display.py : prints the result in the console
- main.py : runs everything

## Team
- Name 1 : scrum leader, documentation
- Name 2 : API client
- Name 3 : data model
- Name 4 : display, tests, presentation

## Ideas for later
- look up any IP the user types
- export to CSV
