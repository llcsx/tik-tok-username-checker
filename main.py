from urllib3 import disable_warnings
import os
from os import system
import threading
import time
import logging
try:
    import requests
except:
    print("Requests not found installing module now...")
    system('pip install requests')
    import requests
try:
    from colorama import Fore, Back, Style
except:
    print("Colorama not found installing module now...")
    system('pip install colorama')
    from colorama import Fore, Back, Style
logging.getLogger('suds').setLevel(logging.WARNING)
disable_warnings()


class Main:
    def __init__(self):
        disable_warnings()
        print(Fore.RED)
        self.variables = {
            'available': 0,
            'unavailable': 0,
            'retries': 0
        }
        try:
            self.threads = int(input(Fore.WHITE + "Threads: "))
        except ValueError:
            print("Please enter a valid number of threads!")
            os.system(
                'title [TikTok Username Checker] - Restart required && '
                'pause >NUL && '
                'title [TikTok Username Checker] - Exiting...'
            )
            time.sleep(3)
            quit()

    def _checker(self, arg):
        try:
            arg = arg.replace("\n", '')
            available = requests.get(
                f"https://api16-normal-c-alisg.tiktokv.com/aweme/v1/unique/id/check/?residence=AU&device_id=6744798170507642374&os_version=14.0&app_id=1233&iid=6871351508912146178&app_name=musical_ly&pass-route=1&locale=en&pass-region=1&ac=WIFI&sys_region=AU&version_code=17.5.1&vid=68E586CD-EB05-43F7-B737-07EF062C6F79&channel=App%20Store&op_region=AU&os_api=18&idfa=00000000-0000-0000-0000-000000000000&device_platform=iphone&device_type=iPhone12%2C1&openudid=71d082ee1bfad590fb78b0aa85af107ec63d9e3a&account_region=&app_language=en&carrier_region=AU&current_region=AU&aid=1233&mcc_mnc=50501&screen_width=828&uoo=1&content_language=&language=en&cdid=95F7F032-2B8E-4764-98BC-364327802C73&build_number=175107&app_version=17.5.1&resolution=828%2A1792&unique_id={arg}", verify=False, headers={
                    'Host': 'api16-normal-c-alisg.tiktokv.com',
                    'Connection': 'keep-alive',
                    'x-Tt-Token': '0123ba5aaf5fcfc38b03f1b1f3314084e3f416223391f32bfa6b8ec114d6ed315d3629d2d21e2664e7ab563e6b566058a51e',
                    'sdk-version': '2',
                    'User-Agent': 'TikTok 17.5.1 rv:175107 (iPhone; iOS 14.0; en_AU) Cronet',
                    'x-tt-store-idc': 'alisg',
                    'x-tt-store-region': 'au',
                    'X-SS-DP': '1233',
                    'Accept-Encoding': 'gzip, deflate'
                }
            ).json()['is_valid']

        except Exception as e:
            print(e)
            self.variables['retries'] += 1
            self._checker(arg)
        else:
            if available == True:
                self.variables['available'] += 1
                print(Fore.GREEN + f'[AVAILABLE] {arg}')
                with open('Available.txt', 'a') as f:
                    f.write(f'{arg}\n')
            else:
                self.variables['unavailable'] += 1
                print(Fore.RED + f'[UNAVAILABLE] {arg}')

    def _multi_threading(self):
        threading.Thread(target=self._update_title).start()

        for username in self.usernames:
            attempting = True

            while attempting:
                if threading.active_count() <= self.threads:
                    threading.Thread(target=self._checker,
                                     args=(username,)).start()
                    attempting = False

    def _update_title(self):
        while (checked := (self.variables['available'] + self.variables['unavailable'])) < len(
            self.usernames
        ):
            os.system(
                f'title [TikTok Username Checker by betalol and elv] - Checked: {checked}/{self.total_usernames} ^| Av'
                f'ailable: {self.variables["available"]} ^| Unavailable: '
                f'{self.variables["unavailable"]} ^| Retries: {self.variables["retries"]}'
            )
            time.sleep(0.2)
        os.system(
            f'title [TikTok Username Checker by betalol and elv] - Checked: {checked}/{self.total_usernames} ^| Availa'
            f'ble: {self.variables["available"]} ^| Unavailable: {self.variables["unavailable"]} ^|'
            f' Retries: {self.variables["retries"]} && pause >NUL'
        )

    def setup(self):
        error = False
        if os.path.exists((usernames_txt := 'Usernames.txt')):
            with open(usernames_txt, 'r', encoding='UTF-8', errors='replace') as f:
                self.usernames = f.read().splitlines()
            self.total_usernames = len(self.usernames)
            if self.total_usernames == 0:
                error = True
        else:
            open(usernames_txt, 'a').close()
            error = True

        if error:
            print('[!] Paste the usernames in Usernames.txt.')
            os.system(
                'title [TikTok Username Checker] - Restart required && '
                'pause >NUL && '
                'title [TikTok Username Checker] - Exiting...'
            )
            time.sleep(3)
        else:
            self._multi_threading()


if __name__ == '__main__':
    os.system('cls && title [TikTok Username Checker]')
    disable_warnings()
    main = Main()
    main.setup()
