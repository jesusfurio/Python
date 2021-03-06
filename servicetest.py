import subprocess
from datetime import datetime, date, timedelta
from enum import Enum
import requests
import json


def print_head(message):
    print('=' * len(message))
    print(message)
    print('=' * len(message))


def print_bottom(message):
    print('=' * len(message))
    print(message)
    print('=' * len(message))


def get_network_commands(ip):
    commands = [['ping', '-c 5', ip], ['nmap', '-Pn', ip]]


def get_website_commands(ip):
    commands = [['wget', domain]]


def run_commands(option):
    server_ip = input("Write the server IP or domain to check:")

    if option == 1:
        commands = get_network_commands(server_ip)
    elif option == 2:
        commands = get_website_commands(server_ip)
    return subprocess.call(commands)


class MenuStatus(Enum):
    network_commands = "1-Realize network test"
    website_commands = "2-Realize web service test"
    execute_sla = "3-Calculate SLA of Cloud service"
    close_menu = "4-Exit"


class Menu:

    def date_epoch(date):
        d = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        convert = d.strftime("%s")

        return convert

    def input_sla_params():
        try:
            st_date = input(
                "Start date of the incident. The correct format is YYYY-MM-DD hh:mm:ss : ")
            st_epoch = date_epoch(st_date)

            end_date = input(
                "End date of the incident. The correct format is YYYY-MM-DD hh:mm:ss : ")
            end_epoch = date_epoch(end_date)

            ip = input("Write affected IP: ")

            return st_epoch, end_epoch, ip

        except ValueError:

            exit("Invalid date format.")

    def get_sla(start, end, ip):
        url = "https://gscan.2i.ovh.net/api/ip/{}/sla".format(ip)

        response = requests.get(url, params={"start": start, "end": end})

        if response.status_code == 200:
            payload = response.json()
            availability = payload["availability"]
            print(availability * 100, "% of time available")

        if response.status_code == 500:
            print("Invalid IP address.")

    def execute_sla():
        start, end, ip = input_sla_params()
        get_sla(start, end, ip)

    def close_menu():
        print ('Goodbye!')

    def main():
        print_head(message="Select your option:")
        for item in MenuStatus:
            print (item.value)

        option = int(input())

        return option


function_by_state = {
    0: Menu.main,
    1: run_commands,
    2: run_commands,
    3: Menu.execute_sla,
    4: Menu.close_menu,
}

if __name__ == '__main__':
    option = 0
    while option != 3:
        option = Menu.main()
        if option not in function_by_state:
            print ('Value not correct')
            continue
        function_by_state[option](option)
