import asyncio
import logging
from typing import Callable

import serial_asyncio

from .improvwifimessage import ImprovWifiMessage
from .improvwifiprotocol import ImprovWiFiSerialProtocol


class ImprovWifiSerialClient:
    """
    Class for the Improv Wi-Fi serial client
    """

    def __init__(self, port: str, speed: int,
                 on_message: Callable[[ImprovWifiMessage], None],
                 on_connected: Callable[[str], None] = None,
                 on_disconnected: Callable[[str], None] = None) -> None:
        """
        ImprovWifiSerialClient constructor

        :param port: Serial port name.
        :param callback: Callback function to receive data from the Improv Wi-Fi.
        """
        self.port = port
        self.speed = speed
        self._on_message_callback = on_message
        self._on_connected_callback = on_connected
        self._on_disconnected_callback = on_disconnected
        self._exit = False
        self._data = b''
        self.transport = None
        self.protocol = None
        self.connected = False
        self.connection_timeout = 30

    def connect(self) -> bool:
        """
        Connects to Improv Wi-Fi serial device

        :return: True if the connection was established, False otherwise.
        :rtype: bool
        """
        logging.info(f"Connecting to {self.port}...")
        try:
            loop = asyncio.get_event_loop()
            coro = serial_asyncio.create_serial_connection(loop,
                                                           lambda: ImprovWiFiSerialProtocol(self.on_connected,
                                                                                            self.on_message,
                                                                                            self.on_connection_lost),
                                                           self.port, baudrate=self.speed)
            loop.run_until_complete(coro)
            loop.run_until_complete(self.wait_for_connection())
            loop.run_forever()
        except Exception as e:
            logging.error(e)
            return False
        return True

    def on_connected(self):
        """
        Callback function for when the connection is established
        """
        self.connected = True
        logging.debug(f"Connected to {self.port}")
        if self._on_connected_callback:
            self._on_connected_callback(self.host)

    def on_message(self, message: ImprovWifiMessage) -> None:
        """
        Callback function for when a message is received from the Improv Wi-Fi

        :param message: The received ImprovWifiMessage.
        :type message: ImprovWifiMessage
        """
        logging.debug(f"< {message}")
        if self._on_message_callback:
            self._on_message_callback(message)

    def on_connection_lost(self):
        """
        Callback function for when the connection is lost
        """
        logging.debug(f"Connection to {self.port} lost")
        self.connected = False
        if self._on_disconnected_callback:
            self._on_disconnected_callback(self.port)