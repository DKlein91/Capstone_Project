#!/usr/bin/env python
# ShimCacheParser.py
#
# Andrew Davis, andrew.davis@mandiant.com
# Copyright 2012 Mandiant
#
# Mandiant licenses this file to you under the Apache License, Version
# 2.0 (the "License"); you may not use this file except in compliance with the
# License.  You may obtain a copy of the License at:
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.  See the License for the specific language governing
# permissions and limitations under the License.
#
# Identifies and parses Application Compatibility Shim Cache entries for forensic data.

import sys
import os
import datetime
import struct
import zipfile
import argparse
import binascii
import pywin
import codecs
import io as sio
import xml.etree.cElementTree as et
from os import path
from csv import writer

# Values used by Windows 6.1 (Win7 and Server 2008 R2)
CACHE_MAGIC_NT6_1 = 0xbadc0fee
CACHE_HEADER_SIZE_NT6_1 = 0x80
NT6_1_ENTRY_SIZE32 = 0x20
NT6_1_ENTRY_SIZE64 = 0x30
CSRSS_FLAG = 0x2

# Values used by Windows 8
WIN8_STATS_SIZE = 0x80
WIN8_MAGIC = '00ts'

# Magic value used by Windows 8.1
WIN81_MAGIC = '10ts'

# Values used by Windows 10
WIN10_STATS_SIZE = 0x30
WIN10_CREATORS_STATS_SIZE = 0x34
WIN10_MAGIC = '10ts'
CACHE_HEADER_SIZE_NT6_4 = 0x30
CACHE_MAGIC_NT6_4 = 0x30

bad_entry_data = 'N/A'
g_verbose = False
g_usebom = False
output_header  = ["Last Modified", "Path"]

# Date Formats
DATE_MDY = "%m/%d/%y %H:%M:%S"
DATE_ISO = "%Y-%m-%d %H:%M:%S"
g_timeformat = DATE_ISO


def even_checker(item):
    if item % 2 == 1:
        return item + 1
    else:
        return item


def filetime_to_dt(ft):
    """Converts a Microsoft filetime number to a Python datetime. The new
    datetime object is time zone-naive but is equivalent to tzinfo=utc.

    >>> filetime_to_dt(116444736000000000)
    datetime.datetime(1970, 1, 1, 0, 0)

    >>> filetime_to_dt(128930364000)
    datetime.datetime(2009, 7, 25, 23, 0)
                      
    >>> filetime_to_dt(128930364000001000)
    datetime.datetime(2009, 7, 25, 23, 0, 0, 100)
    """
    # Get seconds and remainder in terms of Unix epoch
    # Convert to datetime object
    
    try: 
        if ft != 0: 
            return datetime.datetime.utcfromtimestamp((ft - 116444736000000000) / 10000000)
        else:
            return 116444736000000000
    except ValueError as e:
        return 0

# Return a unique list while preserving ordering.
def unique_list(li):

    ret_list = []
    for entry in li:
        if entry not in ret_list:
            ret_list.append(entry)
    return ret_list

def csv_it(rows, outfile=None):
    try:

        if not rows:
            print("[-] No data to write...")
            return

        if not outfile:
            for row in rows:
                print(" ".join(["%s"%x for x in row]))
        else:
            print("[+] Writing output to %s..."%outfile)
            try:
                f = open(outfile, 'wb')
                if g_usebom:
                    f.write(codecs.BOM_UTF8)
                csv_writer = writer(f, delimiter=',')
                csv_writer.writerows(rows)
                f.close()
            except IOError as err:
                print("[-] Error writing output file: %s" % str(err))
                return

    except UnicodeEncodeError as err:
        print("[-] Error writing output file: %s" % str(err))
        return
    
# Write the Log.
def write_it(rows, outfile=None):

    try:

        if not rows:
            print("[-] No data to write...")
            return

        if not outfile:
            for row in rows:
                print(" ".join(["%s"%x for x in row]))
        else:
            print("[+] Writing output to %s..."%outfile)
            try:
                directory = os.path.dirname(outfile)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                outfile = outfile + "AppCompatCacheResults.csv"
                f = open(outfile, 'w+')
                csv_writer = writer(f, delimiter=',')
                csv_writer.writerows(rows)
                f.close()
            except IOError as err:
                print("[-] Error writing output file: %s" % str(err))
                return

    except UnicodeEncodeError as err:
        print("[-] Error writing output file: %s" % str(err))
        return

#Found code to change from Base 10 to 16
def base16to10(num):
    num_rep={10:'a',
         11:'b',
         12:'c',
         13:'d',
         14:'e',
         15:'f',
         }
    new_num = 0
    num_exp = 0
    current=str(num)
    num_len = len(str(current))-1
    while num_len >= 0:
        if RepresentsInt(current[num_len]):
            new_num += (int(current[num_len], 16) * (16 ** (num_exp)))
        else: 
            #for x in range(0, num_len-1):
            for y in range(0, len(num_rep)):
                if(current[num_len] == num_rep[y]):
                    new_num += num_rep[y]
        num_len -= 1
        num_exp += 1
    return new_num

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

# Read the Shim Cache format, return a list of last modified dates/paths.
def read_cache(cachebin, quiet=False):

    if len(cachebin) < 16:
        # Data size less than minimum header size.
        return None

    try:
        # Get the format type
        magic = struct.unpack("<L", cachebin[0:4])[0]

        # Find the format that matches.
        # This is a Windows 7/2k8-R2 Shim Cache.
        if magic == CACHE_MAGIC_NT6_1:
            test_size = (struct.unpack("<H",
                         cachebin[CACHE_HEADER_SIZE_NT6_1:
                         CACHE_HEADER_SIZE_NT6_1 + 2])[0])
            test_max_size = (struct.unpack("<H", cachebin[CACHE_HEADER_SIZE_NT6_1+2:
                             CACHE_HEADER_SIZE_NT6_1 + 4])[0])

            # Shim Cache types can come in 32-bit or 64-bit formats.
            # We can determine this because 64-bit entries are serialized with
            # u_int64 pointers. This means that in a 64-bit entry, valid
            # UNICODE_STRING sizes are followed by a NULL DWORD. Check for this here.
            if (test_max_size-test_size == 2 and
                struct.unpack("<L", cachebin[CACHE_HEADER_SIZE_NT6_1+4:
                CACHE_HEADER_SIZE_NT6_1 + 8])[0] ) == 0:
                if not quiet:
                    print("[+] Found 64bit Windows 7/2k8-R2 Shim Cache data...")
                entry = CacheEntryNt6(False)
                return read_nt6_entries(cachebin, entry)
            else:
                if not quiet:
                    print("[+] Found 32bit Windows 7/2k8-R2 Shim Cache data...")
                entry = CacheEntryNt6(True)
                return read_nt6_entries(cachebin, entry)


        # Check the data set to see if it matches the Windows 8 format.
        elif len(cachebin) > WIN8_STATS_SIZE and cachebin[WIN8_STATS_SIZE:WIN8_STATS_SIZE+4] == WIN8_MAGIC:
            if not quiet:
                print("[+] Found Windows 8/2k12 Apphelp Cache data...")
            return read_win8_entries(cachebin, WIN8_MAGIC)

        # Windows 8.1 will use a different magic dword, check for it
        elif len(cachebin) > WIN8_STATS_SIZE and cachebin[WIN8_STATS_SIZE:WIN8_STATS_SIZE+4] == WIN81_MAGIC:
            if not quiet:
                print("[+] Found Windows 8.1 Apphelp Cache data...")
            return read_win8_entries(cachebin, WIN81_MAGIC)

        # Windows 10 will use a different magic dword, check for it
        elif len(cachebin) > WIN10_STATS_SIZE and cachebin[WIN10_STATS_SIZE:WIN10_STATS_SIZE+4] == WIN10_MAGIC:
            if not quiet:
                print("[+] Found Windows 10 Apphelp Cache data...")
            return read_win10_entries(cachebin, WIN10_MAGIC)

        # Windows 10 Creators Update will use a different STATS_SIZE, account for it
        elif len(cachebin) > WIN10_CREATORS_STATS_SIZE and (str(cachebin[WIN10_CREATORS_STATS_SIZE:WIN10_CREATORS_STATS_SIZE+4], 'utf-8') == (WIN10_MAGIC)):
            if not quiet:
                print("[+] Found Windows 10 Creators Update Apphelp Cache data...")
            return read_win10_entries(cachebin, WIN10_MAGIC, creators_update=True)

        else:
            print("[-] Got an unrecognized magic value of 0x%x... bailing" % magic)
            return None

    except (RuntimeError, TypeError, NameError) as err:
        print("[-] Error reading Shim Cache data: %s" % err)
        return None

# Read Windows 8/2k12/8.1 Apphelp Cache entry formats.
def read_win8_entries(bin_data, ver_magic):
    offset = 0
    entry_meta_len = 12
    entry_list = []

    # Skip past the stats in the header
    cache_data = bin_data[WIN8_STATS_SIZE:]

    data = sio.StringIO(cache_data)
    while data.tell() < len(cache_data):
        header = data.read(entry_meta_len)
        # Read in the entry metadata
        # Note: the crc32 hash is of the cache entry data
        magic, crc32_hash, entry_len = struct.unpack('<4sLL', header)

        # Check the magic tag
        if magic != ver_magic:
            raise Exception("Invalid version magic tag found: 0x%x" % struct.unpack("<L", magic)[0])

        entry_data = sio.StringIO(data.read(entry_len))

        # Read the path length
        path_len = struct.unpack('<H', entry_data.read(2))[0]
        if path_len == 0:
            path = 'None'
        else:
            path = entry_data.read(path_len).decode('utf-16le', 'replace').encode('utf-8')

        # Check for package data
        package_len = struct.unpack('<H', entry_data.read(2))[0]
        if package_len > 0:
            # Just skip past the package data if present (for now)
            entry_data.seek(package_len, 1)

        # Read the remaining entry data
        flags, unk_1, low_datetime, high_datetime, unk_2 = struct.unpack('<LLLLL', entry_data.read(20))

        # Check the flag set in CSRSS
        if (flags & CSRSS_FLAG):
            exec_flag = 'True'
        else:
            exec_flag = 'False'

        last_mod_date = convert_filetime(low_datetime, high_datetime)
        try:
            last_mod_date = datetime.datetime.fromtimestamp(last_mod_date)
        except ValueError:
            last_mod_date = bad_entry_data

        row = [last_mod_date, 'N/A', path, 'N/A', exec_flag]
        entry_list.append(row)

    return entry_list

# Read Windows 10 Apphelp Cache entry format
def read_win10_entries(bin_data, ver_magic, creators_update=False):

    offset = 0
    entry_meta_len = 12
    entry_list = []

    # Skip past the stats in the header
    if creators_update:
        cache_data = bin_data[WIN10_CREATORS_STATS_SIZE:]
    else:
        cache_data = bin_data[WIN10_STATS_SIZE:]
    #print(cache_data)
    #print((binascii.hexlify(cache_data))) #HEXLIFY A BYTES STRING?
    b_data = binascii.hexlify(cache_data)
    test_num = (hex(entry_meta_len))
    next_cache = 0
    count=0
   # data = sio.StringIO(cache_data.decode('utf-8', 'replace'))
    while b_data.find(b'31307473') != -1:
        count += 1
        print('cache No. ', count)
        #Set up the next cache entry's location; set up the current entry's cache, which will be independently manipulated.
        next_cache = b_data[8:].find(b'31307473')
        if next_cache is not -1:
            cache_data = b_data[:next_cache+8]
        elif next_cache == 1:
            cache_data = b_data

        #Create the header of 12 bytes, which houses the signature and entry size
        b_header=b_data[:entry_meta_len*2]

        # Read in the entry metadata
        # Note: the crc32 hash is of the cache entry data - usused here
        magic = binascii.unhexlify(b_header[:8]).decode('utf-8', 'ignore')
        crc32_hash = b_header[9:15]
        entry_len = b''
        for x in range(12,7,-1):
            entry_len += b_header[x*2:(x*2)+2]

        entry_len =  int(entry_len, 16)
        # Check the magic tag
        if magic != ver_magic:
            raise Exception("Invalid version magic tag found: 0x%x" % struct.unpack("<L", magic)[0])
        b_entry_data = cache_data[entry_meta_len*2: even_checker(entry_len)+((entry_meta_len+2)*2)]
        # Read the path length
        path_len = int(b_entry_data[:2], 16)
        if path_len == 0:
            path = 'None'
        else:
            path = binascii.unhexlify(cache_data[(entry_meta_len*2)+2:(entry_meta_len*2) + (path_len+2)*2]).decode('utf-8', 'strict')

        b_entry_data = cache_data[(entry_meta_len*2) + (path_len+2)*2:]
        # Read the remaining entry data
        b_datetime = b_entry_data[0:16]
        date_array = (b_datetime).decode('utf-8')
        filetime = ""
        for x in range(8,-1,-1):
            filetime += (date_array[x*2:x*2+2])

#        print( 'filetime: ', filetime)
        #last_mod_date = convert_filetime(low_datetime, high_datetime)
        try:
            temp_datetime = int(filetime, 16)
            test_datething = filetime_to_dt(temp_datetime)
            last_mod_date = test_datething
        except Exception:
            last_mod_date = bad_entry_data

        print(last_mod_date, path)
        row = [last_mod_date, path]
        entry_list.append(row)
        b_data = b_data[8:]
        b_data = b_data[next_cache:]
    return entry_list

# Read the Shim Cache Windows 7/2k8-R2 entry format,
# return a list of last modifed dates/paths.
def read_nt6_entries(bin_data, entry):

    try:
        entry_list = []
        exec_flag = ""
        entry_size = entry.size()
        num_entries = struct.unpack('<L', bin_data[4:8])[0]

        if num_entries == 0:
            return None

        # Walk each entry in the data structure.
        for offset in range(CACHE_HEADER_SIZE_NT6_1,
                             num_entries*entry_size + CACHE_HEADER_SIZE_NT6_1,
                             entry_size):

            entry.update(bin_data[offset:offset+entry_size])
            last_mod_date = convert_filetime(entry.dwLowDateTime,
                                             entry.dwHighDateTime)
            try:
                last_mod_date = last_mod_date.strftime(g_timeformat)
            except ValueError:
                last_mod_date = 'N/A'
            path = (bin_data[entry.Offset:entry.Offset +
                             entry.wLength].decode('utf-16le','replace').encode('utf-8'))
            path = path.replace("\\??\\", "")

            # Test to see if the file may have been executed.
            if (entry.FileFlags & CSRSS_FLAG):
                exec_flag = 'True'
            else:
                exec_flag = 'False'

            hit = [last_mod_date, 'N/A', path, 'N/A', exec_flag]

            if hit not in entry_list:
                entry_list.append(hit)
        return entry_list

    except (RuntimeError, ValueError, NameError) as err:
        print('[-] Error reading Shim Cache data: %s...' % err)
        return None

# Acquire the current system's Shim Cache data.
def get_local_data():

    tmp_list = []
    out_list = []
    global g_verbose

    try:
        import winreg as reg
    except ImportError:
        print("[-] \'winreg.py\' not found... Is this a Windows system?")
        sys.exit(1)

    hReg = reg.ConnectRegistry(None, reg.HKEY_LOCAL_MACHINE)
    hSystem = reg.OpenKey(hReg, r'SYSTEM')
    for i in range(1024):
        try:
            control_name = reg.EnumKey(hSystem, i)
            if 'controlset' in control_name.lower():
                hSessionMan = reg.OpenKey(hReg,
                                          'SYSTEM\\%s\\Control\\Session Manager' % control_name)
                for i in range(1024):
                    try:
                        subkey_name = reg.EnumKey(hSessionMan, i)
                        if ('appcompatibility' in subkey_name.lower()
                            or 'appcompatcache' in subkey_name.lower()):

                            appcompat_key = reg.OpenKey(hSessionMan, subkey_name)
                            bin_data = reg.QueryValueEx(appcompat_key,
                                                        'AppCompatCache')[0]
                            tmp_list = read_cache(bin_data)
                            if tmp_list:
                                path_name = 'SYSTEM\\%s\\Control\\Session Manager\\%s' % (control_name, subkey_name)
                                for row in tmp_list:
                                    if g_verbose:
                                        row.append(path_name)
                                    if row not in out_list:
                                        out_list.append(row)
                    except EnvironmentError:
                        break
        except EnvironmentError:
            break

    if len(out_list) == 0:
        return None
    else:
        #Add the header and return the list.
        if g_verbose:
            out_list.insert(0, output_header + ['Key Path'])
            return out_list
        else:
        #Only return unique entries.
            out_list = unique_list(out_list)
            out_list.insert(0, output_header)
            return out_list


# Do the work.
def main(argv=[]):

    global g_verbose
    global g_timeformat
    global g_usebom

    parser = argparse.ArgumentParser(description="Parses Application Compatibilty Shim Cache data")
    parser.add_argument("-l", "--local", action="store_true", help="Reads data from local system and outputs it into command line and a CSV file at the directory specified.")

    action1 = sys.argv[1]

    # Read the local Shim Cache data from the current system
    if action1 in ['-l', 'local']:
        print("[+] Dumping Shim Cache data from the current system...")
        entries = get_local_data()
        if not entries:
            print("[-] No Shim Cache entries found...")
        else:
            write_it(entries, sys.argv[2])

if __name__ == '__main__':
    main(sys.argv)
