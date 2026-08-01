#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import subprocess
import os
import threading
import time
import re
import socket
import ssl
import json
import signal
import platform
import select
import math
import random
import concurrent.futures
from io import BytesIO
from datetime import datetime
from urllib3.exceptions import InsecureRequestWarning
import webbrowser


try:
    import customtkinter as ctk
    from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageSequence
    import requests
    import xlsxwriter
    import urllib3
    import dns.resolver
    import dns.exception
    import dns.name
    import idna
except ImportError:
    packages = [
        "customtkinter", "Pillow", "requests", "urllib3", "xlsxwriter",
        "dnspython", "idna"
    ]
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install"] + packages + ["--break-system-packages"]
    )
    import customtkinter as ctk
    from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageSequence
    import requests
    import xlsxwriter
    import urllib3
    import dns.resolver
    import dns.exception
    import dns.name
    import idna

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
urllib3.disable_warnings(category=InsecureRequestWarning)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

SERVICE_MAP = {}
SERVICE_CATEGORIES = {}

def _load_service_map():
    
    global SERVICE_MAP, SERVICE_CATEGORIES

    gist_url = "https://gist.githubusercontent.com/Dx3iZ/58e033637e2828e2e469ffcd48791a6c/raw/1cb4f260f41247e03619b790def0b2238f9b49f4/services.json"

    
    try:
        r = requests.get(gist_url, timeout=10,
                         headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code == 200:
            data = r.json()
            for port_str, (svc, cat) in data.items():
                p = int(port_str)
                SERVICE_MAP[p] = (svc, cat)
                SERVICE_CATEGORIES[p] = cat
    except Exception:
        pass

    
    ek_portlar = {
        21: ("FTP", "Dosya Transfer"), 22: ("SSH", "Uzaktan Erisim"),
        23: ("Telnet", "Uzaktan Erisim"), 25: ("SMTP", "E-Posta"),
        53: ("DNS", "Ag"), 69: ("TFTP", "Dosya Transfer"),
        80: ("HTTP", "Web"), 81: ("HTTP-Alt", "Web"),
        82: ("HTTP-Alt", "Web"), 83: ("HTTP-Alt", "Web"),
        84: ("HTTP-Alt", "Web"), 85: ("HTTP-Alt", "Web"),
        86: ("HTTP-Alt", "Web"), 87: ("HTTP-Alt", "Web"),
        88: ("HTTP-Alt", "Web"), 89: ("HTTP-Alt", "Web"),
        90: ("HTTP-Alt", "Web"), 110: ("POP3", "E-Posta"),
        111: ("RPC", "Ag"), 123: ("NTP", "Ag"),
        135: ("MSRPC", "Ag"), 137: ("NetBIOS-NS", "Ag"),
        138: ("NetBIOS-DGM", "Ag"), 139: ("NetBIOS-SSN", "Ag"),
        143: ("IMAP", "E-Posta"), 161: ("SNMP", "Izleme"),
        162: ("SNMP-Trap", "Izleme"), 179: ("BGP", "Ag"),
        389: ("LDAP", "Guvenlik"), 443: ("HTTPS", "Web"),
        444: ("HTTPS-Alt", "Web"), 445: ("SMB", "Dosya Paylasim"),
        446: ("HTTPS-Alt", "Web"), 447: ("HTTPS-Alt", "Web"),
        448: ("HTTPS-Alt", "Web"), 449: ("HTTPS-Alt", "Web"),
        465: ("SMTPS", "E-Posta"), 500: ("IPSec", "Ag"),
        514: ("Syslog", "Izleme"), 520: ("RIP", "Ag"),
        554: ("RTSP", "Ses/Goruntu"), 587: ("SMTP-Submit", "E-Posta"),
        631: ("IPP", "Yonetim"), 636: ("LDAPS", "Guvenlik"),
        873: ("Rsync", "Dosya Paylasim"), 902: ("VMware-ESXi", "Yonetim"),
        903: ("VMware-ESXi", "Yonetim"), 993: ("IMAPS", "E-Posta"),
        995: ("POP3S", "E-Posta"), 1080: ("SOCKS", "Proxy"),
        1099: ("RMI", "Gelistirme"), 1194: ("OpenVPN", "VPN"),
        1241: ("Nessus", "Guvenlik"), 1352: ("IBM-Lotus", "E-Posta"),
        1433: ("MSSQL", "Veritabani"), 1521: ("Oracle", "Veritabani"),
        1723: ("PPTP", "VPN"), 1883: ("MQTT", "Mesajlasma/Kuyruk"),
        2049: ("NFS", "Dosya Paylasim"), 2082: ("cPanel", "Yonetim"),
        2083: ("cPanel-SSL", "Yonetim"), 2086: ("WHM", "Yonetim"),
        2087: ("WHM-SSL", "Yonetim"), 2095: ("cPanel-Webmail", "E-Posta"),
        2096: ("cPanel-Webmail-SSL", "E-Posta"),
        2181: ("ZooKeeper", "Mesajlasma/Kuyruk"),
        2222: ("DirectAdmin", "Yonetim"),
        2375: ("Docker-REST", "Container"), 2376: ("Docker-SSL", "Container"),
        2379: ("etcd", "Container"), 2380: ("etcd-Peer", "Container"),
        2424: ("OrientDB", "Veritabani"), 2480: ("OrientDB-HTTPS", "Veritabani"),
        2525: ("SMTP-Alt", "E-Posta"), 3000: ("Grafana", "Izleme"),
        3001: ("Gitea-Web", "Gelistirme"), 3128: ("Squid-Proxy", "Proxy"),
        3306: ("MySQL", "Veritabani"), 3389: ("RDP", "Uzaktan Erisim"),
        3690: ("SVN", "Gelistirme"), 4000: ("Node.js-Dev", "Web"),
        4001: ("etcd-Client", "Container"), 4040: ("Jenkins", "Gelistirme"),
        4044: ("Hadoop", "Veritabani"), 4222: ("NATS", "Mesajlasma/Kuyruk"),
        4430: ("HTTPS-Alt", "Web"), 4443: ("HTTPS-Alt", "Web"),
        4444: ("Metasploit", "Guvenlik"), 4445: ("Metasploit", "Guvenlik"),
        4446: ("Metasploit", "Guvenlik"), 4447: ("Metasploit", "Guvenlik"),
        4448: ("Metasploit", "Guvenlik"), 4449: ("Metasploit", "Guvenlik"),
        4500: ("IPSec-NAT", "Ag"), 4560: ("Logstash", "Izleme"),
        4567: ("Sinatra", "Web"), 4646: ("Appian", "Yonetim"),
        4711: ("Pulse-Secure", "VPN"), 4848: ("GlassFish", "Yonetim"),
        4899: ("Radmin", "Uzaktan Erisim"), 4949: ("Munin", "Izleme"),
        5000: ("Flask-Dev", "Web"), 5001: ("Synology-DSM", "Depolama"),
        5002: ("Synology-Admin", "Depolama"), 5003: ("Synology-File", "Depolama"),
        5005: ("JVM-Debug", "Gelistirme"), 5006: ("WMI", "Yonetim"),
        5038: ("Asterisk", "Ses/Goruntu"), 5040: ("Modbus", "Endustriyel"),
        5050: ("YARN", "Veritabani"), 5051: ("Hadoop-IPC", "Veritabani"),
        5060: ("SIP", "Ses/Goruntu"), 5061: ("SIPS", "Ses/Goruntu"),
        5222: ("XMPP", "Mesajlasma/Kuyruk"), 5223: ("XMPP-SSL", "Mesajlasma/Kuyruk"),
        5269: ("XMPP-Server", "Mesajlasma/Kuyruk"),
        5353: ("mDNS", "Ag"), 5432: ("PostgreSQL", "Veritabani"),
        5555: ("Android-ADB", "Gelistirme"), 5556: ("Android-ADB", "Gelistirme"),
        5601: ("Kibana", "Izleme"), 5631: ("pcAnywhere", "Uzaktan Erisim"),
        5632: ("pcAnywhere", "Uzaktan Erisim"), 5666: ("NRPE", "Izleme"),
        5667: ("NSCA", "Izleme"), 5672: ("RabbitMQ", "Mesajlasma/Kuyruk"),
        5683: ("CoAP", "IoT"), 5800: ("VNC-HTTP", "Uzaktan Erisim"),
        5900: ("VNC", "Uzaktan Erisim"),
        5984: ("CouchDB", "Veritabani"), 5985: ("WinRM-HTTP", "Yonetim"),
        5986: ("WinRM-HTTPS", "Yonetim"), 6000: ("X11", "Uzaktan Erisim"),
        6379: ("Redis", "Veritabani"), 6443: ("Kubernetes-API", "Container"),
        6667: ("IRC", "Mesajlasma/Kuyruk"), 6789: ("Splunk", "Izleme"),
        6881: ("BitTorrent", "Dosya Paylasim"),
        7000: ("Cassandra", "Veritabani"), 7001: ("Cassandra-SSL", "Veritabani"),
        7070: ("WebSphere", "Yonetim"), 7077: ("Spark", "Veritabani"),
        7199: ("Cassandra-JMX", "Veritabani"),
        7443: ("HTTPS-Alt", "Web"), 7474: ("Neo4j", "Veritabani"),
        8000: ("HTTP-Alt", "Web"), 8001: ("HTTP-Alt", "Web"),
        8008: ("HTTP-Alt", "Web"), 8009: ("AJP", "Yonetim"),
        8080: ("HTTP-Proxy", "Web"), 8081: ("HTTP-Alt", "Web"),
        8086: ("InfluxDB", "Veritabani"), 8089: ("Splunk-API", "Izleme"),
        8090: ("HTTP-Alt", "Web"), 8091: ("Couchbase", "Veritabani"),
        8096: ("Emby/Jellyfin", "Ses/Goruntu"), 8118: ("Privoxy", "Proxy"),
        8140: ("Puppet", "Yonetim"), 8172: ("Plesk", "Yonetim"),
        8200: ("Vault", "Guvenlik"), 8222: ("VMware-HTTP", "Yonetim"),
        8300: ("Consul", "Ag"), 8332: ("Bitcoin-RPC", "Blockchain"),
        8333: ("Bitcoin-P2P", "Blockchain"),
        8443: ("HTTPS-Alt", "Web"), 8444: ("HTTPS-Alt", "Web"),
        8500: ("Consul-UI", "Ag"), 8530: ("DPM", "Yonetim"),
        8545: ("Ethereum-RPC", "Blockchain"),
        8883: ("MQTT-SSL", "Mesajlasma/Kuyruk"),
        8888: ("HTTPS-Alt", "Web"),
        8983: ("Solr", "Veritabani"),
        9000: ("PHP-FPM", "Web"), 9001: ("Hadoop-NameNode", "Veritabani"),
        9042: ("Cassandra-CQL", "Veritabani"), 9050: ("Tor-SOCKS", "Guvenlik"),
        9051: ("Tor-Control", "Guvenlik"),
        9090: ("HTTPS-Alt", "Web"), 9092: ("Kafka", "Mesajlasma/Kuyruk"),
        9100: ("JetDirect", "Yonetim"),
        9200: ("Elasticsearch", "Veritabani"), 9300: ("Elasticsearch-Transport", "Veritabani"),
        9418: ("Git", "Gelistirme"),
        9443: ("HTTPS-Alt", "Web"),
        10000: ("Webmin", "Yonetim"), 10050: ("Zabbix-Agent", "Izleme"),
        10051: ("Zabbix-Trapper", "Izleme"),
        10250: ("Kubelet", "Container"), 10255: ("Kubelet-ReadOnly", "Container"),
        11211: ("Memcached", "Veritabani"),
        12345: ("NetBus", "Guvenlik"),
        15672: ("RabbitMQ-UI", "Mesajlasma/Kuyruk"),
        16379: ("Redis-Alt", "Veritabani"),
        25565: ("Minecraft", "Oyun"),
        27017: ("MongoDB", "Veritabani"), 27018: ("MongoDB-Alt", "Veritabani"),
        27019: ("MongoDB-Alt", "Veritabani"), 28017: ("MongoDB-HTTP", "Veritabani"),
        31337: ("BackOrifice", "Guvenlik"),
        32764: ("HTTPS-Alt", "Web"),
        49152: ("Windows-RPC", "Ag"), 49153: ("Windows-RPC", "Ag"),
        49154: ("Windows-RPC", "Ag"), 49155: ("Windows-RPC", "Ag"),
    }

    for p, (svc, cat) in ek_portlar.items():
        if p not in SERVICE_MAP:
            SERVICE_MAP[p] = (svc, cat)
            SERVICE_CATEGORIES[p] = cat

    
    web_http = [81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 3000, 3001, 4000,
                5000, 5001, 6000, 7000, 7001, 7070, 8000, 8001, 8002, 8003,
                8004, 8005, 8006, 8007, 8008, 8010, 8043, 8080, 8081, 8082,
                8083, 8084, 8085, 8087, 8088, 8090, 8096, 8097, 8181, 8222,
                8280, 8281, 8800, 8880, 9000, 9080]
    web_https = [444, 446, 447, 448, 449, 4430, 4443, 7443, 7444, 7445, 7446,
                 7447, 8243, 8403, 8443, 8444, 8445, 8446, 8447, 8448, 8449,
                 8834, 8888, 8889, 8890, 8891, 8892, 8893, 8894, 8895, 8896,
                 8897, 8898, 8899, 9060, 9443, 9444, 9445, 9446, 9447, 9448,
                 9449, 9450, 9943, 9944, 9981, 9999, 10080, 10134, 10443,
                 11000, 14534, 15000, 17000, 18080, 19000, 19100, 20000,
                 32764, 32768, 33333, 40000, 50000]

    for p in web_http:
        if p not in SERVICE_MAP:
            SERVICE_MAP[p] = (f"HTTP-Alt", "Web")
            SERVICE_CATEGORIES[p] = "Web"
    for p in web_https:
        if p not in SERVICE_MAP:
            SERVICE_MAP[p] = (f"HTTPS-Alt", "Web")
            SERVICE_CATEGORIES[p] = "Web"


_load_service_map()


ALL_PORTS = sorted(SERVICE_MAP.keys())




OS_SIGS = [
    ("Linux 2.4/2.6/3.x", 63, 65, 5800, 5900, True),
    ("Linux (modern)", 63, 65, 65000, 66000, True),
    ("Linux 4.x/5.x", 63, 65, 29000, 29500, True),
    ("Linux 6.x (latest)", 63, 65, 60000, 61000, True),
    ("Windows 10/11/Server 2016+", 127, 129, 65000, 66000, True),
    ("Windows 7/8/Server 2008", 127, 129, 8100, 8300, True),
    ("Windows Server 2003/XP", 127, 129, 65000, 66000, False),
    ("macOS / FreeBSD", 59, 61, 5800, 5900, True),
    ("macOS (modern)", 59, 61, 65000, 66000, True),
    ("FreeBSD (modern)", 63, 65, 65000, 66000, True),
    ("Solaris", 63, 65, 57000, 58000, True),
    ("Cisco IOS", 254, 256, 8700, 66000, True),
    ("AIX / IBM", 63, 65, 16300, 16500, True),
    ("HP-UX", 63, 65, 32768, 65535, True),
    ("OpenBSD", 63, 65, 16384, 16385, True),
    ("Android", 63, 65, 5720, 5840, True),
]




WAF_SIGS = {
    "Cloudflare": ["CF-Ray", "cloudflare", "__cfduid", "cf-ray"],
    "CloudFront": ["x-amz-cf-id", "x-amz-cf-pop", "cloudfront"],
    "Akamai": ["x-akamai", "akamai"],
    "Fastly": ["x-fastly", "fastly"],
    "Sucuri": ["x-sucuri", "sucuri"],
    "ModSecurity": ["ModSecurity", "mod_security"],
    "Wordfence": ["wordfence"],
    "AWS WAF": ["x-amzn-waf", "awswaf"],
    "Barracuda": ["barracuda"],
    "F5 BIG-IP": ["BigIP", "F5"],
    "Imperva": ["incapsula", "Imperva"],
    "Varnish": ["x-varnish", "varnish"],
    "Naxsi": ["naxsi"],
    "Armor": ["armor"],
    "StackPath": ["stackpath"],
    "Radware": ["radware"],
    "Fortinet": ["fortigate", "fortiweb"],
    "Citrix NetScaler": ["netscaler", "citrix"],
    "Comodo": ["comodo"],
    "Airlock": ["airlock"],
}




TECH_CHECKS = {
    "WordPress": ["wp-content", "wp-includes", "wordpress"],
    "Drupal": ["Drupal", "drupal"],
    "Joomla": ["Joomla", "joomla"],
    "Laravel": ["laravel", "Laravel"],
    "Symfony": ["symfony", "Symfony"],
    "Django": ["django", "Django", "csrftoken", "sessionid"],
    "Vue.js": ["vue.js", "Vue.js", "__vue__", "vue-router"],
    "React": ["react", "React", "react-dom", "create-react-app"],
    "Angular": ["angular", "Angular", "ng-version"],
    "Next.js": ["next.js", "Next.js", "__NEXT_DATA__", "_next/static"],
    "Nuxt.js": ["nuxt", "Nuxt"],
    "Squarespace": ["squarespace"],
    "Wix": ["wix"],
    "Shopify": ["shopify", "myshopify"],
    "Magento": ["magento", "Mage", "Magento"],
    "PrestaShop": ["prestashop", "PrestaShop"],
    "Joomla": ["joomla", "Joomla"],
    "Tomcat": ["tomcat", "Tomcat", "Apache Tomcat"],
    "JBoss": ["jboss", "JBoss", "WildFly"],
    "Jetty": ["jetty", "Jetty"],
    "Node.js": ["node.js", "Node.js", "node-icon", "x-powered-by: Express"],
    "Flask": ["flask", "Flask"],
    "Ruby on Rails": ["rails", "Rails", "ruby", "RUBY"],
    "ASP.NET": ["asp.net", "ASP.NET", "__VIEWSTATE", "__EVENTVALIDATION"],
    "IIS": ["Microsoft-IIS", "IIS"],
    "Nginx": ["nginx", "Nginx"],
    "Apache": ["Apache", "apache"],
    "Caddy": ["caddy", "Caddy"],
    "LiteSpeed": ["litespeed", "LiteSpeed"],
}





def detect_os(ttl, win=5840, df=True):
    
    for name, tl, th, wl, wh, dr in OS_SIGS:
        if tl <= ttl <= th and wl <= win <= wh and df == dr:
            return name
    if ttl <= 64:
        return "Linux/Unix (generic)"
    if ttl <= 128:
        return "Windows (generic)"
    return "Cisco/Solaris (generic)"


def ping_fingerprint(ip):
    
    ttl, win, df = 64, 5840, True
    try:
        if platform.system().lower() == 'windows':
            r = subprocess.run(['ping', '-n', '1', '-w', '500', ip],
                               capture_output=True, text=True, timeout=2)
        else:
            r = subprocess.run(['ping', '-c', '1', '-W', '1', ip],
                               capture_output=True, text=True, timeout=2)
        o = r.stdout + r.stderr
        m = re.search(r'(?:TTL|ttl)[=:]\s*(\d+)', o)
        if m:
            ttl = int(m.group(1))
        m = re.search(r'(?:win|Win|WIN)[=:]\s*(\d+)', o)
        if m:
            win = int(m.group(1))
        df = bool(re.search(r'df|DF', o))
    except Exception:
        pass
    return {"ttl": ttl, "win_size": win, "df": df, "os": detect_os(ttl, win, df)}


def resolve_target(t):
    
    t = t.strip()
    if not t:
        return None
    try:
        t = idna.encode(t).decode('ascii')
    except Exception:
        pass
    t = re.sub(r'[^a-zA-Z0-9.\-:]', '', t)
    if re.search(r':\d+$', t):
        return None

    blocked = {"127.0.0.1", "0.0.0.0", "localhost", "::1", "255.255.255.255"}
    b_pre = ["10.", "172.16.", "172.17.", "172.18.", "172.19.", "172.20.",
             "172.21.", "172.22.", "172.23.", "172.24.", "172.25.", "172.26.",
             "172.27.", "172.28.", "172.29.", "172.30.", "172.31.", "192.168.",
             "169.254."]
    b_v6 = ["fc", "fd", "fe80", "::1", "::", "2001:db8", "ff", "ff02"]

    for fam in [socket.AF_INET, socket.AF_INET6]:
        try:
            socket.inet_pton(fam, t)
            if fam == socket.AF_INET6:
                tl = t.lower()
                if tl in blocked:
                    return None
                for p in b_v6:
                    if tl.startswith(p):
                        return None
                return t
            if t in blocked:
                return None
            for p in b_pre:
                if t.startswith(p):
                    return None
            return t
        except Exception:
            pass

    try:
        ip = socket.gethostbyname(t)
        if ip in blocked:
            return None
        for p in b_pre:
            if ip.startswith(p):
                return None
        return ip
    except Exception:
        return None


def is_ip(target):
    
    for fam in [socket.AF_INET, socket.AF_INET6]:
        try:
            socket.inet_pton(fam, target)
            return True
        except Exception:
            pass
    return False


def _check_port(ip, port, timeout):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        r = s.connect_ex((ip, port))
        s.close()
        return port if r == 0 else None
    except Exception:
        return None


def parallel_tcp_scan(ip, ports, timeout=0.5):
    results = []
    if not ports:
        return results
    max_workers = min(len(ports), 300)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(_check_port, ip, p, timeout): p for p in ports}
        for f in concurrent.futures.as_completed(futures):
            try:
                r = f.result()
                if r is not None:
                    results.append(r)
            except Exception:
                pass
    return results


def http_probe(ip, port, use_ssl=False):
    """HTTP/HTTPS keşif - başlık, WAF, teknoloji tespiti"""
    result = {
        "status_code": 0,
        "headers": {},
        "body": "",
        "server": "",
        "title": "",
        "waf": None,
        "tech": [],
        "response_time": 0
    }

    try:
        protocol = "https" if use_ssl else "http"
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3.0)

        start_t = time.time()
        sock.connect((ip, port))

        if use_ssl:
            try:
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                sock = ctx.wrap_socket(sock, server_hostname=ip)
            except Exception:
                sock.close()
                return result

        req = (
            f"GET / HTTP/1.1\r\n"
            f"Host: {ip}\r\n"
            f"User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            f"(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36\r\n"
            f"Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\n"
            f"Accept-Language: en-US,en;q=0.5\r\n"
            f"Connection: close\r\n\r\n"
        )
        sock.sendall(req.encode())

        resp = b""
        sock.settimeout(3.0)
        try:
            while True:
                c = sock.recv(4096)
                if not c:
                    break
                resp += c
                if len(resp) > 65536 or b"</html>" in resp.lower():
                    break
        except socket.timeout:
            pass
        except Exception:
            pass

        result["response_time"] = round((time.time() - start_t) * 1000, 1)

        sock.close()

        if not resp:
            return result

        
        parts = resp.split(b"\r\n\r\n", 1)
        header_raw = parts[0].decode('utf-8', errors='replace')
        body_raw = parts[1].decode('utf-8', errors='replace') if len(parts) > 1 else ""

        result["body"] = body_raw[:5000]

        
        m = re.search(r'HTTP/\d\.\d\s+(\d+)', header_raw)
        if m:
            result["status_code"] = int(m.group(1))

        
        header_dict = {}
        for line in header_raw.split('\r\n')[1:]:
            if ':' in line:
                k, v = line.split(':', 1)
                header_dict[k.strip().lower()] = v.strip()
        result["headers"] = header_dict

        
        result["server"] = header_dict.get("server", "")

       
        m = re.search(r'<title[^>]*>(.*?)</title>', body_raw, re.I | re.DOTALL)
        if m:
            result["title"] = m.group(1).strip()[:80]

        
        waf = detect_waf(header_dict, body_raw)
        result["waf"] = waf

        
        techs = detect_tech(header_dict, body_raw, result["server"])
        result["tech"] = techs

    except Exception:
        pass

    return result


def detect_waf(headers, body):
    
    all_text = str(headers) + " " + (body or "")
    for name, sigs in WAF_SIGS.items():
        for sig in sigs:
            if sig.lower() in all_text.lower():
                return name
    return None


def detect_tech(headers, body, server):
    
    techs = set()
    all_text = str(headers) + " " + (body or "")
    for t, pats in TECH_CHECKS.items():
        for p in pats:
            if p.lower() in all_text.lower():
                techs.add(t)
                break
    if server:
        su = server.upper()
        if "APACHE" in su:
            techs.add("Apache")
        elif "NGINX" in su:
            techs.add("Nginx")
        elif "IIS" in su:
            techs.add("IIS")
        elif "LITESPEED" in su:
            techs.add("LiteSpeed")
        elif "CADDY" in su:
            techs.add("Caddy")
        elif "CLOUDFLARE" in su:
            techs.add("Cloudflare")
        elif "OPENRESTY" in su:
            techs.add("OpenResty")
    return sorted(techs)


def banner_grab(ip, port, service):
    
    svc_lower = service.lower()
    banner = ""
    bd = ""
    try:
        s = socket.create_connection((ip, port), timeout=1.5)
        s.settimeout(0.5)

        if 'ftp' in svc_lower or port == 21:
            d = s.recv(1024)
            if d:
                banner = re.sub(r'[^\x20-\x7E]', ' ',
                                d.decode('utf-8', 'replace')).strip()[:80]
                for kw, nm in [('vsFTPd', 'vsFTPd'), ('ProFTPD', 'ProFTPD'),
                               ('Pure-FTPd', 'Pure-FTPd'), ('FileZilla', 'FileZilla'),
                               ('Microsoft', 'IIS FTP')]:
                    if kw.lower() in banner.lower():
                        bd = nm
                        break
        elif 'ssh' in svc_lower or port == 22:
            d = s.recv(256)
            if d:
                banner = re.sub(r'[^\x20-\x7E]', ' ',
                                d.decode('utf-8', 'replace')).strip()[:80]
                for kw, nm in [('OpenSSH', 'OpenSSH'), ('Dropbear', 'Dropbear'),
                               ('libssh', 'libssh')]:
                    if kw.lower() in banner.lower():
                        bd = nm
                        break
        elif port in (25, 465, 587, 2525) or 'smtp' in svc_lower:
            d = s.recv(512)
            if d:
                banner = re.sub(r'[^\x20-\x7E]', ' ',
                                d.decode('utf-8', 'replace')).strip()[:80]
                for kw, nm in [('Postfix', 'Postfix'), ('Sendmail', 'Sendmail'),
                               ('Exim', 'Exim'), ('Exchange', 'MS Exchange'),
                               ('Qmail', 'Qmail')]:
                    if kw.lower() in banner.lower():
                        bd = nm
                        break
        elif port in (110, 995) or 'pop3' in svc_lower:
            d = s.recv(512)
            if d:
                banner = re.sub(r'[^\x20-\x7E]', ' ',
                                d.decode('utf-8', 'replace')).strip()[:80]
                if 'dovecot' in banner.lower():
                    bd = 'Dovecot POP3'
                elif 'courier' in banner.lower():
                    bd = 'Courier POP3'
        elif port in (143, 993) or 'imap' in svc_lower:
            d = s.recv(512)
            if d:
                banner = re.sub(r'[^\x20-\x7E]', ' ',
                                d.decode('utf-8', 'replace')).strip()[:80]
                if 'dovecot' in banner.lower():
                    bd = 'Dovecot IMAP'
                elif 'courier' in banner.lower():
                    bd = 'Courier IMAP'
                elif 'cyrus' in banner.lower():
                    bd = 'Cyrus IMAP'
        elif port == 3306 or 'mysql' in svc_lower:
            d = s.recv(256)
            if d:
                banner = re.sub(r'[^\x20-\x7E]', ' ',
                                d.decode('utf-8', 'replace')).strip()[:80]
                if 'mariadb' in banner.lower():
                    bd = 'MariaDB'
                elif 'mysql' in banner.lower():
                    bd = 'MySQL'
        elif port == 5432 or 'postgresql' in svc_lower:
            d = s.recv(256)
            if d:
                banner = re.sub(r'[^\x20-\x7E]', ' ',
                                d.decode('utf-8', 'replace')).strip()[:80]
                bd = 'PostgreSQL'
        elif port == 6379 or 'redis' in svc_lower:
            s.sendall(b"PING\r\n")
            time.sleep(0.03)
            d = s.recv(256)
            if d and b'PONG' in d:
                banner, bd = 'Redis Sunucusu', 'Redis'
        elif port == 3389 or 'rdp' in svc_lower:
            d = s.recv(256)
            banner = 'RDP Sunucusu'
            bd = 'RDP'
            if d:
                banner = re.sub(r'[^\x20-\x7E]', ' ',
                                d.decode('utf-8', 'replace')).strip()[:80]
        elif port in (5900, 5901, 5800) or 'vnc' in svc_lower:
            d = s.recv(256)
            if d:
                banner = re.sub(r'[^\x20-\x7E]', ' ',
                                d.decode('utf-8', 'replace')).strip()[:80]
                if re.search(r'RFB|VNC|RealVNC|TightVNC', banner, re.I):
                    bd = banner.strip()
        elif port == 445 or 'smb' in svc_lower:
            banner, bd = 'SMB', 'SMB'
        elif port in (389, 636) or 'ldap' in svc_lower:
            banner, bd = 'LDAP', 'LDAP'
        elif port in (161, 162) or 'snmp' in svc_lower:
            banner, bd = 'SNMP', 'SNMP'
        elif port == 27017 or 'mongodb' in svc_lower:
            d = s.recv(256)
            if d:
                banner = re.sub(r'[^\x20-\x7E]', ' ',
                                d.decode('utf-8', 'replace')).strip()[:80]
                bd = 'MongoDB'
        else:
            s.sendall(b"\r\n")
            time.sleep(0.02)
            d = s.recv(256)
            if d:
                banner = re.sub(r'[^\x20-\x7E]', ' ',
                                d.decode('utf-8', 'replace')).strip()[:80]

    except Exception:
        pass
    finally:
        try:
            s.close()
        except Exception:
            pass

    return banner, bd


def dns_lookup(domain):
    
    records = {
        "A": [],
        "AAAA": [],
        "MX": [],
        "NS": [],
        "TXT": [],
        "CNAME": [],
        "SOA": [],
    }

    resolver = dns.resolver.Resolver()
    resolver.timeout = 3.0
    resolver.lifetime = 3.0

    for rtype in ["A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA"]:
        try:
            answers = resolver.resolve(domain, rtype)
            for ans in answers:
                if rtype == "MX":
                    records["MX"].append(f"{ans.preference} {ans.exchange}")
                elif rtype == "SOA":
                    records["SOA"].append(f"{ans.mname} {ans.rname}")
                elif rtype == "TXT":
                    txt_str = ans.to_text().strip('"')
                    records["TXT"].append(txt_str[:100])
                else:
                    records[rtype].append(ans.to_text())
        except dns.exception.DNSException:
            pass
        except Exception:
            pass

    return records


def get_service_info(port):
    
    if port in SERVICE_MAP:
        return SERVICE_MAP[port]
    return (f"Port-{port}", "Bilinmeyen")


class CyberAnkaGozcu:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("CyberAnka Gözcü - Port Tarama ve Güvenlik Analizi")
        self.root.configure(fg_color="#0a0a0a")
        self._set_window_icon()
        
        self.screen_w = self.root.winfo_screenwidth()
        self.screen_h = self.root.winfo_screenheight()
        w = int(self.screen_w * 0.92)
        h = int(self.screen_h * 0.88)
        if w < 1100:
            w = 1100
        if h < 700:
            h = 700
        x = (self.screen_w - w) // 2
        y = (self.screen_h - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")
        self.root.minsize(1000, 650)
        self.root.resizable(True, True)
        self.root.attributes("-alpha", 0)
        
        self.current_operation = "bekliyor"
        self.paused = False
        self.stopped = False
        self.pause_event = threading.Event()
        self.pause_event.set()
        self.scan_start_time = 0
        self._probe_stop = threading.Event()
        self._probe_pause = threading.Event()
        self._probe_pause.set()
        
        self.scan_results = []          # port tarama sonuçları
        self.http_results = {}          # port -> http_probe sonuçları
        self.dns_results = {}           # domain -> dns kayıtları
        self.os_result = {}             # OS fingerprint
        self.target_domain = ""
        self.target_ip = ""
        
        self.thread_count = ctk.IntVar(value=100)
        self.timeout_value = ctk.IntVar(value=1)
        self.port_mode = ctk.StringVar(value="full")  # "full", "web", "custom"
        self.custom_ports = ""
        
        self.logo_img_pil = None
        self.anka_img_pil = None
        self.splash_phase = 0
        
        self.root.after(50, self.start_splash)

    def _set_window_icon(self):
        try:
            r = requests.get(
                "https://i.hizliresim.com/7fh9ayg.png",
                timeout=10,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            r.raise_for_status()
            icon_img = Image.open(BytesIO(r.content))
            icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
            icon_photo = ImageTk.PhotoImage(icon_img.resize((64, 64), Image.LANCZOS))
            self._icon_ref = icon_photo
            self.root.wm_iconphoto(True, icon_photo)
            if sys.platform == "win32":
                try:
                    import ctypes
                    import tempfile
                    ico_path = os.path.join(tempfile.gettempdir(), "cyberanka_gozcu_icon.ico")
                    icon_img.save(ico_path, format="ICO", sizes=icon_sizes)
                    self.root.iconbitmap(ico_path)
                    myappid = "cyberanka.gozcu.scanner.1"
                    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
                except Exception:
                    pass
        except Exception:
            pass

    def download_anka_logo(self):
        
        try:
            r = requests.get(
                "https://i.ibb.co/FLmVQVy8/8b03dcac-32f1-4bea-ab20-f695f2953652.png",
                timeout=15,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            r.raise_for_status()
            img = Image.open(BytesIO(r.content))
            return img
        except Exception:
            return None

    def download_bg_logo(self):
        
        try:
            r = requests.get(
                "https://i.hizliresim.com/e9rbpzb.png",
                timeout=10,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            r.raise_for_status()
            img = Image.open(BytesIO(r.content))
            return img
        except Exception:
            return None

    def download_subflame_logo(self):
        
        try:
            r = requests.get(
                "https://cyberanka.com/assets/images/subflame.png",
                timeout=10,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            r.raise_for_status()
            img = Image.open(BytesIO(r.content))
            return img
        except Exception:
            return None

    def create_hacker_bg(self, w, h):
        
        bg = Image.new('RGBA', (w, h), (0, 0, 0, 255))
        draw = ImageDraw.Draw(bg)
        try:
            font_tiny = ImageFont.truetype("Consolas", 8)
            font_small = ImageFont.truetype("Consolas", 10)
            font_med = ImageFont.truetype("Consolas", 12)
            font_big = ImageFont.truetype("Consolas", 48)
        except Exception:
            font_tiny = font_small = font_med = font_big = ImageFont.load_default()

        rng = random.Random(42)

        
        for col in range(0, w, 25):
            alpha = rng.randint(4, 12)
            draw.line([(col, 0), (col, h)], fill=(0, 255, 65, alpha), width=1)

        for row in range(0, h, 40):
            alpha = rng.randint(3, 8)
            draw.line([(0, row), (w, row)], fill=(0, 200, 50, alpha), width=1)

        
        corner_data = [
            (15, 15, "[", "#ff4444"),
            (w - 25, 15, "]", "#ff4444"),
            (15, h - 30, "{", "#00ff41"),
            (w - 25, h - 30, "}", "#00ff41"),
        ]
        for cx, cy, char, color in corner_data:
            draw.text((cx, cy), char, fill=color, font=font_med)

        
        hex_chars = "0123456789ABCDEF"
        for i in range(25):
            y = i * 20 + 40
            if y < h - 40:
                char = rng.choice(hex_chars)
                alpha = rng.randint(8, 25)
                draw.text((8, y), char, fill=(0, 255, 65, alpha), font=font_tiny)
                draw.text((w - 18, y), rng.choice(hex_chars),
                          fill=(0, 255, 65, alpha), font=font_tiny)

        
        draw.text((w // 2, h // 2 - 40), "GOZCU",
                  fill=(0, 255, 65, 6), font=font_big, anchor="mm")
        draw.text((w // 2, h // 2 + 20), "v1.0",
                  fill=(0, 200, 50, 8), font=font_med, anchor="mm")

        
        for _ in range(120):
            x = rng.randint(20, w - 30)
            y = rng.randint(10, h - 20)
            draw.text((x, y), rng.choice(hex_chars),
                      fill=(0, rng.randint(100, 220), 0, rng.randint(3, 12)),
                      font=font_tiny)

        
        for i in range(15):
            x = rng.randint(30, w - 40)
            y = rng.randint(20, h - 30)
            char = rng.choice([">", "!", "$", "#"])
            draw.text((x, y), char, fill=(255, 40, 40, rng.randint(8, 20)),
                      font=font_small)

        
        draw.line([(0, h - 22), (w, h - 22)], fill=(0, 255, 65, 10), width=1)
        status = f"CYBERANKA GOZCU v1.0 // {time.strftime('%H:%M:%S')} UTC"
        draw.text((10, h - 18), status, fill=(0, 255, 65, 12), font=font_tiny)

        
        for i in range(0, w, 6):
            alpha = rng.randint(3, 8)
            draw.point((i, 0), fill=(0, 255, 65, alpha))
            draw.point((i, h - 1), fill=(0, 255, 65, alpha))
        for i in range(0, h, 6):
            alpha = rng.randint(3, 8)
            draw.point((0, i), fill=(0, 255, 65, alpha))
            draw.point((w - 1, i), fill=(0, 255, 65, alpha))

        return bg

    def start_splash(self):
        """Splash ekranı - Anka.png ile"""
        self.anka_img_pil = self.download_anka_logo()

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        self.splash_bg = ctk.CTkFrame(self.root, fg_color="#000000", corner_radius=0)
        self.splash_bg.place(relx=0, rely=0, relwidth=1, relheight=1)

        
        self.hacker_bg_pil = self.create_hacker_bg(screen_w, screen_h)
        self.hacker_bg_tk = ImageTk.PhotoImage(self.hacker_bg_pil)
        self.hacker_bg_label = ctk.CTkLabel(
            self.splash_bg, text="", image=self.hacker_bg_tk, fg_color="transparent"
        )
        self.hacker_bg_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        
        if self.anka_img_pil:
            try:
                anka_display = self.anka_img_pil.copy()
                
                anka_display.thumbnail((280, 280), Image.LANCZOS)
                self.anka_splash_photo = ImageTk.PhotoImage(anka_display)
                self.anka_label = ctk.CTkLabel(
                    self.splash_bg, text="", image=self.anka_splash_photo,
                    fg_color="transparent"
                )
                self.anka_label.place(relx=0.5, rely=0.35, anchor="center")
            except Exception:
                pass

        
        brand_frame = ctk.CTkFrame(self.splash_bg, fg_color="transparent")
        brand_frame.place(relx=0.5, rely=0.55, anchor="center")

        ctk.CTkLabel(
            brand_frame,
            text="Cyber",
            font=ctk.CTkFont(family="Montserrat", size=56, weight="bold"),
            text_color="#ff4444",
            fg_color="transparent"
        ).pack(side=ctk.LEFT)

        ctk.CTkLabel(
            brand_frame,
            text="Anka",
            font=ctk.CTkFont(family="Montserrat", size=56, weight="normal"),
            text_color="#ff8888",
            fg_color="transparent"
        ).pack(side=ctk.LEFT)

        
        ctk.CTkLabel(
            brand_frame,
            text="GÖZCÜ",
            font=ctk.CTkFont(family="Consolas", size=28, weight="bold"),
            text_color="#00ff41",
            fg_color="transparent"
        ).pack(pady=(5, 0))

        
        ctk.CTkLabel(
            self.splash_bg,
            text="Gelişmiş Port Tarama · DNS Keşif · WAF Tespit · OS Fingerprinting",
            font=ctk.CTkFont(family="Montserrat", size=13),
            text_color="#aaaaaa",
            fg_color="transparent"
        ).place(relx=0.5, rely=0.62, anchor="center")

        
        ctk.CTkLabel(
            self.splash_bg,
            text="v1.0 - Tarama Motoru Aktif",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color="#33aa33",
            fg_color="transparent"
        ).place(relx=0.5, rely=0.68, anchor="center")

        
        self.countdown_label = ctk.CTkLabel(
            self.splash_bg,
            text="",
            font=ctk.CTkFont(family="Consolas", size=48, weight="bold"),
            text_color="#00ff41",
            fg_color="transparent"
        )
        self.countdown_label.place(relx=0.5, rely=0.78, anchor="center")

        self.countdown_sub = ctk.CTkLabel(
            self.splash_bg,
            text="Arayüz açılıyor",
            font=ctk.CTkFont(family="Consolas", size=16),
            text_color="#00cc33",
            fg_color="transparent"
        )
        self.countdown_sub.place(relx=0.5, rely=0.74, anchor="center")

        
        ctk.CTkLabel(
            self.splash_bg,
            text="https://cyberanka.com",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#335533",
            fg_color="transparent"
        ).place(relx=0.5, rely=0.95, anchor="center")

        self.countdown_remaining = 4
        self.root.attributes("-alpha", 1)
        self.do_countdown()

    def do_countdown(self):
       
        if self.splash_phase == 2:
            return
        if self.countdown_remaining > 0:
            self.countdown_label.configure(text=str(self.countdown_remaining))
            dots = "." * (5 - self.countdown_remaining)
            self.countdown_sub.configure(text=f"Arayüz açılıyor{dots}")
            self.countdown_remaining -= 1
            self.root.after(1000, self.do_countdown)
        else:
            self.countdown_label.configure(text="GO")
            self.splash_phase = 2
            if self.splash_bg and self.splash_bg.winfo_exists():
                self.splash_bg.destroy()
            self.splash_bg = None
            self._final_setup()

    def _final_setup(self):
        
        self.splash_phase = 2
        self.logo_img_pil = self.download_subflame_logo()
        self.anka_img_pil = self.download_anka_logo()
        self.bg_logo_img_pil = self.download_bg_logo()
        self._build_gui()

    def _build_gui(self):
        
        for w in self.root.winfo_children():
            w.destroy()

        main = ctk.CTkFrame(self.root, fg_color="#0a0a0a", corner_radius=0)
        main.pack(fill=ctk.BOTH, expand=True)

        
        top_bar = ctk.CTkFrame(main, fg_color="#661111", height=4, corner_radius=0)
        top_bar.pack(fill=ctk.X, side=ctk.TOP)

        
        header = ctk.CTkFrame(main, fg_color="#111111", height=85, corner_radius=0)
        header.pack(fill=ctk.X, side=ctk.TOP)
        header.pack_propagate(False)

        
        brand_left = ctk.CTkFrame(header, fg_color="transparent")
        brand_left.pack(side=ctk.LEFT, padx=(10, 3))

        if self.anka_img_pil:
            try:
                sm_logo = self.anka_img_pil.copy()
                sm_logo.thumbnail((50, 50), Image.LANCZOS)
                self.anka_logo_small = ImageTk.PhotoImage(sm_logo)
                ctk.CTkLabel(
                    brand_left, text="", image=self.anka_logo_small,
                    fg_color="transparent"
                ).pack(side=ctk.LEFT, padx=(0, 6))
            except Exception:
                pass

        brand_text = ctk.CTkFrame(brand_left, fg_color="transparent")
        brand_text.pack(side=ctk.LEFT)

        title_row = ctk.CTkFrame(brand_text, fg_color="transparent")
        title_row.pack(anchor="w")
        ctk.CTkLabel(
            title_row, text="Cyber",
            font=ctk.CTkFont(family="Montserrat", size=20, weight="bold"),
            text_color="#ff6666", fg_color="transparent"
        ).pack(side=ctk.LEFT)
        ctk.CTkLabel(
            title_row, text="Anka",
            font=ctk.CTkFont(family="Montserrat", size=20, weight="normal"),
            text_color="#ff8888", fg_color="transparent"
        ).pack(side=ctk.LEFT)
        ctk.CTkLabel(
            title_row, text="  GÖZCÜ",
            font=ctk.CTkFont(family="Consolas", size=16, weight="bold"),
            text_color="#00ff41", fg_color="transparent"
        ).pack(side=ctk.LEFT)

        self.brand_desc = ctk.CTkLabel(
            brand_text,
            text="Port Tarama · DNS Keşif · WAF Tespit · OS Fingerprinting",
            font=ctk.CTkFont(family="Montserrat", size=10),
            text_color="#aaaaaa", fg_color="transparent"
        )
        self.brand_desc.pack(anchor="w")

        
        self.status_label = ctk.CTkLabel(
            header, text="[ HAZIR ]",
            font=ctk.CTkFont(family="Consolas", size=13, weight="bold"),
            text_color="#00ff41", fg_color="transparent"
        )
        self.status_label.pack(side=ctk.LEFT, padx=(15, 0))

        
        counter_frame = ctk.CTkFrame(header, fg_color="transparent")
        counter_frame.pack(side=ctk.RIGHT, padx=(0, 15))

        self.live_counter = ctk.CTkLabel(
            counter_frame, text="[ 0 açık port ]",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color="#ff6666", fg_color="transparent"
        )
        self.live_counter.pack(side=ctk.RIGHT, padx=(0, 8))

        self.time_counter = ctk.CTkLabel(
            counter_frame, text="( 0.0s )",
            font=ctk.CTkFont(family="Consolas", size=12),
            text_color="#66aaff", fg_color="transparent"
        )
        self.time_counter.pack(side=ctk.RIGHT, padx=(0, 5))

        self.target_label = ctk.CTkLabel(
            header, text="",
            font=ctk.CTkFont(family="Consolas", size=11),
            text_color="#aaaaaa", fg_color="transparent"
        )
        self.target_label.pack(side=ctk.RIGHT, padx=(0, 15))

        
        self.term_container = ctk.CTkFrame(main, fg_color="#0a0a0a", corner_radius=0)
        self.term_container.pack(fill=ctk.BOTH, expand=True, padx=0, pady=(0, 0))

        self.term_frame = ctk.CTkFrame(self.term_container, fg_color="#000000", corner_radius=0)
        self.term_frame.pack(fill=ctk.BOTH, expand=True, padx=0, pady=0)

        
        bg_frame = ctk.CTkFrame(self.term_frame, fg_color="#000000", corner_radius=0)
        bg_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=1, relheight=1)
        bg_frame.lower()

        if self.bg_logo_img_pil:
            try:
                big_logo = self.bg_logo_img_pil.copy()
                tw = self.term_frame.winfo_width() if self.term_frame.winfo_width() > 100 else 1000
                th = self.term_frame.winfo_height() if self.term_frame.winfo_height() > 100 else 600
                big_logo.thumbnail((int(tw * 1.5), int(th * 1.5)), Image.LANCZOS)
                if big_logo.mode == 'RGBA':
                    r, g, b, a = big_logo.split()
                    a = a.point(lambda i: max(0, int(i * 0.06)))
                    big_logo = Image.merge('RGBA', (r, g, b, a))
                else:
                    big_logo = big_logo.convert('RGBA')
                    datas = big_logo.getdata()
                    new_data = [(r, g, b, 15) for (r, g, b, a) in datas]
                    big_logo.putdata(new_data)
                self.bg_logo_big = ImageTk.PhotoImage(big_logo)
                ctk.CTkLabel(
                    bg_frame, text="", image=self.bg_logo_big, fg_color="transparent"
                ).place(relx=0.5, rely=0.5, anchor="center")
            except Exception:
                pass

       
        term_title = ctk.CTkFrame(self.term_frame, fg_color="#111111", height=26, corner_radius=0)
        term_title.pack(fill=ctk.X, side=ctk.TOP)
        term_title.pack_propagate(False)

        for i, color in enumerate(["#ff4444", "#ffaa00", "#00ff41"]):
            ctk.CTkLabel(
                term_title, text="●", font=ctk.CTkFont(size=10),
                text_color=color, fg_color="transparent"
            ).pack(side=ctk.LEFT, padx=(4 if i == 0 else 2, 1))

        ctk.CTkLabel(
            term_title, text="root@gozcu:~$",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color="#ff6666", fg_color="transparent"
        ).pack(side=ctk.LEFT, padx=(10, 0))

        
        self.terminal = ctk.CTkTextbox(
            self.term_frame,
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="#000000", text_color="#ffffff",
            border_color="#111111", border_width=1,
            corner_radius=0, wrap="word", activate_scrollbars=True
        )
        self.terminal.pack(fill=ctk.BOTH, expand=True)

        
        for tag, color in [
            ("green", "#00ff41"), ("cyan", "#66ccff"), ("red", "#ff4444"),
            ("yellow", "#ffcc44"), ("purple", "#cc88ff"), ("dim", "#666666"),
            ("orange", "#ff8844"), ("white", "#ffffff"), ("blue", "#4488ff"),
            ("pink", "#ff66aa"), ("lime", "#88ff44"),
            ("h_http", "#ff8844"), ("h_https", "#44ddaa"),
            ("h_waf", "#ff66aa"), ("h_os", "#66ccff"),
            ("h_dns", "#ffcc44"), ("h_tech", "#cc88ff"),
        ]:
            self.terminal.tag_config(tag, foreground=color)

        # Progress bar
        self.progress = ctk.CTkProgressBar(
            self.term_frame, fg_color="#111111", progress_color="#ff6666",
            height=4, corner_radius=0
        )
        self.progress.pack(fill=ctk.X, padx=0, pady=0)
        self.progress.set(0)

        
        
        
        self.results_frame = ctk.CTkFrame(main, fg_color="#0a0a0a", height=140, corner_radius=0)
        self.results_frame.pack(fill=ctk.X, side=ctk.TOP, padx=0, pady=(1, 1))
        self.results_frame.pack_propagate(False)

        
        results_inner = ctk.CTkFrame(self.results_frame, fg_color="#0a0a0a")
        results_inner.pack(fill=ctk.BOTH, expand=True, padx=5, pady=3)

        
        stats_row = ctk.CTkFrame(results_inner, fg_color="transparent")
        stats_row.pack(fill=ctk.X, pady=(0, 3))

        self.stat_cards = {}
        stat_items = [
            ("open", "AÇIK PORT", "0", "#ff6666"),
            ("http", "HTTP", "0", "#ff8844"),
            ("https", "HTTPS", "0", "#44ddaa"),
            ("waf", "WAF TESPİT", "-", "#ff66aa"),
            ("os", "İŞLETİM SİSTEMİ", "-", "#66ccff"),
            ("dns", "DNS KAYDI", "-", "#ffcc44"),
            ("service", "SERVİS", "0", "#cc88ff"),
            ("tech", "TEKNOLOJİ", "-", "#88ff44"),
        ]

        for key, label, default, color in stat_items:
            card = ctk.CTkFrame(stats_row, fg_color="#111111", corner_radius=4,
                                height=32, width=120)
            card.pack(side=ctk.LEFT, padx=(0, 4))
            card.pack_propagate(False)

            inner_c = ctk.CTkFrame(card, fg_color="transparent")
            inner_c.pack(fill=ctk.BOTH, expand=True, padx=6, pady=2)

            ctk.CTkLabel(
                inner_c, text=label,
                font=ctk.CTkFont(family="Consolas", size=9),
                text_color="#777777", fg_color="transparent"
            ).pack(anchor="w")

            val_label = ctk.CTkLabel(
                inner_c, text=default,
                font=ctk.CTkFont(family="Consolas", size=12, weight="bold"),
                text_color=color, fg_color="transparent"
            )
            val_label.pack(anchor="w")
            self.stat_cards[key] = val_label

        
        detail_row = ctk.CTkFrame(results_inner, fg_color="transparent")
        detail_row.pack(fill=ctk.X)

        ctk.CTkLabel(
            detail_row, text="🔍",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#555555", fg_color="transparent"
        ).pack(side=ctk.LEFT, padx=(2, 3))

        self.filter_entry = ctk.CTkEntry(
            detail_row,
            placeholder_text="Filtre: port, servis, durum... (örn: 80,443,open,http)",
            font=ctk.CTkFont(family="Consolas", size=11),
            fg_color="#1a0a0a", text_color="#ffffff",
            placeholder_text_color="#555555", border_color="#661111",
            border_width=1, corner_radius=3, height=26
        )
        self.filter_entry.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=(3, 3))
        self.filter_entry.bind("<Return>", self.on_filter_search)

        self.btn_filter = ctk.CTkButton(
            detail_row, text="ARA",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            fg_color="#661111", hover_color="#882222",
            text_color="#ffffff", height=26, width=50, corner_radius=3,
            command=self.on_filter_search
        )
        self.btn_filter.pack(side=ctk.LEFT, padx=(0, 3))

        self.btn_filter_clear = ctk.CTkButton(
            detail_row, text="X",
            font=ctk.CTkFont(family="Consolas", size=10, weight="bold"),
            fg_color="#882222", hover_color="#993333",
            text_color="#ffffff", height=26, width=26, corner_radius=3,
            command=self.on_filter_clear
        )
        self.btn_filter_clear.pack(side=ctk.LEFT, padx=(0, 5))

        self.filter_count_label = ctk.CTkLabel(
            detail_row, text="[ 0 / 0 ]",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color="#ff8888", fg_color="transparent", width=70
        )
        self.filter_count_label.pack(side=ctk.RIGHT, padx=(0, 10))

        
       
        
        cmd_frame = ctk.CTkFrame(main, fg_color="#111111", height=52, corner_radius=0)
        cmd_frame.pack(fill=ctk.X, side=ctk.BOTTOM, padx=0, pady=(1, 2))
        cmd_frame.pack_propagate(False)

        ctk.CTkLabel(
            cmd_frame, text="root@gozcu:~$",
            font=ctk.CTkFont(family="Consolas", size=14, weight="bold"),
            text_color="#ff6666", fg_color="transparent"
        ).pack(side=ctk.LEFT, padx=(12, 6))

        self.entry = ctk.CTkEntry(
            cmd_frame,
            placeholder_text="ornek.com veya IP adresi (örn: 192.168.1.1 veya hedefler.txt)",
            font=ctk.CTkFont(family="Consolas", size=13),
            fg_color="#1a0a0a", text_color="#ffffff",
            placeholder_text_color="#555555", border_color="#661111",
            border_width=1, corner_radius=4, height=34
        )
        self.entry.pack(side=ctk.LEFT, fill=ctk.X, expand=True, padx=(3, 6))
        self.entry.bind("<Return>", lambda e: self.start_scan())

        
        btn_frame = ctk.CTkFrame(cmd_frame, fg_color="transparent")
        btn_frame.pack(side=ctk.RIGHT, padx=(0, 6))

        bs = {"font": ctk.CTkFont(family="Consolas", size=10, weight="bold"),
              "height": 32, "corner_radius": 4}

        self.btn_scan = ctk.CTkButton(
            btn_frame, text="▶ TARA", fg_color="#661111",
            hover_color="#882222", text_color="#ffffff", width=70,
            command=self.start_scan, **bs
        )
        self.btn_scan.pack(side=ctk.LEFT, padx=2)

        self.btn_pause = ctk.CTkButton(
            btn_frame, text="⏸ DURAKLAT", fg_color="#884422",
            hover_color="#995533", text_color="#ffffff", width=100,
            command=self.toggle_pause, state=ctk.DISABLED, **bs
        )
        self.btn_pause.pack(side=ctk.LEFT, padx=2)

        self.btn_stop = ctk.CTkButton(
            btn_frame, text="⏹ DURDUR", fg_color="#882222",
            hover_color="#993333", text_color="#ffffff", width=80,
            command=self.stop_operation, state=ctk.DISABLED, **bs
        )
        self.btn_stop.pack(side=ctk.LEFT, padx=2)

        self.btn_dns = ctk.CTkButton(
            btn_frame, text="🌐 DNS SORGULA", fg_color="#224488",
            hover_color="#335599", text_color="#ffffff", width=120,
            command=self.run_dns_lookup, state=ctk.DISABLED, **bs
        )
        self.btn_dns.pack(side=ctk.LEFT, padx=2)

        self.btn_export = ctk.CTkButton(
            btn_frame, text="💾 DIŞA AKTAR", fg_color="#444444",
            hover_color="#555555", text_color="#ffffff", width=100,
            command=self.export_results, state=ctk.DISABLED, **bs
        )
        self.btn_export.pack(side=ctk.LEFT, padx=2)

        self.btn_clear = ctk.CTkButton(
            btn_frame, text="🗑 TEMİZLE", fg_color="#444444",
            hover_color="#555555", text_color="#ffffff", width=80,
            command=self.clear_terminal, **bs
        )
        self.btn_clear.pack(side=ctk.LEFT, padx=2)

        
        
        
        settings_frame = ctk.CTkFrame(main, fg_color="#111111", height=34, corner_radius=0)
        settings_frame.pack(fill=ctk.X, side=ctk.BOTTOM, padx=0, pady=(0, 0))
        settings_frame.pack_propagate(False)

        ctk.CTkLabel(
            settings_frame, text="İş Parçacığı:",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#777777", fg_color="transparent"
        ).pack(side=ctk.LEFT, padx=(10, 3))

        ts = ctk.CTkSlider(
            settings_frame, from_=10, to=500, number_of_steps=49,
            variable=self.thread_count, fg_color="#222222",
            progress_color="#ff6666", button_color="#ff6666",
            button_hover_color="#ff8888", width=100, height=12,
            command=self.on_thread_change
        )
        ts.pack(side=ctk.LEFT, padx=(1, 3))
        self.thread_label = ctk.CTkLabel(
            settings_frame, text="100",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color="#ff6666", fg_color="transparent", width=30
        )
        self.thread_label.pack(side=ctk.LEFT, padx=(0, 5))

        for v, l in [(50, "Yavaş"), (100, "Normal"), (500, "Hızlı")]:
            ctk.CTkButton(
                settings_frame, text=l,
                font=ctk.CTkFont(family="Consolas", size=8),
                fg_color="#222222", hover_color="#333333",
                text_color="#999999", height=20, width=45, corner_radius=2,
                command=lambda val=v: self.set_thread_preset(val)
            ).pack(side=ctk.LEFT, padx=2)

        ctk.CTkLabel(
            settings_frame, text="Zaman Aşımı:",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#777777", fg_color="transparent"
        ).pack(side=ctk.LEFT, padx=(5, 3))

        ts2 = ctk.CTkSlider(
            settings_frame, from_=1, to=10, number_of_steps=9,
            variable=self.timeout_value, fg_color="#222222",
            progress_color="#884422", button_color="#884422",
            button_hover_color="#995533", width=60, height=12,
            command=self.on_timeout_change
        )
        ts2.pack(side=ctk.LEFT, padx=(1, 3))
        self.timeout_label = ctk.CTkLabel(
            settings_frame, text="1s",
            font=ctk.CTkFont(family="Consolas", size=11, weight="bold"),
            text_color="#884422", fg_color="transparent", width=25
        )
        self.timeout_label.pack(side=ctk.LEFT, padx=(0, 5))

        
        ctk.CTkLabel(
            settings_frame, text="Port:",
            font=ctk.CTkFont(family="Consolas", size=10),
            text_color="#777777", fg_color="transparent"
        ).pack(side=ctk.LEFT, padx=(5, 2))

        self.port_mode_btn_full = ctk.CTkButton(
            settings_frame, text="TÜMÜ",
            font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
            fg_color="#661111", hover_color="#882222",
            text_color="#ffffff", height=22, width=45, corner_radius=2,
            command=lambda: self.set_port_mode("full")
        )
        self.port_mode_btn_full.pack(side=ctk.LEFT, padx=1)

        self.port_mode_btn_web = ctk.CTkButton(
            settings_frame, text="WEB",
            font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
            fg_color="#333333", hover_color="#444444",
            text_color="#999999", height=22, width=40, corner_radius=2,
            command=lambda: self.set_port_mode("web")
        )
        self.port_mode_btn_web.pack(side=ctk.LEFT, padx=1)

        self.port_mode_btn_custom = ctk.CTkButton(
            settings_frame, text="ÖZEL",
            font=ctk.CTkFont(family="Consolas", size=9, weight="bold"),
            fg_color="#333333", hover_color="#444444",
            text_color="#999999", height=22, width=40, corner_radius=2,
            command=lambda: self.set_port_mode("custom")
        )
        self.port_mode_btn_custom.pack(side=ctk.LEFT, padx=(1, 3))

        self.custom_port_entry = ctk.CTkEntry(
            settings_frame,
            placeholder_text="örn: 80,443,8080,3306",
            font=ctk.CTkFont(family="Consolas", size=10),
            fg_color="#1a0a0a", text_color="#ffffff",
            placeholder_text_color="#444444", border_color="#333333",
            border_width=1, corner_radius=2, height=22, width=120
        )
        self.custom_port_entry.pack(side=ctk.LEFT, padx=(0, 5))

        ctk.CTkLabel(
            settings_frame, text="cyberanka.com",
            font=ctk.CTkFont(family="Consolas", size=9),
            text_color="#333333", fg_color="transparent"
        ).pack(side=ctk.RIGHT, padx=(0, 10))

        
        self._print_banner()
        self._print("", "dim")
        self._print("[TAMAM] CyberAnka Gözcü v1.0 hazır", "green")
        self._print(f"[TAMAM] {len(ALL_PORTS)} port tanımlı | {len(WAF_SIGS)} WAF imzası | {len(OS_SIGS)} OS imzası", "green")
        self._print("", "dim")
        self._print("root@gozcu:~$ Hedef alan adı veya IP girin ve ENTER'a basın", "green")
        self._print("root@gozcu:~$ Örnek: ornek.com | 8.8.8.8 | hedefler.txt", "dim")
        self._print("─" * 70, "dim")

        self.root.bind("<F11>", lambda e: self.toggle_fullscreen())

    
    
    

    def set_port_mode(self, mode):
        self.port_mode.set(mode)
        
        full_color = "#661111" if mode == "full" else "#333333"
        web_color = "#661111" if mode == "web" else "#333333"
        custom_color = "#661111" if mode == "custom" else "#333333"
        full_text = "#ffffff" if mode == "full" else "#999999"
        web_text = "#ffffff" if mode == "web" else "#999999"
        custom_text = "#ffffff" if mode == "custom" else "#999999"

        self.port_mode_btn_full.configure(fg_color=full_color, text_color=full_text)
        self.port_mode_btn_web.configure(fg_color=web_color, text_color=web_text)
        self.port_mode_btn_custom.configure(fg_color=custom_color, text_color=custom_text)

        if mode == "custom":
            self.custom_port_entry.configure(border_color="#661111")
        else:
            self.custom_port_entry.configure(border_color="#333333")

    def get_target_ports(self):
        
        mode = self.port_mode.get()
        if mode == "web":
            web_ports = []
            for p, (svc, cat) in SERVICE_MAP.items():
                if "HTTP" in svc.upper() or "HTTPS" in svc.upper():
                    web_ports.append(p)
                elif cat == "Web":
                    web_ports.append(p)
            return sorted(set(web_ports))
        elif mode == "custom":
            raw = self.custom_port_entry.get().strip()
            if raw:
                ports = []
                for part in raw.split(","):
                    part = part.strip()
                    if '-' in part:
                        try:
                            a, b = part.split('-', 1)
                            ports.extend(range(int(a), int(b) + 1))
                        except ValueError:
                            pass
                    else:
                        try:
                            ports.append(int(part))
                        except ValueError:
                            pass
                return sorted(set(p for p in ports if 1 <= p <= 65535))
            else:
                return ALL_PORTS
        else:
            return ALL_PORTS

    
    
    

    def start_scan(self):
        target_input = self.entry.get().strip()
        target_input = re.sub(r'^https?://', '', target_input).split('/')[0].strip()
        if not target_input:
            self._print("HATA: Hedef girilmedi!", "red")
            return
        if target_input.lower() in ("exit", "quit"):
            self.root.destroy()
            return
        if self.current_operation != "bekliyor":
            self._print("UYARI: Zaten bir işlem devam ediyor!", "yellow")
            return

        
        if os.path.isfile(target_input):
            targets = self.read_targets_from_file(target_input)
            if not targets:
                self._print("HATA: Dosyada geçerli hedef bulunamadı!", "red")
                return
            self._print(f"{len(targets)} hedef yüklendi: {target_input}", "cyan")
            for d in targets[:3]:
                self._print(f"  - {d}", "dim")
            if len(targets) > 3:
                self._print(f"  ... ve {len(targets)-3} hedef daha", "dim")
        else:
            targets = [target_input]

        
        ip = resolve_target(target_input)
        if not ip and not os.path.isfile(target_input):
            self._print(f"HATA: '{target_input}' çözümlenemedi veya engellendi!", "red")
            return

        self.target_domain = target_input
        self.target_ip = ip or target_input

        self.scan_results = []
        self.http_results = {}
        self.dns_results = {}
        self.os_result = {}
        self.scan_start_time = time.time()
        self.progress.set(0)

        self.update_stats()
        self.operation_started("tarama")

        
        self._print("+" + "-" * 68 + "+", "cyan")
        self._print(f"| HEDEF : {self.target_domain}", "cyan")
        self._print(f"| IP     : {self.target_ip}", "cyan")
        self._print(f"| PORT   : {self.port_mode.get().upper()} mod", "cyan")
        self._print(f"| ZAMAN  : {time.strftime('%H:%M:%S')}", "cyan")
        self._print(f"| THREAD : {self.thread_count.get()}", "cyan")
        self._print("+" + "-" * 68 + "+", "cyan")
        self._print("Port taraması başlatılıyor...", "yellow")
        self._print("", "dim")

        self.target_label.configure(text=f"[ {self.target_ip} ]")
        self.update_time_counter()

        threading.Thread(target=self._do_os_fingerprint, args=(ip,), daemon=True).start()

        if not is_ip(self.target_domain):
            threading.Thread(target=self._auto_dns_scan, args=(self.target_domain,), daemon=True).start()

        t = threading.Thread(target=self._run_port_scan, args=(ip,), daemon=True)
        t.start()

    def _do_os_fingerprint(self, ip):
        self._print("[OS] İşletim sistemi tespiti yapılıyor...", "h_os")
        result = ping_fingerprint(ip)
        self.os_result = result
        self.root.after(0, lambda: self.stat_cards["os"].configure(text=result["os"]))
        self._print(
            f"[OS] TTL: {result['ttl']} | Window: {result['win_size']} | "
            f"DF: {result['df']} -> {result['os']}",
            "h_os"
        )

    def _auto_dns_scan(self, domain):
        domain = re.sub(r'^https?://', '', domain).split('/')[0].strip()
        self._print(f"[DNS] Otomatik DNS sorgulama başlatıldı: {domain}", "h_dns")
        results = dns_lookup(domain)
        self.dns_results[domain] = results
        total_records = sum(len(v) for v in results.values())
        self.root.after(0, lambda: self.stat_cards["dns"].configure(text=str(total_records)))
        for rtype, records in results.items():
            if records:
                self._print(f"[DNS] {rtype}: {', '.join(records[:3])}{'...' if len(records)>3 else ''}", "h_dns")
        self._print(f"[DNS] Toplam {total_records} kayıt bulundu.", "h_dns")

    def _run_port_scan(self, ip):
        target_ports = self.get_target_ports()
        total_ports = len(target_ports)
        batch_size = min(self.thread_count.get(), 500)
        batch_size = max(50, batch_size)
        completed = 0
        open_count = 0
        last_print_pct = -1

        self._print(f"[TARAMA] {total_ports} port taranıyor ({batch_size} paralel)...", "cyan")

        banner_pool = concurrent.futures.ThreadPoolExecutor(max_workers=30)

        for i in range(0, total_ports, batch_size):
            if self.stopped:
                break
            self.pause_event.wait()
            if self.stopped:
                break

            batch = target_ports[i:i + batch_size]
            open_ports = parallel_tcp_scan(ip, batch, timeout=max(0.3, self.timeout_value.get() * 0.5))

            for port in open_ports:
                svc_name, svc_cat = get_service_info(port)
                self.scan_results.append({
                    "port": port,
                    "service": svc_name,
                    "category": svc_cat,
                    "state": "open",
                    "banner": "",
                    "service_detected": ""
                })
                open_count += 1
                banner_pool.submit(self._grab_banner, ip, port, svc_name, svc_cat)

            completed += len(batch)
            progress = min(completed / total_ports, 1.0)
            pct = int(progress * 100)
            elapsed_now = time.time() - self.scan_start_time

            if pct != last_print_pct and pct % 10 == 0:
                last_print_pct = pct
                self._print(
                    f"[TARAMA] %{pct:3d} | {completed}/{total_ports} port | {open_count} açık | {elapsed_now:.1f}s",
                    "dim"
                )

            self.root.after(0, lambda p=progress: self.progress.set(p))
            self.root.after(0, lambda c=open_count: self.stat_cards["open"].configure(text=str(c)))
            self.root.after(0, lambda c=open_count: self.live_counter.configure(
                text=f"[ {c} açık port ]"
            ))

        banner_pool.shutdown(wait=True)

        if not self.stopped:
            elapsed = time.time() - self.scan_start_time
            self.root.after(0, self._scan_done, open_count, elapsed)

    def _grab_banner(self, ip, port, svc_name, svc_cat):
        
        banner = ""
        service_detected = ""

        
        svc_upper = svc_name.upper()
        is_http = "HTTP" in svc_upper and "HTTPS" not in svc_upper
        is_https = "HTTPS" in svc_upper

        if is_http or port in [80, 8080, 8000, 8888, 3000, 5000, 9000, 8081, 8090]:
            result = http_probe(ip, port, use_ssl=False)
            self.http_results[port] = result
            banner = result["server"] or f"HTTP {result['status_code']}"
            service_detected = result.get("title", "")[:60]

           
            if result.get("waf"):
                self.root.after(0, lambda w=result["waf"]: self.stat_cards["waf"].configure(text=w))
                self._print(f"[WAF] Port {port}: {result['waf']} tespit edildi!", "h_waf")

           
            if result.get("tech"):
                tech_str = ", ".join(result["tech"])
                self.root.after(0, lambda t=tech_str: self.stat_cards["tech"].configure(text=tech_str[:30]))
                self._print(f"[TECH] Port {port}: {tech_str}", "h_tech")

            
            if result["status_code"] == 200 or "200" in str(result["status_code"]):
                self._print(f"[HTTP] :{port} -> {result['status_code']} | {result.get('title','')[:50]} | {result.get('server','')}", "h_http")
            elif result["status_code"] in (301, 302, 307, 308):
                self._print(f"[HTTP] :{port} -> {result['status_code']} (Yönlendirme) | {result.get('title','')[:50]}", "yellow")
            else:
                self._print(f"[HTTP] :{port} -> {result['status_code']} | {result.get('title','')[:50]}", "dim")

            
            self.root.after(0, self._update_http_count)

        elif is_https or port in [443, 8443, 9443, 4443, 7443]:
            result = http_probe(ip, port, use_ssl=True)
            self.http_results[port] = result
            banner = result["server"] or f"HTTPS {result['status_code']}"
            service_detected = result.get("title", "")[:60]

            if result.get("waf"):
                self.root.after(0, lambda w=result["waf"]: self.stat_cards["waf"].configure(text=w))
                self._print(f"[WAF] Port {port}: {result['waf']} tespit edildi!", "h_waf")

            if result.get("tech"):
                tech_str = ", ".join(result["tech"])
                self.root.after(0, lambda t=tech_str: self.stat_cards["tech"].configure(text=tech_str[:30]))
                self._print(f"[TECH] Port {port}: {tech_str}", "h_tech")

            if result["status_code"] == 200:
                self._print(f"[HTTPS] :{port} -> {result['status_code']} | {result.get('title','')[:50]} | {result.get('server','')}", "h_https")
            elif result["status_code"] in (301, 302, 307, 308):
                self._print(f"[HTTPS] :{port} -> {result['status_code']} (Yönlendirme) | {result.get('title','')[:50]}", "yellow")
            else:
                self._print(f"[HTTPS] :{port} -> {result['status_code']} | {result.get('title','')[:50]}", "dim")

            self.root.after(0, self._update_https_count)

        else:
            
            b, bd = banner_grab(ip, port, svc_name)
            banner = b
            service_detected = bd

        
        for res in self.scan_results:
            if res["port"] == port:
                res["banner"] = banner
                res["service_detected"] = service_detected
                break

        
        if not is_http and not is_https and not (
            port in [80, 8080, 8000, 8888, 3000, 5000, 9000, 8081, 8090,
                     443, 8443, 9443, 4443, 7443]
        ):
            cat_color = "green"
            if svc_cat == "Veritabani":
                cat_color = "purple"
            elif svc_cat in ("Guvenlik", "Yonetim"):
                cat_color = "red"
            elif svc_cat in ("E-Posta", "Mesajlasma/Kuyruk"):
                cat_color = "yellow"
            elif svc_cat == "Ag":
                cat_color = "blue"

            banner_str = f" | {banner}" if banner else ""
            detected_str = f" [{service_detected}]" if service_detected else ""
            self._print(
                f"[+] :{port:<5} {svc_name:<20} [{svc_cat}]{banner_str}{detected_str}",
                cat_color
            )

        
        self.root.after(0, self._update_service_count)

    def _update_http_count(self):
        http_count = sum(1 for p, r in self.http_results.items()
                         if r.get("status_code", 0) > 0 and
                         "HTTPS" not in SERVICE_MAP.get(p, ("", ""))[0].upper())
        self.stat_cards["http"].configure(text=str(http_count))

    def _update_https_count(self):
        https_count = sum(1 for p, r in self.http_results.items()
                          if r.get("status_code", 0) > 0 and
                          "HTTPS" in SERVICE_MAP.get(p, ("", ""))[0].upper())
        self.stat_cards["https"].configure(text=str(https_count))

    def _update_service_count(self):
        count = sum(1 for r in self.scan_results if r.get("service_detected", ""))
        self.stat_cards["service"].configure(text=str(count))

    def _scan_done(self, open_count, elapsed):
        """Tarama tamamlandı"""
        self.progress.set(1)

        http_count = sum(1 for r in self.http_results.values() if r.get("status_code", 0) > 0)
        https_count = sum(1 for p, r in self.http_results.items()
                          if r.get("status_code", 0) > 0 and
                          ("HTTPS" in SERVICE_MAP.get(p, ("", ""))[0].upper() or p in [443, 8443, 9443, 4443]))
        tech_set = set()
        for r in self.http_results.values():
            for t in r.get("tech", []):
                tech_set.add(t)
        waf_set = set()
        for r in self.http_results.values():
            if r.get("waf"):
                waf_set.add(r["waf"])

        self._print("+" + "-" * 68 + "+", "cyan")
        self._print(f"| TARAMA TAMAMLANDI!", "cyan")
        self._print(f"| Süre: {elapsed:.2f}s", "cyan")
        self._print(f"| Açık Port: {open_count} | HTTP: {http_count} | HTTPS: {https_count}", "cyan")
        if tech_set:
            self._print(f"| Teknoloji: {', '.join(sorted(tech_set))}", "cyan")
        if waf_set:
            self._print(f"| WAF: {', '.join(waf_set)}", "cyan")
        self._print("+" + "-" * 68 + "+", "cyan")

        self.stat_cards["open"].configure(text=str(open_count))
        self.stat_cards["http"].configure(text=str(http_count))
        self.stat_cards["https"].configure(text=str(https_count))

        self.filter_count_label.configure(text=f"[ {open_count} / {open_count} ]")

        self._print("Kullan: DNS SORGULA -> DNS kayıtlarını görüntüle", "yellow")
        self._print("Kullan: DIŞA AKTAR -> Excel olarak kaydet", "yellow")
        self._print("─" * 70, "dim")

        self.operation_finished()

    
    
    

    def run_dns_lookup(self):
        domain_raw = self.entry.get().strip() if not self.target_domain else self.target_domain
        domain_raw = re.sub(r'^https?://', '', domain_raw).split('/')[0].strip()

        if not domain_raw:
            self._print("DNS sorgulama için alan adı gerekli!", "yellow")
            return

        if is_ip(domain_raw):
            self._print("DNS sorgulama için IP değil, alan adı girilmeli!", "yellow")
            return

        if self.current_operation not in ("bekliyor", "tarama"):
            self._print("UYARI: Zaten bir DNS işlemi devam ediyor!", "yellow")
            return

        domain = domain_raw

        self._print("+" + "-" * 68 + "+", "cyan")
        self._print(f"| DNS SORGULAMA: {domain}", "cyan")
        self._print("+" + "-" * 68 + "+", "cyan")

        def _query():
            results = dns_lookup(domain)
            self.dns_results[domain] = results

            total_records = sum(len(v) for v in results.values())
            self.root.after(0, lambda: self.stat_cards["dns"].configure(text=str(total_records)))

            for rtype, records in results.items():
                if records:
                    self._print(f"[DNS] {rtype} ({len(records)} kayıt):", "h_dns")
                    for rec in records[:10]:
                        self._print(f"      {rec}", "dim")
                    if len(records) > 10:
                        self._print(f"      ... ve {len(records)-10} kayıt daha", "dim")
                else:
                    self._print(f"[DNS] {rtype}: Kayıt bulunamadı", "dim")

            self._print("DNS sorgulama tamamlandı.", "green")
            self._print("─" * 70, "dim")

            if self.current_operation == "dns":
                self.root.after(0, self.operation_finished)

        if self.current_operation == "bekliyor":
            self.operation_started("dns")
            threading.Thread(target=_query, daemon=True).start()
        else:
            threading.Thread(target=_query, daemon=True).start()


    def on_filter_search(self, event=None):
       
        raw = self.filter_entry.get().strip().lower()
        if not self.scan_results:
            return

        queries = [q.strip() for q in raw.split(",") if q.strip()]

        
        filtered = []
        for r in self.scan_results:
            if not queries:
                filtered.append(r)
                continue

            match = False
            for q in queries:
                if not q:
                    continue
                
                if q.isdigit() and r["port"] == int(q):
                    match = True
                    break
                
                if q in r["service"].lower():
                    match = True
                    break
                
                if q in r["category"].lower():
                    match = True
                    break
                
                if q in r["state"].lower():
                    match = True
                    break
                
                http_r = self.http_results.get(r["port"], {})
                if http_r:
                    if q == str(http_r.get("status_code", "")):
                        match = True
                        break
                    if http_r.get("waf") and q in http_r["waf"].lower():
                        match = True
                        break
                    for tech in http_r.get("tech", []):
                        if q in tech.lower():
                            match = True
                            break
                    if match:
                        break

            if match:
                filtered.append(r)

        
        self.terminal.delete("1.0", ctk.END)
        self._print_banner()

        if not filtered:
            self._print("Eşleşen sonuç bulunamadı.", "yellow")
            self.filter_count_label.configure(text=f"[ 0 / {len(self.scan_results)} ]")
        else:
            self._print(f"Filtre: '{raw}' -> {len(filtered)} sonuç", "cyan")
            self._print("-" * 70, "dim")
            for r in filtered:
                cat_color = "green"
                if r["category"] == "Web":
                    cat_color = "orange"
                elif r["category"] == "Veritabani":
                    cat_color = "purple"
                elif r["category"] == "Guvenlik":
                    cat_color = "red"
                http_r = self.http_results.get(r["port"], {})
                extra = ""
                if http_r:
                    sc = http_r.get("status_code", 0)
                    title = http_r.get("title", "")[:40]
                    waf = http_r.get("waf", "")
                    techs = http_r.get("tech", [])
                    extra = f" | Kod:{sc} | {title}"
                    if waf:
                        extra += f" | WAF:{waf}"
                    if techs:
                        extra += f" | [{','.join(techs[:3])}]"

                self._print(
                    f"  :{r['port']:<5} {r['service']:<20} [{r['category']}]{extra}",
                    cat_color
                )
            self.filter_count_label.configure(text=f"[ {len(filtered)} / {len(self.scan_results)} ]")

    def on_filter_clear(self):
        """Filtreyi temizle"""
        self.filter_entry.delete(0, ctk.END)
        if not self.scan_results:
            return

        self.terminal.delete("1.0", ctk.END)
        self._print_banner()
        self._print(f"Toplam {len(self.scan_results)} açık port:", "cyan")
        self._print("-" * 70, "dim")

        
        by_cat = {}
        for r in self.scan_results:
            cat = r["category"]
            if cat not in by_cat:
                by_cat[cat] = []
            by_cat[cat].append(r)

        for cat, items in sorted(by_cat.items()):
            cat_color = "green"
            if cat == "Web":
                cat_color = "orange"
            elif cat == "Veritabani":
                cat_color = "purple"
            elif cat == "Guvenlik":
                cat_color = "red"
            elif cat in ("E-Posta", "Mesajlasma/Kuyruk"):
                cat_color = "yellow"
            elif cat == "Ag":
                cat_color = "blue"

            self._print(f"[{cat}] ({len(items)} port):", cat_color)
            for r in items:
                http_r = self.http_results.get(r["port"], {})
                extra = ""
                if http_r:
                    sc = http_r.get("status_code", 0)
                    title = http_r.get("title", "")[:40]
                    if sc:
                        extra = f" | Kod:{sc} | {title}"
                self._print(
                    f"  :{r['port']:<5} {r['service']:<20}{extra}",
                    "dim"
                )

        self.filter_count_label.configure(text=f"[ {len(self.scan_results)} / {len(self.scan_results)} ]")


    def export_results(self):
        if not self.scan_results:
            self._print("Aktarılacak sonuç yok! Önce tarama yapın.", "yellow")
            return

        from tkinter import filedialog
        fp = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML Rapor", "*.html")],
            initialfile=f"cyberanka_gozcu_rapor_{time.strftime('%Y%m%d_%H%M%S')}.html"
        )
        if not fp:
            return

        try:
            os_text = self.os_result.get("os", "Bilinmiyor") if self.os_result else "Bilinmiyor"
            total_dns = 0
            if self.dns_results:
                for res in self.dns_results.values():
                    total_dns += sum(len(v) for v in res.values())
            
            open_count = len(self.scan_results)
            http_count = len(self.http_results)

            html = [
                "<!DOCTYPE html>",
                "<html lang='tr'>",
                "<head>",
                "    <meta charset='UTF-8'>",
                "    <title>CyberAnka Gözcü - Rapor</title>",
                "    <style>",
                "        body { background-color: #0a0a0a; color: #aaaaaa; font-family: 'Consolas', 'Courier New', monospace; margin: 0; padding: 20px; }",
                "        .container { max-width: 1200px; margin: 0 auto; }",
                "        .header { background-color: #111111; padding: 20px; border-top: 4px solid #661111; margin-bottom: 20px; border-radius: 4px; }",
                "        .brand { display: flex; align-items: center; margin-bottom: 15px; }",
                "        .title-cyber { color: #ff6666; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 28px; font-weight: bold; }",
                "        .title-anka { color: #ff8888; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 28px; }",
                "        .title-gozcu { color: #00ff41; font-size: 24px; font-weight: bold; margin-left: 10px; }",
                "        .info-card { background-color: #111111; padding: 20px; margin-bottom: 20px; border-radius: 4px; border-left: 4px solid #00ff41; display:flex; justify-content: space-between; flex-wrap: wrap; gap: 20px; }",
                "        .info-col { flex: 1; min-width: 250px; }",
                "        .info-col h3 { color: #ffffff; margin-top:0; font-family: 'Segoe UI', sans-serif; font-size: 16px; border-bottom: 1px solid #333333; padding-bottom: 8px; margin-bottom: 12px; }",
                "        .info-col div { margin-bottom: 6px; }",
                "        .info-col strong { color: #ffffff; }",
                "        h2 { color: #ffffff; border-bottom: 1px solid #333333; padding-bottom: 10px; font-family: 'Segoe UI', sans-serif; margin-top: 40px; margin-bottom: 15px; }",
                "        table { width: 100%; border-collapse: collapse; margin-bottom: 30px; background-color: #111111; border-radius: 4px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }",
                "        th, td { padding: 12px 15px; text-align: left; border-bottom: 1px solid #222222; font-size: 13px; }",
                "        th { background-color: #1a1a1a; color: #ff6666; font-weight: bold; text-transform: uppercase; font-size: 12px; }",
                "        tr:last-child td { border-bottom: none; }",
                "        tr:hover { background-color: #161616; }",
                "        .badge { padding: 4px 8px; border-radius: 3px; font-size: 11px; font-weight: bold; color: #000; display: inline-block; }",
                "        .bg-web { background-color: #ff8844; }",
                "        .bg-db { background-color: #cc88ff; }",
                "        .bg-sec { background-color: #ff4444; color: #fff; }",
                "        .bg-net { background-color: #4488ff; color: #fff; }",
                "        .bg-def { background-color: #00ff41; }",
                "        .bg-mail { background-color: #ffcc44; }",
                "        .stats { display: flex; gap: 15px; flex-wrap: wrap; margin-bottom: 30px; }",
                "        .stat-box { background-color: #111111; padding: 15px; border-radius: 4px; flex: 1; min-width: 150px; border: 1px solid #222222; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }",
                "        .stat-label { color: #777777; font-size: 12px; margin-bottom: 8px; text-transform: uppercase; font-weight: bold; }",
                "        .stat-value { font-size: 28px; font-weight: bold; color: #00ff41; }",
                "        .val-red { color: #ff6666; }",
                "        .val-orange { color: #ff8844; }",
                "        .val-yellow { color: #ffcc44; }",
                "        .waf-alert { color: #ff66aa; font-weight: bold; }",
                "    </style>",
                "</head>",
                "<body>",
                "    <div class='container'>",
                "        <div class='header'>",
                "            <div class='brand'>",
                "                <span class='title-cyber'>Cyber</span><span class='title-anka'>Anka</span>",
                "                <span class='title-gozcu'>GÖZCÜ</span>",
                "            </div>",
                "            <div style='color: #777; font-size: 13px;'>Port Tarama & Güvenlik Analizi Raporu</div>",
                "        </div>",
                "        <div class='info-card'>",
                "            <div class='info-col'>",
                "                <h3>Hedef Bilgileri</h3>",
                f"                <div>Domain: <strong>{self.target_domain}</strong></div>",
                f"                <div>IP Adresi: <strong>{self.target_ip}</strong></div>",
                f"                <div>İşletim Sistemi: <strong style='color:#66ccff;'>{os_text}</strong></div>",
                "            </div>",
                "            <div class='info-col'>",
                "                <h3>Tarama Detayları</h3>",
                f"                <div>Oluşturulma Tarihi: <strong>{time.strftime('%Y-%m-%d %H:%M:%S')}</strong></div>",
                f"                <div>Tarama Modu: <strong>{self.port_mode.get().upper()}</strong></div>",
                "            </div>",
                "        </div>",
                "        <div class='stats'>",
                f"            <div class='stat-box'><div class='stat-label'>Açık Port</div><div class='stat-value val-red'>{open_count}</div></div>",
                f"            <div class='stat-box'><div class='stat-label'>HTTP(S) Servisi</div><div class='stat-value val-orange'>{http_count}</div></div>",
                f"            <div class='stat-box'><div class='stat-label'>DNS Kaydı</div><div class='stat-value val-yellow'>{total_dns}</div></div>",
                "        </div>"
            ]

            html.append("<h2>Açık Portlar ve Servisler</h2>")
            html.append("<table>")
            html.append("<tr><th>Port</th><th>Servis</th><th>Kategori</th><th>Durum</th><th>Banner / Tespiti</th><th>HTTP Kod</th><th>WAF / Teknoloji</th></tr>")

            for r in self.scan_results:
                port = r['port']
                svc = r['service']
                cat = r['category']
                http_r = self.http_results.get(port, {})
                
                cat_class = "bg-def"
                if cat == "Web": cat_class = "bg-web"
                elif cat == "Veritabani": cat_class = "bg-db"
                elif cat == "Guvenlik": cat_class = "bg-sec"
                elif cat == "Ag": cat_class = "bg-net"
                elif cat in ("E-Posta", "Mesajlasma/Kuyruk"): cat_class = "bg-mail"

                banner = r.get('banner', '')
                if not banner and http_r.get('title'):
                    banner = http_r.get('title', '')[:80]
                elif r.get('service_detected'):
                    banner += f" <strong>[{r['service_detected']}]</strong>"

                code = http_r.get('status_code', '')
                if str(code) == "0": code = ""
                
                tech_waf = ""
                if http_r.get('tech'):
                    tech_waf += ", ".join(http_r['tech'])
                if http_r.get('waf'):
                    if tech_waf: tech_waf += "<br>"
                    tech_waf += f"<span class='waf-alert'>WAF: {http_r['waf']}</span>"

                html.append("<tr>")
                html.append(f"<td><strong style='color:#ffffff;'>{port}</strong></td>")
                html.append(f"<td>{svc}</td>")
                html.append(f"<td><span class='badge {cat_class}'>{cat}</span></td>")
                html.append(f"<td style='color:#00ff41; font-weight:bold;'>{r['state']}</td>")
                html.append(f"<td>{banner}</td>")
                html.append(f"<td>{code}</td>")
                html.append(f"<td>{tech_waf}</td>")
                html.append("</tr>")
                
            html.append("</table>")

            if self.http_results:
                html.append("<h2>HTTP/HTTPS Detayları</h2>")
                html.append("<table>")
                html.append("<tr><th>Port</th><th>Protokol</th><th>Kod</th><th>Sunucu</th><th>Başlık (Title)</th><th>Teknoloji</th><th>Yanıt Süresi</th></tr>")
                for port, result in sorted(self.http_results.items()):
                    if result.get('status_code', 0) == 0 and not result.get('server'):
                        continue
                        
                    svc = SERVICE_MAP.get(port, ("", ""))[0]
                    is_https = "HTTPS" in svc.upper() or port in [443, 8443, 9443, 4443]
                    proto = "HTTPS" if is_https else "HTTP"
                    
                    html.append("<tr>")
                    html.append(f"<td><strong style='color:#ffffff;'>{port}</strong></td>")
                    html.append(f"<td style='color:#44ddaa;'>{proto}</td>")
                    html.append(f"<td>{result.get('status_code', '')}</td>")
                    html.append(f"<td>{result.get('server', '')}</td>")
                    html.append(f"<td>{result.get('title', '')[:80]}</td>")
                    html.append(f"<td>{', '.join(result.get('tech', []))}</td>")
                    html.append(f"<td>{result.get('response_time', 0)} ms</td>")
                    html.append("</tr>")
                html.append("</table>")

            if self.dns_results:
                html.append("<h2>DNS Kayıtları</h2>")
                html.append("<table>")
                html.append("<tr><th style='width: 150px;'>Kayıt Tipi</th><th>Değer</th></tr>")
                for domain_name, r_dict in self.dns_results.items():
                    html.append(f"<tr><td colspan='2' style='background-color:#1a1a1a; color:#ff8888; font-weight:bold; text-align:center;'>Alan Adı: {domain_name}</td></tr>")
                    for rtype, records in r_dict.items():
                        if records:
                            html.append(f"<tr><td rowspan='{len(records)}' style='color:#ffcc44; font-weight:bold; border-right: 1px solid #222;'>{rtype}</td>")
                            html.append(f"<td>{records[0]}</td></tr>")
                            for rec in records[1:]:
                                html.append(f"<tr><td>{rec}</td></tr>")
                html.append("</table>")

            html.append("    </div>")
            html.append("</body>")
            html.append("</html>")

            with open(fp, "w", encoding="utf-8") as f:
                f.write("\n".join(html))

            self._print(f"Rapor HTML olarak kaydedildi: {fp}", "green")
            self._print(f"  Port: {open_count} | HTTP: {http_count} | DNS: {total_dns}", "cyan")
            
            try:
                import webbrowser
                webbrowser.open('file://' + os.path.realpath(fp))
            except Exception:
                pass

        except Exception as e:
            import traceback
            err_msg = traceback.format_exc()
            self._print(f"AKTARIM HATASI: {e}", "red")
            print(err_msg)

    
    
    

    def update_stats(self):
        
        self.stat_cards["open"].configure(text="0")
        self.stat_cards["http"].configure(text="0")
        self.stat_cards["https"].configure(text="0")
        self.stat_cards["waf"].configure(text="-")
        self.stat_cards["os"].configure(text="-")
        self.stat_cards["dns"].configure(text="-")
        self.stat_cards["service"].configure(text="0")
        self.stat_cards["tech"].configure(text="-")

    def update_time_counter(self):
        if self.current_operation != "bekliyor" and self.scan_start_time > 0:
            elapsed = time.time() - self.scan_start_time
            self.time_counter.configure(text=f"( {elapsed:.1f}s )")
            self.root.after(100, self.update_time_counter)

    def operation_started(self, op):
        self.current_operation = op
        self.stopped = False
        self.paused = False
        self.pause_event.set()
        self._probe_stop.clear()
        self._probe_pause.set()
        self.status_label.configure(text=f"[ {op.upper()} ]")
        self.btn_scan.configure(state=ctk.DISABLED)
        self.btn_pause.configure(state=ctk.NORMAL, text="⏸ DURAKLAT")
        self.btn_stop.configure(state=ctk.NORMAL)
        self.btn_dns.configure(state=ctk.NORMAL)
        self.btn_export.configure(state=ctk.DISABLED)

    def operation_finished(self):
        self.current_operation = "bekliyor"
        self.paused = False
        self.stopped = False
        self.status_label.configure(text="[ HAZIR ]")
        self.btn_scan.configure(state=ctk.NORMAL)
        self.btn_pause.configure(state=ctk.DISABLED, text="⏸ DURAKLAT")
        self.btn_stop.configure(state=ctk.DISABLED)
        if self.scan_results:
            self.btn_export.configure(state=ctk.NORMAL)
            if self.target_domain and not is_ip(self.target_domain):
                self.btn_dns.configure(state=ctk.NORMAL)

    def toggle_pause(self):
        if self.stopped:
            return
        if self.paused:
            self.paused = False
            self.pause_event.set()
            self.btn_pause.configure(text="⏸ DURAKLAT")
            self.status_label.configure(text=f"[ {self.current_operation.upper()} ]")
        else:
            self.paused = True
            self.pause_event.clear()
            self.btn_pause.configure(text="▶ DEVAM ET")
            self.status_label.configure(text="[ DURAKLATILDI ]")

    def stop_operation(self):
        self.stopped = True
        self.pause_event.set()
        self._probe_stop.set()
        self._probe_pause.set()
        self.status_label.configure(text="[ DURDURULDU ]")
        self._print("İşlem durduruldu!", "red")
        self.operation_finished()

    def set_thread_preset(self, v):
        self.thread_count.set(v)
        self.thread_label.configure(text=str(v))

    def on_thread_change(self, v):
        val = int(v)
        self.thread_count.set(val)
        self.thread_label.configure(text=str(val))

    def on_timeout_change(self, v):
        val = int(v)
        self.timeout_value.set(val)
        self.timeout_label.configure(text=f"{val}s")

    def toggle_fullscreen(self):
        c = self.root.attributes("-fullscreen")
        self.root.attributes("-fullscreen", not c)

    
    
    

    def _print_banner(self):
        banner_lines = [
            "╔══════════════════════════════════════════════════════════════════╗",
            "║                  ░▒▓█ CYBERANKA GÖZCÜ v1.0 █▓▒░                  ║",
            "║     Port Tarama · DNS Keşif · WAF Tespit · OS Fingerprinting     ║",
            "╚══════════════════════════════════════════════════════════════════╝"
        ]
        for line in banner_lines:
            self._print(line, "red")

    def _print(self, msg, tag="green"):
        try:
            self.terminal.insert(ctk.END, msg + "\n", tag)
            self.terminal.see(ctk.END)
            self.terminal.update_idletasks()
        except Exception:
            pass

    def read_targets_from_file(self, fp):
        
        targets = []
        try:
            with open(fp, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        t = re.sub(r'^https?://', '', line).split('/')[0].strip()
                        if t:
                            resolved = resolve_target(t)
                            if resolved:
                                targets.append(resolved)
                            else:
                                targets.append(t)
        except Exception as e:
            self._print(f"DOSYA HATASI: {e}", "red")
            return None
        return targets

    def clear_terminal(self):
        
        if self.current_operation != "bekliyor":
            self.stop_operation()
            time.sleep(0.3)

        self.terminal.delete("1.0", ctk.END)
        self.scan_results = []
        self.http_results = {}
        self.dns_results = {}
        self.os_result = {}
        self.scan_start_time = 0
        self.paused = False
        self.stopped = False
        self.pause_event.set()
        self._probe_stop.set()
        self._probe_pause.set()
        self.current_operation = "bekliyor"
        self.live_counter.configure(text="[ 0 açık port ]")
        self.time_counter.configure(text="( 0.0s )")
        self.progress.set(0)
        self.filter_count_label.configure(text="[ 0 / 0 ]")
        self.btn_pause.configure(state=ctk.DISABLED, text="⏸ DURAKLAT")
        self.btn_stop.configure(state=ctk.DISABLED)
        self.btn_dns.configure(state=ctk.DISABLED)
        self.btn_export.configure(state=ctk.DISABLED)
        self.target_label.configure(text="")
        self.update_stats()
        self.operation_finished()
        self._print_banner()
        self._print("root@gozcu:~$ Hedef alan adı veya IP girin ve ENTER'a basın", "green")
        self._print("root@gozcu:~$ Örnek: ornek.com | 8.8.8.8 | hedefler.txt", "dim")
        self._print("─" * 70, "dim")

    def run(self):
        self.root.after(400, self.do_countdown)
        self.root.update_idletasks()
        self.root.mainloop()


if __name__ == "__main__":
    app = CyberAnkaGozcu()
    app.run()