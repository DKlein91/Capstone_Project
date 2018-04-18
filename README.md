# Capstone_Project
This repository holds the code and documentation for our Windows Forensic Suite.

Documentation Windows Forensics Suite Individual Scripts

Prefetch Files - Analyze the most recently used programs' activation times
	Input: -f [filepath\filename]
		Example: -f "C:\Windows\Prefetch\WINWORD.EXE-A29E96D8"
	Output: Single File details for the file specified: Executable Name, Run Count, Last Eight Execution datetimes, List of Volume Informations (Volume Name, Creation Date, Serial Number), List of Directory Strings, List of Resources Loaded

	Input: -d [filepath]
		Example: -d "C:\Windows\Prefetch\"
	Output: Output of "-f" results for every Prefetch file inthe given directory

	Input: -e [filepath]
	Output: Output of all Prefetch Files, ordered by most recent last execution
AppCompatCache - Analyze the files with the most recently changed application compatibility status
	Input: -l "[output folder]\\"
		Example: -l "C:\Test\\"
	Output: Contents of the AppCompatCache: list of Date Modified and File Name

LNK Files


Windows Trash

Jump List

Shellbags 
	Output: Original Folder Name, Original Path to Folder, Last Time folder was opened, Username ran