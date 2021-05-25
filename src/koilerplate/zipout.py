#!/usr/bin/env python

"""
One of the frustrating features of Kaggle is that there is some, non-specified, limit
to the number of files that can be stored in the working folder and/or sub-folders
of the working folder.
The solution to this is to first save the output as files to the TEMP folder location
and then finally to zip up the folder's contents and move it to the working folder.
If you upload zip files to a dataset then kaggle conveniently unzips them when you
use them in the dataset or load them into a notebook.
This module makes this process easy to accomplish.
"""

from __future__ import annotations

__author__ = "Andrew Scholan"
__credits__ = []
__license__ = "MIT"
__version__ = "0.1.3"
__maintainer__ = "Andrew Scholan"
__email__ = "andrew.scholan@scholan.com"
__status__ = "Development"

import os
import shutil

from .folders import TEMP_ROOT, WORKING_ROOT


class ZipOut(object):
    """
    Useful container object for zip folder handling.
    """

    def __init__(self, folder_name: str, delete_existing: bool = False) -> None:
        """
        Creates a ZipOut object that keeps track of the folders associated with a
        folder used for zipping data to copy to the working folder.

        Args:
            folder_name: The folder name to use for saving files into.
            delete_existing: If this flag is set to True then the existing contents
                of the folder in the TEMP folder will be deleted and any zip file
                in the WORKING folder is deleted. (default is False).
        """
        self._folder_path = os.path.join(TEMP_ROOT, folder_name)
        self._zip_file_base = os.path.join(WORKING_ROOT, folder_name)
        if os.path.exists(self.folder_path) and delete_existing:
            shutil.rmtree(self.folder_path)
        if os.path.exists(self.zip_file_path):
            os.remove(self.zip_file_path)
        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path)

    @property
    def folder_path(self) -> str:
        """
        The folder path to be used for storing files/folders into.
        """
        return self._folder_path

    @property
    def zip_file_path(self) -> str:
        """
        Zip file path including the file name.
        """
        return f"{self._zip_file_base}.zip"

    def make_zip_file(self) -> str:
        """
        This makes the zip file from the temporary folder contents. It generates
        a zip file in the WORKING folder with the same base name as the folder
        name used when initialising the ZipOut object.

        Returns:
            The path and filename of the zip file created.
        """
        shutil.make_archive(
            base_name=self._zip_file_base, format="zip", root_dir=self.folder_path
        )
        return self.zip_file_path
