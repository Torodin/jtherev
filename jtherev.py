#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from urllib.request import urlopen
from html.parser import HTMLParser
from lxml import html
#from lxml import etree
#from bs4 import BeautifulSoup
from string import ascii_lowercase
from colorama import init, Fore, Back, Style

import argparse
import pyfiglet
import os, sys
import re
import json
import time
import getopt
import requests, dns.resolver, socket

init(convert=True) # override whether to convert ANSI codes in the output into win32 calls
init(autoreset=True) # reset sequences to turn off color changes at the end of every print

# static title, version, sign & desc
def header():
    title = pyfiglet.figlet_format("jtherev", font = "ogre" )
    vsign = pyfiglet.figlet_format("John The Revealer 1.4 by indevi0us", font = "digital" )
    print(title + vsign)
    print('Check an IP address through multiple DNS-based blacklists (DNSBL) and IP reputation services in real-time. '
	'In this way, you\'ll be able to detect if an IP is involved in malware incidents and spamming activities.\n')
    return

# whois.json
def jprint(obj):
    print('IP : ' + obj['data']['geo']['ip'] + '\n'
        + 'FQDN :', obj['data']['geo']['rdns'] + '\n'
        + 'Continent :', obj['data']['geo']['continent_name'] + '\n'
        + 'Country :', obj['data']['geo']['country_name'] + '\n'
        + 'ISP :', obj['data']['geo']['isp'] + '\n'
        + 'ASN :', obj['data']['geo']['asn'], '\n'
        + 'Postal Code:', obj['data']['geo']['postal_code'], '\n'
        + 'Region Name :', obj['data']['geo']['region_name'], '\n'
        + 'Time Zone:', obj['data']['geo']['timezone'])

# tracking and call to .json function to get geo ip location
def tracking():
    print(Fore.YELLOW + Style.BRIGHT + '\nProcess started' + Style.RESET_ALL + ': tracking the target...')
    time.sleep(2.5)
    print('[+] Get: receiving data about continent... Done' + '\n'
        + '[+] Get: receiving data about country... Done' + '\n'
        + '[+] Get: receiving data about ISP... Done' + '\n'
        + '[+] Get: receiving data about ASN... Done' + '\n'
        + '[+] Get: receiving data about postal code... Done' + '\n'
        + '[+] Get: receiving data about region name... Done' + '\n'
        + '[+] Get: receiving data about time zone... Done')
    time.sleep(1)
    #reversed_dns = socket.getfqdn(badip)
    urlgeo = 'https://tools.keycdn.com/geo.json?host='
    header = {'User-Agent': 'keycdn-tools:https://example.com'}
    geoip = requests.get(urlgeo + badip, headers=header).json()
    print('Fetching data received...\n')
    print('Fetching result {}'.format(geoip['status']))
    jprint(geoip)
    outputJson.update({'ip_data': geoip})
    return

# graphical function to keep track of the confidence of abuse
def confabuse():
    print(Fore.YELLOW + Style.BRIGHT + 'Process started' + Style.RESET_ALL + ': checking for confidence of abuse...')
    time.sleep(1)
    print('[+] Get: receiving data about confidence of abuse... Done\n' + 'Fetching data received...\n')
    time.sleep(1)
    return

# graphical function to keep track of the tor exit nodes check
def tprocess():
    print(Fore.YELLOW + Style.BRIGHT + '\nProcess started''' + Style.RESET_ALL + ': checking against TOR exit nodes DB...')
    time.sleep(1)
    return

# graphical function to keep track of the dnsbl check
def blprocess():
    print(Fore.YELLOW + Style.BRIGHT + '''\nProcess started''' + Style.RESET_ALL + ''': checking against multiple IP and DNS blacklists...''')
    time.sleep(1)
    return

# HTML parsing of www.abuseipdb.com to grep conf. abuse %
def abuseparse():
    #reversed_dns = socket.getfqdn(badip)
    geoip = requests.get('https://www.abuseipdb.com/check/' + badip)
    tree = html.fromstring(geoip.content)
    conf = tree.xpath('//*[@id="report-wrapper"]/div[1]/div[1]/div/p[1]/b[2]/text()')
    conf  = str(conf)
    print('Confidence of abuse is: ' + conf.replace('\'','').replace('[','').replace(']',''))
    outputJson.update({'confidence': conf})
    return

# input error handling
def reset():
    print(Fore.RED + Style.BRIGHT + "\n[!] Error: No IP address to check! Please, check your input.\n" + Style.RESET_ALL)
    return

bls = [
    "cbl.abuseat.org", "bl.spamcop.net", "pbl.spamhaus.org", "sbl.spamhaus.org",
    "rbl.interserver.net", "dnsbl.dronebl.org", "dnsbl.spfbl.net", "all.s5h.net",
    "spam.spamrats.com", "dnsbl-1.uceprotect.net", "spambot.bls.digibase.ca",
    "z.mailspike.net", "dnsbl-2.uceprotect.net", "dnsbl-3.uceprotect.net",
    "ips.backscatterer.org", "dyna.spamrats.com","b.barracudacentral.org",
    "bl.emailbasura.org", "spambot.bls.digibase.ca", "z.mailspike.net",
    "black.junkemailfilter.com", "dnsbl.sorbs.net", "web.dnsbl.sorbs.net",
    "ubl.unsubscore.com", "spam.dnsbl.sorbs.net", "dnsbl.justspam.org",
    "bl.blocklist.de", "bl.blocklist.it"
    ]

tor = ["tor.dan.me.uk"]

header()
outputJson = {'listed_in': []}

try:
    options, remainder = getopt.getopt(sys.argv[1:], 'o:i:', ['output='])
except getopt.GetoptError as err:
    print('ERROR:', err)
    sys.exit(1)

try:
    badip = None
    for opt, arg in options:
        if opt in ('-i', '--ip'):
            badip = arg

    if badip != None and re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", badip):
        tracking()
    else:
        reset()
        sys.exit(1)
except KeyError:
    reset()
    sys.exit(1)
except OSError:
    reset()
    sys.exit(1)
except re.error:
    reset()
    sys.exit(1)

BAD = 0
GOOD = 0

blprocess()

# blacklist check & results
for bl in bls:
    try:
        my_resolver = dns.resolver.Resolver()
        query = '.'.join(reversed(str(badip).split("."))) + "." + bl
        my_resolver.timeout = 5
        my_resolver.lifetime = 10
        answers = my_resolver.query(query, "A")
        answer_txt = my_resolver.query(query, "TXT")
        print (str(badip) + Fore.RED + Style.BRIGHT + ' is listed in ' + bl + Style.RESET_ALL
                        + ' (%s: %s)' % (answers[0], answer_txt[0]))
        outputJson['listed_in'].append({'list_name': bl, 'answer': '(%s: %s)' % (answers[0], answer_txt[0])})
        BAD = BAD + 1

# dns exceptions handling
    except dns.resolver.NXDOMAIN:
        print (str(badip) + ' is not listed in ' + bl)
        GOOD = GOOD + 1

    except dns.resolver.Timeout:
        print (Fore.RED + Style.BRIGHT + 'WARNING: Timeout querying ' + bl + Style.RESET_ALL)

    except dns.resolver.NoNameservers:
        print (Fore.RED + Style.BRIGHT + 'WARNING: No nameservers for ' + bl + Style.RESET_ALL)

    except dns.resolver.NoAnswer:
        print (Fore.RED + Style.BRIGHT + 'WARNING: No answer for ' + bl + Style.RESET_ALL)

print('\n{0} is on {1}/{2} blacklists.\n'.format(badip, BAD, (GOOD + BAD)))
confabuse()
abuseparse()
tprocess()

# tor check & results
for t in tor:
    try:
        my_resolver = dns.resolver.Resolver()
        query = '.'.join(reversed(str(badip).split("."))) + "." + t
        my_resolver.timeout = 5
        my_resolver.lifetime = 10
        answers = my_resolver.query(query, "A")
        answer_txt = my_resolver.query(query, "TXT")
        print(str(badip) + Fore.MAGENTA + Style.BRIGHT + ' is a TOR exit node\n' + Style.RESET_ALL
                        + ' (%s: %s)' % (answers[0], answer_txt[0]))
        outputJson.update({'tor_exit': True})
        BAD = BAD + 1

    except dns.resolver.NXDOMAIN:
        print(str(badip) + ' is not a TOR exit node\n')
        outputJson.update({'tor_exit': False})
        GOOD = GOOD + 1

for opt, arg in options:
    if opt in ('-o', '--output'):
        output_filepath = arg

        with open(output_filepath, "w") as f:
            jsonString = json.dumps(outputJson, indent=4)
            f.write(jsonString)
            f.close()