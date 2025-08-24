import requests
from colorama import Style, Fore
import os

url = "https://summer.skyfall.dev/api/shop" # this is @mahad's api - if it breaks, i might make my own

os.system('cls' if os.name == 'nt' else 'clear')

try:
    response = requests.get(url=url).json()
except requests.exceptions.JSONDecodeError:
    print(f"JSON decode error!")
    exit()
except Exception as e:
    print(f"Failed to contact api: {e}")

regions = set()
for item in response:
    regions.update(item["prices"].keys())

while True:
    region = input("What region are you in? (US, EU, IN, CA, AU, or XX) ")
    region = region.upper()
    if region in regions:
        break
    else:
        print("That isn't a region! (Use XX if you aren't in the main regions)")
print(f"region is {region}")


print("")
print(f"{Fore.RED}HEIDIMARKET ITEMS:{Style.RESET_ALL}")
print("")
for item in response:
    spaces = 5
    if region in item["prices"]:
        if item["isBlackMarket"] == True:
            spaces -= len(str(item["prices"][region]))
            print(f"{Fore.GREEN} Found new project! {Fore.YELLOW}{item["prices"][region]}{Fore.BLUE}", end="")
            for i in range(spaces):
                print("", end=" ")
            print(f"{Fore.BLUE}{item["title"]}{Style.RESET_ALL}")
    elif "XX" in item["prices"]:
        if item["isBlackMarket"] == True:
            spaces -= len(str(item["prices"]["XX"]))
            print(f"{Fore.GREEN} Found new project! {Fore.YELLOW}{item["prices"]["XX"]}{Fore.BLUE}", end="")
            for i in range(spaces):
                print("", end=" ")
            print(f"{Fore.BLUE}{item["title"]}{Style.RESET_ALL}")
print("")
print(f"{Fore.RED}NORMAL ITEMS{Style.RESET_ALL}")
print("")
for item in response:
    spaces = 5
    if region in item["prices"]:
        if item["isBlackMarket"] == False:
            spaces -= len(str(item["prices"][region]))
            print(f"{Fore.GREEN} Found new project! {Fore.YELLOW}{item["prices"][region]}{Fore.BLUE}", end="")
            for i in range(spaces):
                print("", end=" ")
            print(f"{Fore.BLUE}{item["title"]}{Style.RESET_ALL}")
    elif "XX" in item["prices"]:
        if item["isBlackMarket"] == False:
            spaces -= len(str(item["prices"]["XX"]))
            print(f"{Fore.GREEN} Found new project! {Fore.YELLOW}{item["prices"]["XX"]}{Fore.BLUE}", end="")
            for i in range(spaces):
                print("", end=" ")
            print(f"{Fore.BLUE}{item["title"]}{Style.RESET_ALL}")