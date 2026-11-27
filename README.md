# IP Address Application

Python project for Cisco DevNet 4.9.4 (Option 2).
The program shows the public IPv4 and IPv6 address of your computer
and some info about it (city, country, ISP), using the ipify and ipinfo.io APIs.

## How to run
The code is in the folder "projet devops".
```
cd "projet devops"
python -m pip install requests
python main.py
```

## Tests
```
cd "projet devops"
python -m unittest -v
```

## Files (in "projet devops")
- ip_client.py : sends the requests to the API
- ip_info.py : class that stores the IP data
- display.py : prints the result in the console
- main.py : runs everything
- test_*.py : unit tests

## Team
- Ala Naffoussi : scrum leader, documentation, main.py, unit tests
- Islem Jlejla : API client
- Ranim Lassoued : data model
- Hazem Jemili : display, presentation

## Ideas for later
- look up any IP the user types
- export to CSV
- graphical interface
