from typing import Self


class ImprovWifiMessage:
    """
    This class represents a message sent from the ImprovWifi server to the client.
    """
    MESSAGE_HEADER = b'IMPROV'

    """ Message types """
    MESSAGE_TYPE_CURRENT_STATE = 0x01
    MESSAGE_TYPE_ERROR_STATE = 0x02
    MESSAGE_TYPE_RPC_COMMAND = 0x03
    MESSAGE_TYPE_RPC_RESPONSE = 0x04

    def __init__(self, message_type, message_body):
        """
        Constructor for the ImprovWifiMessage class.

        :param message_type: The type of the message.
        :param message_body: The body of the message.
        """
        self.message_type = message_type
        self.message_body = message_body

    @staticmethod
    def from_bytes(data: bytearray) -> (int, Self):
        """
        Tries to construct a complete ImprovWifiMessage from the data and returns the index of the next
        non-consumed data in the buffer, together with the message.
        Converts a byte array to a ImprovWifiMessage instance.

        1-6	Header will equal IMPROV
        7	Version CURRENT VERSION = 1
        8	Type (see below)
        9	Length
        10...X	Data
        X + 10	Checksum

        :param data: The current data buffer
        :return: The index of the next non-consumed data in the buffer, together with the message,
                 or the next found start index and None if the message is incomplete.
        :rtype: tuple[int, GrowcubeMessage] or tuple[int, None]
        """
        # Locate the start of the message
        start_index = data.find(ImprovWifiMessage.MESSAGE_HEADER)
        if start_index == -1:
            return len(data), None

        # Check if the message is long enough to parse
        if len(data) < start_index + 12:
            return start_index, None

        version = data[start_index + 6]
        type = data[start_index + 7]
        length = data[start_index + 8]

        # Check if we got all data
        if len(data) < start_index + 12 + length:
            return start_index, None

        # Check if the message is complete  (header + version + type + length + data + checksum)
        checksum = sum(data[10:10+length]) & 0xFF
        if checksum != data[start_index + 10 + length]:
            return start_index + 12 + length, None

        # Create the message
        if type == ImprovWifiMessage.MESSAGE_TYPE_CURRENT_STATE:
            message = ImprovWifiCurrentStateMessage(type, data[start_index + 10:start_index + 10 + length])
        elif type == ImprovWifiMessage.MESSAGE_TYPE_ERROR_STATE:
            message = ImprovWifiErrorStateMessage(type, data[start_index + 10:start_index + 10 + length])
        elif type == ImprovWifiMessage.MESSAGE_TYPE_RPC_COMMAND:
            message = ImprovWifiRpcCommandMessage(type, data[start_index + 10:start_index + 10 + length])
        else:
            message = ImprovWifiMessage(type, data[start_index + 10:start_index + 10 + length])

        return start_index + 12 + length, message

    def __str__(self):
        """
        Returns a string representation of the ImprovWifiMessage object.

        :return: A string representation of the ImprovWifiMessage object.
        """
        return "ImprovWifiMessage(message_type={}, message_body={})".format(self.message_type, self.message_body)


class ImprovWifiCurrentStateMessage(ImprovWifiMessage):
    """
    This class represents a message sent from the ImprovWifi server to the client.
    """

    def __init__(self, message_type, message_body):
        """
        Constructor for the ImprovWifiMessage class.

        :param message_type: The type of the message.
        :param message_body: The body of the message.
        """
        self.message_type = message_type
        self.message_body = message_body

    def __str__(self):
        """
        Returns a string representation of the ImprovWifiMessage object.

        :return: A string representation of the ImprovWifiMessage object.
        """
        return "ImprovWifiMessage(message_type={}, message_body={})".format(self.message_type, self.message_body)

class ImprovWifiErrorStateMessage(ImprovWifiMessage):
    """
    This class represents a message sent from the ImprovWifi server to the client.
    """

    def __init__(self, message_type, message_body):
        """
        Constructor for the ImprovWifiMessage class.

        :param message_type: The type of the message.
        :param message_body: The body of the message.
        """
        self.message_type = message_type
        self.message_body = message_body

    def __str__(self):
        """
        Returns a string representation of the ImprovWifiMessage object.

        :return: A string representation of the ImprovWifiMessage object.
        """
        return "ImprovWifiMessage(message_type={}, message_body={})".format(self.message_type, self.message_body)

class ImprovWifiRpcCommandMessage(ImprovWifiMessage):
    """
    This class represents a message sent from the ImprovWifi server to the client.
    """

    def __init__(self, message_type, message_body):
        """
        Constructor for the ImprovWifiMessage class.

        :param message_type: The type of the message.
        :param message_body: The body of the message.
        """
        self.message_type = message_type
        self.message_body = message_body

    def __str__(self):
        """
        Returns a string representation of the ImprovWifiMessage object.

        :return: A string representation of the ImprovWifiMessage object.
        """
        return "ImprovWifiMessage(message_type={}, message_body={})".format(self.message_type, self.message_body)
