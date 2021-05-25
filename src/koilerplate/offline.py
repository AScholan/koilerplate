#!/usr/bin/env python

"""
Code competitions often require that notebooks be submitted and are run without
internet access enabled. This is fine when the base kaggle notebook contains all
the libraries that you want to use. However is problematic if you want to use a
python library that's not in the base notebook.
Most of these competitions allow you to load libraries from kaggle datasets. This
module does the heavy lifting in preparing a kaggle dataset that can be later used
to offline load libraries into your competition notebook.

Examples:
    To prepare a kaggle dataset that can be used to offline pip-install a set of python
    packages, add this to a kaggle notebook that's configured for internet access:

        >>> from koilerplate import offline_pip_prepare
        >>>
        >>> PACKAGES = [
        >>>    "torch==1.7.1+cu110",
        >>>    "torchvision==0.8.2+cu110",
        >>>    "torchaudio==0.7.2",
        >>>    "cellpose==0.6.1",
        >>> ]
        >>> LINKS = [
        >>>    "https://download.pytorch.org/whl/torch_stable.html"
        >>> ]
        >>>
        >>> offline_pip_prepare(packages=PACKAGES, links=LINKS)
        >>>

    Save the resulting contents of the WORKING folder as a kaggle dataset. This will
    consist of a requirements.txt file and a zip file called wheels.zip. (Let's
    assume you've called your dataset "competition-packages".)

    Create your competition notebook and add your "competition-packages" dataset
    as a data source. This will appear in in the input folder in the folder
    /input/competition-packages.

    Add the following to a code cell at the top of the notebook:

        >>> !pip install \\
        >>>    --requirement /input/competition-packages/requirements.txt \\
        >>>    --no-index \\
        >>>    --find-links file:///input/competition-packages/wheels

    Important: You need the --no-index to make this work offline!
"""

from __future__ import annotations

__author__ = "Andrew Scholan"
__credits__ = []
__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Andrew Scholan"
__email__ = "andrew.scholan@scholan.com"
__status__ = "Development"

import os
import sys
import subprocess
from typing import List, Optional

from .folders import WORKING_ROOT
from .zipout import ZipOut


def _pip_wheel(
    packages: List[str],
    links: Optional[List[str]],
    wheels_folder: str,
) -> None:
    """
    Calls pip in a subprocess to build the wheel files.

    Args:
        packages: This is the package specification list.
        links: This is a collection of find-links options, may be empty.
        wheels_folder: This is the folder where pip will build the wheel files.

    Raises:
        subprocess.CalledProcessError: in the event that the pip wheel operation
            returns a non-zero status code.
    """
    if links:
        find_links = [arg for link in links for arg in ("--find-links", f"{link}")]
    else:
        find_links = []
    subprocess.run(
        args=[
            sys.executable,
            "-m",
            "pip",
            "wheel",
            *packages,
            *find_links,
            "--progress-bar",
            "off",
            f"--wheel-dir={wheels_folder}",
        ],
        check=True,
    )


def offline_pip_prepare(packages: List[str], links: Optional[List[str]] = None) -> None:
    """
    This prepares a zip file in the working folder that can be uploaded to kaggle
    as a dataset.

    Args:
        packages: This is a list of packages to be loaded. The format of each of
            the package entries in the list is exactly as you would use in a
            requirements.txt file for pip. So, to specify a specific version of
            pytorch and the cellpose library you would specify,
            E.g. packages=["torch==1.7.1+cu110", "torchvision==0.8.2+cu110",
            "torchaudio==0.7.2", "cellpose==0.6.1"].
        links: This is an optional list that allows pip to find the appropriate
            links when preparing the packages. Often there is no need to specify
            it unless the library suggests a --find-links parameter when installing
            with pip. For pytorch, you would specify
            E.g. links=["https://download.pytorch.org/whl/torch_stable.html"]

    Raises:
        subprocess.CalledProcessError: in the event that the pip wheel operation
            returns a non-zero status code.
    """
    # Create a temporary folder where we are going to place the wheel files
    wheels = ZipOut("wheels")

    # Get pip to build the wheel files for the packages
    _pip_wheel(packages=packages, links=links, wheels_folder=wheels.folder_path)

    # Zip the wheels folder to the working directory
    _ = wheels.make_zip_file()

    # Now create the requirements.txt file.
    requirements_file_path = os.path.join(WORKING_ROOT, "requirements.txt")
    with open(requirements_file_path, "w") as f:
        for package in packages:
            f.write(f"{package}\n")
