// CppHDDReadTest.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <fstream>
#include <windows.h>
#include <tchar.h>
#include <strsafe.h>
#include <vector>
#include "CppHDDReadTest.h"
using namespace std;

void DisplayError(LPTSTR lpszFunction);

ifstream::pos_type size;
char * memblock;

int main()
{		//\\.\C:
	HANDLE hfile;
	ifstream inFile;
	ifstream::pos_type size;
	char* buffer = new char[84];
	hfile = CreateFile( (LPCTSTR)"D:\testfile1.img", GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL | FILE_FLAG_OVERLAPPED, NULL);
	ReadFile(hfile, buffer, 84, NULL, NULL);
	printf(buffer);

/*	ifstream file("D:\eula.1028.txt", ios::in | ios::binary | ios::ate);
	if (file.is_open())
	{
		long double size;
		size = file.tellg();
		memblock = new char[size];
		file.seekg(0, ios::beg);
		file.read(memblock, size);
		file.close();

		cout << "the complete file content is in memory";
		printf(memblock);
		delete[] memblock;
	}
	else cout << "Unable to open file";
*/
    return 0;
}

