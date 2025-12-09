#!/usr/bin/env python3
import argparse
import socket
import sys
from urllib.parse import urlparse
import ipaddress

def extract_domain(url):
    """Извлекает домен из URL или чистой строки."""
    url = url.strip()
    if not url or url.startswith('#'):
        return None
    # Обрабатываем как домен, так и URL
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    parsed = urlparse(url)
    domain = parsed.netloc
    if ':' in domain:
        domain = domain.split(':')[0]
    return domain if domain else None

def resolve_domain(domain):
    """Получает все IPv4 и IPv6 адреса домена."""
    ips = set()
    # Попробуем A (IPv4) и AAAA (IPv6)
    for family in (socket.AF_INET, socket.AF_INET6):
        try:
            results = socket.getaddrinfo(domain, None, family, socket.SOCK_STREAM)
            for res in results:
                ip = res[4][0]
                # Убираем IPv6 в полной форме (много ::), но socket и так даёт нормальный формат
                try:
                    # Валидация и нормализация через ipaddress
                    normalized = str(ipaddress.ip_address(ip))
                    ips.add(normalized)
                except ValueError:
                    continue
        except Exception:
            continue
    return ips

def main():
    parser = argparse.ArgumentParser(
        description="Преобразует список URL/доменов в список IP-адресов (IPv4 + IPv6), по одному на строку."
    )
    parser.add_argument("input_file", help="Файл со списком URL или доменов (по одному на строку)")
    parser.add_argument("-o", "--output", default="ipset-myunblock.txt", help="Выходной файл")
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ Файл не найден: {args.input_file}", file=sys.stderr)
        sys.exit(1)

    all_ips = set()
    total_domains = 0

    for line in lines:
        domain = extract_domain(line)
        if not domain:
            continue
        total_domains += 1
        ips = resolve_domain(domain)
        all_ips.update(ips)

    # Сортировка: сначала IPv4, потом IPv6, внутри — лексикографически (корректно для IP)
    ipv4_list = []
    ipv6_list = []
    for ip in all_ips:
        try:
            if isinstance(ipaddress.ip_address(ip), ipaddress.IPv4Address):
                ipv4_list.append(ip)
            else:
                ipv6_list.append(ip)
        except Exception:
            continue

    ipv4_list.sort(key=lambda ip: [int(x) for x in ip.split('.')])
    ipv6_list.sort()

    final_list = ipv4_list + ipv6_list

    with open(args.output, 'w') as f:
        for ip in final_list:
            f.write(ip + '\n')

    print(f"✅ Обработано: {total_domains} доменов → найдено {len(final_list)} уникальных IP (IPv4+IPv6) → сохранено в {args.output}")

if __name__ == "__main__":
    main()