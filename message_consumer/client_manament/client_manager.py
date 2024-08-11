class ClientManager:
    consumer = None
    connected_clients = []
    maximum_clients = 50

    def __init__(self, consumer):
        self.consumer = consumer

        # Singleton pattern
        if not hasattr(self.__class__, 'instance'):
            self.__class__.instance = self
        else:
            self.__class__.instance = self

    def add_client(self, client):
        if len(self.connected_clients) < self.maximum_clients:
            self.connected_clients.append(client)
            return True
        return False

    def remove_client(self, client):
        self.connected_clients.remove(client)

    def is_allowed_to_connect(self):
        return len(self.connected_clients) < self.maximum_clients and self._is_unique_client(self.consumer)

    def _is_unique_client(self, client):
        return client not in self.connected_clients
