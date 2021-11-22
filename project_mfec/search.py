import re
import collections
import time
import csv
import requests
from SelectFile import fileNames,path
import socket
hostnames = {}
warnPort = {}
sWarnPort = {}
catOrNex = {}

def netConnection():
    try:
        socket.create_connection(('Google.com',80))
        return True
    except OSError:
        return False

def searchLocal(newMac):
    match = ""
    with open("macaddress.io-db.csv","r", encoding="utf-8",newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if(newMac == row[0]):
                match = row[2]
    return match


def searchAll():
    # Function for switch type Catalyst and Nexus to search Mac address and vendor
    dict = {}
    sdict = {}
    try:

        for filepath,filename in enumerate(fileNames):
            with open(path[filepath] + "/" + filename, "r", encoding="utf-8") as fo:
                with open("macaddress.io-db.csv", "a", encoding="utf-8",newline="") as fwc:
                    fws = open("conv_file/sort_file" + "/" + "sort" + filename, "w+", encoding="utf-8")
                    fw = open("conv_file/unsort_file" + "/" + "unsort" + filename, "w+", encoding="utf-8")
                    new = csv.writer(fwc)
                    filedata = fo.readlines()
                    mac_ind = None
                    nexus = False
                    nex = "Catalyst Switch"
                    for ind,line in enumerate(filedata):
                        if line.strip() == "Cisco Nexus Operating System (NX-OS) Software":
                            nexus = True
                            nex = "Nexus Switch"
                    catOrNex.setdefault(filename,nex)
                    if nexus == True:
                        for ind,line in enumerate(filedata):
                            if line.strip().split("#")[-1] == " show mac address-table":    # Find Hostname and Start search line
                                hostname = line.strip().split("#")[0]
                                hostnames.setdefault(filename,hostname)
                                mac_ind = ind
                            if mac_ind != None and ind > mac_ind + 6:   # Stop search line
                                if line.split("#")[0] == hostname :
                                    break
                                else:
                                    line = line[1:-1].strip()
                                    newline = list(map(lambda x: x.strip(),line.split(" ")))
                                    dict.setdefault(newline[-1],{}).setdefault(newline[5],[]).append(newline[0])
                                    if "po" in newline[-1].lower():  # Check if in that line have po and add to dict
                                        sdict.setdefault(newline[-1],{}).setdefault(newline[5],[]).append(newline[0])
                    elif nexus == False:
                        for ind,line in enumerate(filedata):
                            if line.strip() == "Mac Address Table":      # Start search line
                                mac_ind = ind
                            if line.strip().split("#")[-1].strip() == "show version":   # Find Hostname
                                hostname = line.strip().split("#")[0]
                                hostnames.setdefault(filename,hostname)
            
                            if mac_ind != None and ind > mac_ind + 4:   # Stop search line
                                if line.split(":")[0] == "Total Mac Addresses for this criterion" : 
                                    break
                                else:
                                    line = list(map(lambda x: x.strip(),line.strip().split("    ")))
                                    dict.setdefault(line[3],{}).setdefault(line[1],[]).append(line[0])  # Add line that got split to dict and append vlan
                                    if "po" in line[3].lower():  # Check if in that line have po and add to dict
                                        sdict.setdefault(line[3],{}).setdefault(line[1],[]).append(line[0])
                        
                    #   Remove Port po
                    for key in sdict.keys():
                        dict.pop(key)
                        
                    print("File:" + filename + "\n")
                    # Start write line to text
                    fw.writelines("Vlan" + "\t" + "Mac-Address" + "\t" + "Port" + "\t" + "Vendor" +"\n")
                    for key,inkey in dict.items():
                        if len(inkey.keys()) > 1 and key != "CPU":  # Check mac address that more than 1 and Port isn't CPU
                            print("This port ",key,"is suspicious.\n")
                            warnPort.setdefault(filename,[]).append(key)    # Append port that may be suspicious before sort
                            for mac,vlan in inkey.items():
                                newMac = "{:2}:{:2}:{:2}".format(mac[0:2],mac[2:4],mac[5:7]).upper()
                                match = searchLocal(newMac)
                                if match != "":
                                    print(vlan[0], mac, key, match + "\n")
                                    fw.writelines(vlan[0] + "\t" + mac + "\t" + key + "\t" + match +"\n")
                                else: #เช็ค condition api connect not connect!
                                    if netConnection() == True:
                                        vendor = requests.get('https://api.macvendors.com/' + mac).text
                                        if vendor == '{"errors":{"detail":"Not Found"}}':
                                            print(vlan[0], mac, key, "Not Found" + "\n")
                                            fw.writelines(vlan[0] + "\t" + mac + "\t" + key + "\t" + "Not found" +"\n")
                                            time.sleep(1)
                                        elif vendor == '{"errors":{"detail":"Too Many Requests","message":"Please slow down your requests or upgrade your plan at https://macvendors.com"}}':
                                                
                                            print(vlan[0], mac, key, "Error:Not Found" + "\n")
                                            fw.writelines(vlan[0] + "\t" + mac + "\t" + key + "\t" + "Not found" +"\n")
                                            time.sleep(1)
                                        else:
                                            print(vlan[0], mac, key, vendor + "\n")
                                            fw.writelines(vlan[0] + "\t" + mac + "\t" + key + "\t" + vendor +"\n")
                                            new.writerow([newMac,0,vendor])
                                            time.sleep(1)
                                    else:
                                        print(vlan[0], mac, key, "Not Found" + "\n")
                                        fw.writelines(vlan[0] + "\t" + mac + "\t" + key + "\t" + "Not Found" +"\n")
                    
                    fw.writelines("End:")
                    fw.close()
                    fws.close()
                    dict.clear()
                    sdict.clear()
                    sort_mac(filename) # Remove port that vendor is cisco 
        return (hostnames ,warnPort ,sWarnPort,catOrNex)
                        
                        
    except Exception as e:
        print(e) 



def sort_mac(filename):
    # Function for sort file to remove port that have vendor cisco 
    try:
        # print("Start sorting file!")
        ndict = {}
        nsdict = {}
        with open("conv_file/unsort_file" + "/" + "unsort" + filename, "r", encoding="utf-8") as fo:
            fws = open("conv_file/sort_file" + "/" + "sort" + filename, "w+", encoding="utf-8")
            filedata = fo.readlines()
            mac_ind = None
            for ind,line in enumerate(filedata):
                if line.strip() == "Vlan	Mac-Address	Port	Vendor":    # Start search line
                    mac_ind = ind
                if mac_ind != None and ind > mac_ind:   # Stop search line
                    if line.split(":")[0] == "End" :
                        break
                    else:
                        line = list(map(lambda x: x.strip(),line.strip().split("\t")))
                        ndict.setdefault(line[2],{}).setdefault(line[1],{}).setdefault(line[0],line[3])
                        if "cisco" in line[3].lower():  # Check if in that line have cisco and add to dict
                            nsdict.setdefault(line[2],{}).setdefault(line[1],{}).setdefault(line[0],line[3])
                        elif type(line[3].lower()) == None:
                            #Get hostname
                            hostname = hostnames.get(filename)
                            # Start write line to text
                            fws.writelines("Hostname:" + "\t" + hostname + "\n")
                            fws.writelines("This File don't have any port that look suspicious" +"\n")
                        
                            fws.close()
                            ndict.clear()
                            nsdict.clear()
                            break
            #   Remove Port that have cisco
            for key in nsdict.keys():
                ndict.pop(key)
            #Get hostname
            hostname = hostnames.get(filename)
            # Start write line to text
            fws.writelines("Hostname:" + "\t\t" + hostname + "\n")
            fws.writelines("Vlan" + "\t\t" + "Mac-Address" + "\t\t" + "Port" + "\t\t" + "Vendor" +"\n")
            print("Start sorting file! " + filename + "\n")
            for key,inkey in ndict.items():
                print("This port ",key,"is suspicious.\n")
                sWarnPort.setdefault(filename,[]).append(key)   # Append port that look suspicious after sort
                for mac,dvlan in inkey.items():
                    for vlan,vendor in dvlan.items():
                        fws.writelines(vlan + "\t\t" + mac + "\t\t" + key + "\t\t" + vendor +"\n")
                    # print(vlan[0], mac, key, vendor + "\n")
                    
            fws.close()
            ndict.clear()
            nsdict.clear()
        print("Finish sorting file!\n")
    except Exception as e:
        print(e)
