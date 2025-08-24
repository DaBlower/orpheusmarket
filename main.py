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

reigons = set()
for item in response:
    reigons.update(item["prices"].keys())

while True:
    reigon = input("What reigon are you in? (US, EU, IN, CA, AU, or XX) ")
    reigon = reigon.upper()
    if reigon in reigons:
        break
    else:
        print("That isn't a reigon! (Use XX if you aren't in the main reigons)")
print(f"Reigon is {reigon}")


print("")
print(f"{Fore.RED}HEIDIMARKET ITEMS:{Style.RESET_ALL}")
print("")
for item in response:
    spaces = 5
    if reigon in item["prices"]:
        if item["isBlackMarket"] == True:
            spaces -= len(str(item["prices"][reigon]))
            print(f"{Fore.GREEN} Found new project! {Fore.YELLOW}{item["prices"][reigon]}{Fore.BLUE}", end="")
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
    if reigon in item["prices"]:
        if item["isBlackMarket"] == False:
            spaces -= len(str(item["prices"][reigon]))
            print(f"{Fore.GREEN} Found new project! {Fore.YELLOW}{item["prices"][reigon]}{Fore.BLUE}", end="")
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