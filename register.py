# -*- coding: utf-8 -*-
import sys
import os

LF = '\n';
UTF8 = "utf-8";

def createRegisterFile(regFilePath, startFilePath):
    file = open(regFilePath, 'w', encoding = UTF8);
    file.writelines('Windows Registry Editor Version 5.00' + LF);
    file.writelines(LF);
    file.writelines('[HKEY_CLASSES_ROOT\Directory\shell\package]' + LF);
    file.writelines('@="Package Project"' + LF);
    file.writelines(LF);
    file.writelines('[HKEY_CLASSES_ROOT\Directory\shell\package\command]' + LF);
    file.writelines('@="\\"' + startFilePath.replace('\\', '\\\\') + '\\" \\"%1\\""');
    file.close();

def createStartFile(startFilePath, exeFilePath):
    file = open(startFilePath, 'w', encoding = UTF8);
    file.writelines('@echo off' + LF);
    file.writelines('"' + exeFilePath + '"' + ' "-s" %1' + LF);
    file.writelines('pause');
    file.close();

def removeFileSavety(filePath):
    if os.path.exists(filePath):
        os.remove(filePath);

if __name__ == '__main__':
    try:
        baseDir = os.path.dirname(sys.argv[0]);
        suffix = '.py'
        if sys.argv[0].rfind('.exe') != -1:
            suffix = '.exe'
        exeFilePath = os.path.join(baseDir, 'package' + suffix);
        regFilePath = os.path.join(baseDir, 'package.reg');
        startFilePath = os.path.join(baseDir, 'start.bat');
        removeFileSavety(startFilePath);
        createStartFile(startFilePath, exeFilePath);
        print('Create file successful: ' + startFilePath);
        removeFileSavety(regFilePath);
        createRegisterFile(regFilePath, startFilePath);
        print('Create file successful: ' + regFilePath);
        print('Please register package.reg file firstly!');
    except Exception as ex:
        print(ex);
    finally:
        input();