import asyncio
import json

from controller import Controller


class WebcandyClient:
    """
    Webcandy client to receive light configuration submission data from server.
    """

    def __init__(self, control: Controller, host: str = '127.0.0.1',
                 port: int = 6543):
        self.control = control
        self.host = host
        self.port = port

    def start(self):
        """
        Connect to the specified Webcandy server and start receiving data.
        """

        async def _start():
            reader, writer = await asyncio.open_connection(self.host, self.port)
            print(f'Connected to server {self.host}:{self.port}')

            while True:
                try:
                    data = await reader.read(100)
                    try:
                        parsed = json.loads(data.decode())
                        print(f'Received JSON: {parsed}')
                        self.control.run_script(**parsed)
                    except json.decoder.JSONDecodeError:
                        print(f'Received text: {data}')
                except KeyboardInterrupt:
                    break

            writer.close()
            print('Connecton closed')
            await writer.wait_closed()

        asyncio.run(_start())


if __name__ == '__main__':
    client = WebcandyClient(Controller())
    client.start()
