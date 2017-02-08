#!/usr/bin/env python

# My Post: https://www.linickx.com/3970/python-and-mac-addresses

# REF: http://craigbalfour.blogspot.co.uk/2008/10/normalizing-mac-address-string.html
# REF http://www.cyberciti.biz/faq/python-command-line-arguments-argv-example/

# Lib
import sys, getopt

# Function

def printhelp():
  print("Usage: %s -m MAC " % sys.argv[0])
  print("\n MAC can be in any of the following formats: ")
  print(" - 00:00:00:00:00:00")
  print(" - 00-00-00-00-00-00")
  print(" - 0000.0000.0000")
  print("\n Version %s" % version)

# Defaults

addr=""
version="1.01"

# CLI input
try:
    myopts, args = getopt.getopt(sys.argv[1:],"m:h")
except getopt.GetoptError as e:
    print (str(e))
    printhelp()
    sys.exit(2)

# o == option
# a == argument passed to the o

for o, a in myopts:
    if o == '-m':
        addr=a
    if o == '-h':
        printhelp()
        sys.exit()

if addr == "":
  addr = raw_input("Enter the MAC address: ")

# Determine which delimiter style out input is using
if "." in addr:
  delimiter = "."
elif ":" in addr:
  delimiter = ":"
elif "-" in addr:
  delimiter = "-"

# Eliminate the delimiter
m = addr.replace(delimiter, "")

m = m.lower()
u = m.upper()

# convert!
cisco= ".".join(["%s%s%s%s" % (m[i], m[i+1], m[i+2], m[i+3]) for i in range(0,12,4)])
eui= ":".join(["%s%s" % (m[i], m[i+1]) for i in range(0,12,2)])
ms= "-".join(["%s%s" % (u[i], u[i+1]) for i in range(0,12,2)])

print "Cisco: " + cisco
print "EUI: " + eui
print "Microsoft: " + ms