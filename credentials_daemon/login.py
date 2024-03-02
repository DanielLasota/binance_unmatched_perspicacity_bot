import subprocess
import getpass
import json
import os
from utils.ascii_arts import ascii_arts
from utils.colors import colors


class Login:
    @staticmethod
    def get_secret():
        
        os.system('cls')
        print(colors.MAGENTA, ascii_arts.ascii_art_1, colors.RESET)
        
        email = getpass.getpass("Enter E-mail: ")
        password = getpass.getpass("Enter Password: ")
        
        try:
            subprocess.run(['bw', 'login', email, password, '--quiet'], shell=True, check=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"Error while logging in. Check credentials")
            return None
        secret_id = getpass.getpass("Enter Secret ID: ")
        
        try:
            result = subprocess.run(['bw', 'unlock', '--raw'], shell=True, input=password, text=True, capture_output=True, check=False)
            session_key = result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error while unlocking vault")
            return None
        session_key = session_key.strip()
        
        try:
            process = subprocess.Popen(['bw', 'get', 'item', secret_id, '--session', session_key], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            wynik, error = process.communicate()
            if error:
                print(f"Error: failed to get specified secret. Check Secret ID")
                return None
            secret = json.loads(wynik)
            
        except subprocess.CalledProcessError as e:
            print(f"Error")
            return None
        
        finally:
            subprocess.run(['bw', 'logout', '--quiet'], shell=True, check=True, text=True)
        os.system('cls')

        try:
            return secret['fields'][0]['value'], secret['fields'][1]['value']
            os.system('cls')
            
        except Exception as E:
            print("failed to return specified keys. Check Bitwarden's element structure")
            return None
    


