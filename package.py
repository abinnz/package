# -*- coding: utf-8 -*-
import json
import os
import sys
import shutil
from datetime import datetime
import re
import win32api

# 加载json
def loadProjectData(baseDir,fileName = 'project_data.json'):
    projectData = {};
    with open(os.path.join(baseDir,fileName),'r') as jsonFile:
        projectData = json.load(jsonFile);
        return projectData;

def createTargetDir(baseDir,projectData):
    dirName = projectData['targetName'];
    if dirName == '':
        raise Exception('TargetName cann\'t be empty.');
    # baseDir脚本运行目录
    path = '';
    # 默认路径
    if projectData['targetDir'] == '':
        path = os.path.join(baseDir,dirName);
    # 桌面路径
    elif projectData['targetDir'] == '%Desktop%':
        path = os.path.join(os.path.expanduser("~"),'Desktop',dirName);
    # 指定路径
    else:
        path = os.path.join(projectData['targetDir'],dirName);

    # 存在删除
    if os.path.isdir(path):
        print('Remove an existing directory,path: ' + path);
        os.removedirs(path);
    # 创建目录
    os.makedirs(path);
    print('Create target directory: ' + path);
    return path;

def copyDirAndFile(baseSourcePath,sourcePath,targetPath,packageTask):
    if packageTask is None:
        return;
    for item in os.listdir(sourcePath):
        path = os.path.join(sourcePath,item);
        # 文件夹
        if os.path.isdir(path):
            # 非排除的文件夹
            if not isExcludeDir(baseSourcePath,path,packageTask['excludeDir']):
                createPath = os.path.join(targetPath,item);
                os.mkdir(createPath);
                print('Create directory: ' + createPath);
                # 递归
                copyDirAndFile(baseSourcePath,path,createPath,packageTask);
        # 文件
        else:
            if not isExcludeFile(baseSourcePath,path,packageTask['excludeFile'],packageTask['excludeSuffix']):
                # 复制文件
                shutil.copy(path,targetPath);
                print('Copy file: ' + path);

def createNewFile(targetPath,projectData,newFile):
    for item in newFile:
        fileName = getFormatName(projectData,item);
        path = os.path.join(targetPath,fileName);
        file = open(path,'w');
        file.close();
        print('Create File: ' + path);

def isExcludeFile(basePath,path,excludeFile,excludeSuffix):
    lt = excludeFile + excludeSuffix;
    # 排除文件
    for item in lt:
        if '\\' in item:
            value = os.path.join(basePath,item).replace('\\','\\\\');
            value = value.replace('*.','[^\\\\]*\.');
            if re.match(value + "$",path):
                return True;
        else:
            value = item.replace('*.','[^\\\\]*\.');
            if re.match('.*' + value + "$",path):
                return True; 
    return False;

def isExcludeDir(basePath,path,excludeDir):
    result = [];
    for item in excludeDir:
        value = os.path.join(basePath,item).replace('\\','\\\\');
        if re.match(value + "$",path):
            result.append(True);
        else:
            result.append(False);
    # 查看是否有排除的目录
    if True in result:
        return True;
    else:
        return False;

def getFileVersion(binPath):
    info = win32api.GetFileVersionInfo(binPath,os.sep);
    ms = info['FileVersionMS'];
    ls = info['FileVersionLS'];
    version = '%d.%d.%d.%d' % (win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls));
    return version;

def initProjectData(projectData):
    # 命令行参数读取
    if len(sys.argv) < 3:
        print('You can assign source directory through command line arguments,\nexample: -s "path"');
    # 三个参数
    if len(sys.argv) == 3 and sys.argv[1] == '-s':
        if os.path.exists(sys.argv[2]):
            projectData['sourceDir'] = sys.argv[2];
    # 判读source是否存在
    if not os.path.isdir(projectData['sourceDir']):
        raise Exception('SourceDir: ' + projectData['sourceDir'] + ' isn\'t exist.');
    # 获取projectName
    if projectData['projectName'] == '':
        projectData['projectName'] = re.match('(.*)[\\\\/](.*)',projectData['sourceDir']).group(2);
    print('ProjectName: ' + projectData['projectName']);
    # 获取releaseDate
    if projectData['releaseDate'] == '':
        projectData['releaseDate'] = datetime.now().strftime(projectData['dateFormat']);
    print('ReleaseDate: ' + projectData['releaseDate']);
    # 获取projectVersion
    if projectData['projectVersion'] == '':
        suffix = ".dll"
        binPath = os.path.join(projectData['sourceDir'],projectData['sourceBin'],projectData['projectName'] + suffix);
        if os.path.exists(binPath):
            projectData['projectVersion'] = getFileVersion(binPath);
        else:
            raise Exception('Path: ' + binPath + ' isn\'t exist.');
    print('ProjectVersion: ' + projectData['projectVersion']);
    # 获取targetName
    if re.match('.*\${.*}.*',projectData['targetName']):
        projectData['targetName'] = getFormatName(projectData,projectData['targetName']);
    print('TargetName: ' + projectData['targetName']);

def getFormatName(projectData,fmt):
    lt = re.split('\${',fmt);
    name = '';
    for item in lt:
        if re.match('.*}.*',item):
            l = re.split('}',item);
            if l[0] not in projectData.keys():
                raise Exception('ProjectData[' + l[0] + '] isn\'t exist.');
            m = map(lambda t:projectData[t[1]] if t[0]==0 else t[1],enumerate(l));
            l = list(m);
            name += l[0] + l[1];
        else:
            name += item;
    return name;     

if __name__ == '__main__':
    try:
        print('Start load project_data.json...');
        # 当前运行目录
        baseDir = os.path.dirname(sys.argv[0]);
        # 加载json
        projectData = loadProjectData(baseDir);
        # 数据初始化
        initProjectData(projectData);
        # 创建target目录，并返回目录路径
        targetPath = createTargetDir(baseDir,projectData);
        # 复制目录以及文件
        copyDirAndFile(projectData['sourceDir'],projectData['sourceDir'],targetPath,projectData['packageTask']);
        # 创建新文件
        createNewFile(targetPath,projectData,projectData['packageTask']['newFile']);
        print('Complete package project...');
    except Exception as ex:
        print(ex);
        sys.exit(-1);