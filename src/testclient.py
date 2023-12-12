from improvwifi_client import ImprovWifiSerialClient
from improvwifi_client import ImprovWifiMessage

if __main__ == "__main__":
    # Set serial port and speed
    PORT = "/dev/ttyUSB0"
    SPEED = 115200

    # Define a callback function to print messages to the screen
    def callback(message: ImprovWifiMessage) -> None:
        # Just dump the message to the console
        print(f"Received: {message.get_description()}")

    # Create a client instance
    client = ImprovWifiSerialClient(PORT, SPEED, callback)

    # Connect to the Improv Wi-Fi and start listening for messages
    client.connect()