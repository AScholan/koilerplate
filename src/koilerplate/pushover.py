#!/usr/bin/env python

"""
Defines an interface to the pushover notification system. Expects to find a "dataset"
called pushover-credentials containing a JSON file called pushover_credentials.json.
This must contain two strings: "token" and "user" which are then used for pushover
notifications.
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
import json
import socket
import requests

from typing import Optional

from .folders import INPUT_ROOT


class Pushover(object):
    """
    Callable class to send notifications over pushover.net
    """

    def __init__(
        self,
        cred_file_path: Optional[str] = None,
        notebook_name: Optional[str] = None,
        echo_print: bool = True,
    ):
        """
        Creates the callable class object for handling push notifications.

        Args:
            cred_file_path: Location of the credentials file. If none is supplied
                it will assume INPUT_ROOT/pushover-credentials/pushover_credentials.json
            notebook_name: The name of the notebook. If none is given then it will default
                to NOTEBOOK_NAME, it it exists, or simply "Kaggle Notebook"
            echo_print: Choose to echo the message to the print stream, or not.
        """
        super().__init__()
        try:
            if cred_file_path is None:
                cred_file_path = os.path.join(
                    INPUT_ROOT, "pushover-credentials", "pushover_credentials.json"
                )
        except NameError:
            cred_file_path = ""
        try:
            # noinspection PyUnresolvedReferences
            self._notebook_name = notebook_name if notebook_name else NOTEBOOK_NAME
        except NameError:
            self._notebook_name = "Kaggle Notebook"
        try:
            with open(cred_file_path, "r") as f:
                credentials = json.load(f)
            self._token, self._user = credentials["token"], credentials["user"]
        except Exception:
            # Broad exception catching - means no pushover
            self._token, self._user = None, None
        self._internet_is_on = self._has_internet()
        self._report_once_fn = self._report_once
        self._echo_print = echo_print

    @staticmethod
    def _has_internet(
        host: str = "8.8.8.8", port: int = 53, timeout: float = 3
    ) -> bool:
        """
        Probes (by default google DNS) for an internet connection.

        Args:
            host: server IP address (default is 8.8.8.8
                google-public-dns-a.google.com)
            port: port number to connect with (default is 53/tcp)
            timeout: Timeout to wait for connection to succeed
        """
        try:
            socket.setdefaulttimeout(timeout)
            socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
            has_internet = True
        except socket.error:
            has_internet = False
        return has_internet

    def _report_once(self) -> None:
        """
        Used to report once on the first pushover.
        """
        print(
            f"Pushover: Internet on: {self._internet_is_on}, "
            f"Credentials: {bool(self._token and self._user)}, "
            f"Echo printing: {self._echo_print}"
        )
        self._report_once_fn = None

    def __call__(self, message: str) -> None:
        """
        This is the function that sends the notification. It is called when a object of this
        class is used as a function.

        Args:
            message: Message string, pre-formatted, to push in the notification
        """
        if self._report_once_fn:
            self._report_once_fn()
        push_msg = f"{self._notebook_name}:\n{message}"
        if self._echo_print:
            print(push_msg)
        if self._internet_is_on and self._token and self._user:
            requests.post(
                "https://api.pushover.net/1/messages.json",
                data={"token": self._token, "user": self._user, "message": push_msg},
            )


pushover = Pushover()
