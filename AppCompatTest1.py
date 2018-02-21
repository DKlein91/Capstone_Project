import sys
from xml.etree.ElementTree import tostring
import struct
import zipfile
import argparse
import binascii
import datetime
import codecs
import io as sio
import winreg
import xml.etree.cElementTree as et
from os import path
from csv import writer

# Values used by Windows 5.2 and 6.0 (Server 2003 through Vista/Server 2008)
CACHE_MAGIC_NT5_2 = 0xbadc0ffe
CACHE_HEADER_SIZE_NT5_2 = 0x8
NT5_2_ENTRY_SIZE32 = 0x18
NT5_2_ENTRY_SIZE64 = 0x20

# Values used by Windows 6.1 (Win7 and Server 2008 R2)
CACHE_MAGIC_NT6_1 = 0xbadc0fee
CACHE_HEADER_SIZE_NT6_1 = 0x80
NT6_1_ENTRY_SIZE32 = 0x20
NT6_1_ENTRY_SIZE64 = 0x30
CSRSS_FLAG = 0x2

# Values used by Windows 5.1 (WinXP 32-bit)
WINXP_MAGIC32 = 0xdeadbeef
WINXP_HEADER_SIZE32 = 0x190
WINXP_ENTRY_SIZE32 = 0x228
MAX_PATH = 520

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
output_header  = ["Last Modified", "Last Update", "Path", "File Size", "Exec Flag"]

# Date Formats
DATE_MDY = "%m/%d/%y %H:%M:%S"
DATE_ISO = "%Y-%m-%d %H:%M:%S"
g_timeformat = DATE_ISO

def read_win10_entries(bin_data, ver_magic, creators_update=False):

    offset = 0
    entry_meta_len = 12
    entry_list = []

    print(bin_data)

    b_data = binascii.hexlify(bin_data)
    data = sio.StringIO(bin_data.decode('utf-8', 'ignore'))
    print(data.read(-1))
    while data.tell() < len(bin_data):
        header = data.read(entry_meta_len)
        print(header)
        # Read in the entry metadata
        # Note: the crc32 hash is of the cache entry data
        #magic, entry_len = struct.unpack('<8s4L', header)
        magic = header[:4]
        entry_len = 8
        # Check the magic tag
        if magic != ver_magic:
            raise Exception("Invalid version magic tag found: 0x%x" % struct.unpack("<L", magic)[0])
        print(data.read(-1))
        entry_data = sio.StringIO(data.read(entry_len))
        # Read the path length
        path_len = struct.unpack('<H', entry_data.read(2))[0]
        print(path_len)
        if path_len == 0:
            path = 'None'
        else:
            path = entry_data.read(path_len)#.decode('utf-8', 'ignore')

        # Read the remaining entry data
        low_datetime, high_datetime = struct.unpack('<LL', entry_data.read(8))

        last_mod_date = convert_filetime(low_datetime, high_datetime)
        try:
            last_mod_date = last_mod_date.strftime(g_timeformat)
        except ValueError:
            last_mod_date = bad_entry_data

        # Skip the unrecognized Microsoft App entry format for now
        if last_mod_date == bad_entry_data:
            continue

        row = [last_mod_date, 'N/A', path, 'N/A', 'N/A']
        entry_list.append(row)

    return entry_list

# Read the Shim Cache format, return a list of last modified dates/paths.
def read_cache(cachebin, quiet=False):

    if len(cachebin) < 16:
        # Data size less than minimum header size.
        return None

    try:
        # Get the format type
        magic = struct.unpack("<L", cachebin[0:4])[0]

        # This is a Windows 2k3/Vista/2k8 Shim Cache format,
        if magic == CACHE_MAGIC_NT5_2:

            # Shim Cache types can come in 32-bit or 64-bit formats. We can
            # determine this because 64-bit entries are serialized with u_int64
            # pointers. This means that in a 64-bit entry, valid UNICODE_STRING
            # sizes are followed by a NULL DWORD. Check for this here.
            test_size = struct.unpack("<H", cachebin[8:10])[0]
            test_max_size = struct.unpack("<H", cachebin[10:12])[0]
            if (test_max_size-test_size == 2 and
                struct.unpack("<L", cachebin[12:16])[0] ) == 0:
                if not quiet:
                    print("[+] Found 64bit Windows 2k3/Vista/2k8 Shim Cache data...")
                entry = CacheEntryNt5(False)
                return read_nt5_entries(cachebin, entry)

            # Otherwise it's 32-bit data.
            else:
                if not quiet:
                    print("[+] Found 32bit Windows 2k3/Vista/2k8 Shim Cache data...")
                entry = CacheEntryNt5(True)
                return read_nt5_entries(cachebin, entry)

        # This is a Windows 7/2k8-R2 Shim Cache.
        elif magic == CACHE_MAGIC_NT6_1:
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

        # This is WinXP cache data
        elif magic == WINXP_MAGIC32:
            if not quiet:
                print("[+] Found 32bit Windows XP Shim Cache data...")
            return read_winxp_entries(cachebin)

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
        elif len(cachebin) > WIN10_CREATORS_STATS_SIZE and cachebin[0:4] == bytes(WIN10_MAGIC, 'utf-8'):
            if not quiet:
                print("[+] Found Windows 10 Creators Update Apphelp Cache data...")
            return read_win10_entries(cachebin, WIN10_MAGIC, creators_update=True)

        else:
            print("[-] Got an unrecognized magic value of 0x%x... bailing" % magic)
            return None

    except (RuntimeError, TypeError, NameError) as err:
        print("[-] Error reading Shim Cache data: %s" % err)
        return None

# Acquire the current system's Shim Cache data.
def get_local_data():

    tmp_list = []
    out_list = []
    global g_verbose

    try:
        import winreg as reg
    except ImportError:
        print ("[-] \'winreg.py\' not found... Is this a Windows system?")
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
                            bin_data = reg.QueryValueEx(appcompat_key,'CacheMainSdb')[0]
                            tmp_list = read_cache(bin_data)
                            if tmp_list:
                                path_name = 'SYSTEM\\%s\\Control\\Session Manager\\%s' % (control_name, subkey_name)
                                for row in tmp_list:
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

def main(argv=[]):
    get_local_data()


if __name__ == '__main__':
    main(sys.argv)