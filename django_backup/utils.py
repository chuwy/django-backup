#!/usr/bin/env python

# -*- coding: utf-8 -*-

__author__ = 'Anton Parkhomenko'

from datetime import datetime
import os
import zipfile


def import_class(path):
    components = path.split('.')
    mod = __import__('.'.join(components[:-1]), fromlist=[''])
    klass = getattr(mod, components[-1])
    return klass


def zipdir(dir_path=None, zip_file_path=None, include_dir=True):
    """Create a zip archive from a directory.

    Keyword arguments:

    dir_path -- string path to the directory to archive. This is the only
    required argument. It can be absolute or relative, but only one or zero
    leading directories will be included in the zip archive.

    zip_file_path -- string path to the output zip file. This can be an absolute
    or relative path. If the zip file already exists, it will be updated. If
    not, it will be created. If you want to replace it from scratch, delete it
    prior to calling this function. (default is computed as dirPath + ".zip")

    include_dir -- boolean indicating whether the top level directory should
    be included in the archive or omitted. (default True)
    """
    if not zip_file_path:
        zip_file_path = dir_path + ".zip"
    if not os.path.isdir(dir_path):
        raise OSError("dir_path argument must point to a directory. "
                      "'%s' does not." % dir_path)
    parentDir, dirToZip = os.path.split(dir_path)
    #Little nested function to prepare the proper archive path
    def trimPath(path):
        archivePath = path.replace(parentDir, "", 1)
        if parentDir:
            archivePath = archivePath.replace(os.path.sep, "", 1)
        if not include_dir:
            archivePath = archivePath.replace(dirToZip + os.path.sep, "", 1)
        return os.path.normcase(archivePath)

    outFile = zipfile.ZipFile(zip_file_path, "w",
                              compression=zipfile.ZIP_DEFLATED)
    for (archiveDirPath, dirNames, fileNames) in os.walk(dir_path):
        for fileName in fileNames:
            filePath = os.path.join(archiveDirPath, fileName)
            outFile.write(filePath, trimPath(filePath))
            #Make sure we get empty directories as well
        if not fileNames and not dirNames:
            zipInfo = zipfile.ZipInfo(trimPath(archiveDirPath) + "/")
            #some web sites suggest doing
            #zipInfo.external_attr = 16
            #or
            #zipInfo.external_attr = 48
            #Here to allow for inserting an empty directory.  Still TBD/TODO.
            outFile.writestr(zipInfo, "")
    outFile.close()


def validate_backup_file(f):
    try:
        datetime.strptime(f, '%d-%m-%Y_%H-%M.zip')
        return True
    except ValueError:
        return False
