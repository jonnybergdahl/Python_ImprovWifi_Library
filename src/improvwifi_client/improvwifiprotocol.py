import asyncio
import logging
from typing import Callable

from .improvwifimessage import ImprovWifiMessage


class ImprovWiFiSerialProtocol(asyncio.Protocol):

    RPC_HEADER = b'IMPROV'
    RPC_VERSION = 1

    def __init__(self, on_connected: Callable[[str], None],
                 on_message: Callable[[str], None],
                 on_connection_lost: Callable[[], None]):
        self._data = None
        self.transport = None
        self._on_connected = on_connected
        self._on_message = on_message
        self._on_connection_lost = on_connection_lost

    def connection_made(self, transport):
        self.transport = transport
        logging.info("Connection established.")
        if self._on_connected:
            self._on_connected()

    def data_received(self, data):
        """
        Called when data is received.
        :param data:
        :return: None
        """
        self._data += data
        # check for complete message
        new_index, message = ImprovWifiMessage.from_bytes(self._data)
        self._data = self._data[new_index:]

        if message is not None:
            logging.debug(f"message: {message._command} - {message.payload}")
            if self._on_message:
                self._on_message(message)

    def connection_lost(self, exc):
        logging.debug("Serial connection closed")
        if self._on_connection_lost:
            self._on_connection_lost()

    def send_message(self, message: ImprovWifiMessage):
        self.transport.write(message.to_bytes())