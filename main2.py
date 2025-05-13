from lcu_driver import Connector

connector = Connector()


@connector.ready
async def connect(connection):
    print("Connected to League Client.")


@connector.close
async def disconnect(_):
    print("Disconnected from League Client.")


connector.start()
