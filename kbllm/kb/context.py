# third party libraries
import mgclient


class MemgraphConnection:
    """Decorator for Memgraph connection."""

    def __init__(self, func):
        """Initialize the decorator."""
        self.func = func

    def __call__(self, *args, **kwargs):
        """Connect to Memgraph and execute the function."""
        connection = mgclient.connect(host="127.0.0.1", port=7687)
        cursor = connection.cursor()
        try:
            result = self.func(cursor, *args, **kwargs)
            connection.commit()
        finally:
            connection.close()
        return result
