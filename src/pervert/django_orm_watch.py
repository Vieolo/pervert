# Python
import time
from typing import TYPE_CHECKING, Literal

# Django
from django.db import connections as db_connections, reset_queries

if TYPE_CHECKING:
    from django.db.backends.base.base import BaseDatabaseWrapper
    

class DjangoORMQuery:

    def __init__(self, raw_dict: dict[str, str]):
        # Saving the dict received the `queries` properties of the connection
        self.query_data: dict[str, str] = raw_dict
        
        # The time calculated 
        self.time: str = raw_dict["time"]
        
        # Saving the different verbosity levels of the query
        qs: str = raw_dict["sql"]
        self.query_type: Literal["select", "update", "insert", "delete", "other"] = "other"
        self.model_name = "unknown"
        self.query: dict[int, str] = {
            1: qs,
            2: qs,
            3: qs,
        }
        
        if qs.startswith("SELECT"):
            self.model_name = qs.split('FROM "')[1].split('"')[0]
            self.query_type = "select"

            before_from = qs.split("FROM")[0]
            after_from = qs.split("FROM")[1]

            # Django doesn't use SELECT * FROM ...
            # Instead, it uses SELECT "user"."id", "user"."name", ... FROM ...
            # So, to shorten it, we count the items and add it between the SELECT and FROM
            field_count = len(before_from.split(","))
            if field_count > 1:
                self.query[1] = f"Select ({field_count} fields) FROM {self.model_name}"
                self.query[2] = f"Select ({field_count} fields) FROM {after_from}"
        


class DjangoORMWatch:

    def __init__(self):
        # Clearing the connection history
        reset_queries()
        
        # Setting the empty connection list
        self.connections: list[BaseDatabaseWrapper] = []
        
        # Starting the total timer
        self.start = time.perf_counter()
        
        # Then end time, will be set after calling the `stop` function
        self.end: float = 0
    

    @classmethod
    def start(cls) -> 'DjangoORMWatch':
        """A convenience function to create an instance of `DjangoORMWatch` which
        in turn, starts watching for ORM queries

        Returns:
            DjangoORMWatch: A new instance of the class
        """
        return cls()
    

    def stop(self) -> 'DjangoORMWatch':
        """Stops the watch and stores the queries for further processing
        """
        # Stopping the end timer
        self.end = time.perf_counter()

        # Storing the final queries
        self.connections: list[BaseDatabaseWrapper] = db_connections.all()
        self.queries: list[DjangoORMQuery] = []
        
        for c in self.connections:
            for q in c.queries:
                self.queries.append(DjangoORMQuery(q))
        
        return self
    
    def print(self, verbosity: Literal[0, 1, 2, 3] = 2):
        """Prints the query data and their overview

        By passing the verbosity level, you can choose how detailed the queries should be printed

        Args:
            verbosity (Literal[0, 1, 2, 3], optional): The verbosity level of the queries. Defaults to 2.
        """
        v = verbosity
        if verbosity not in [0, 1, 2, 3]:
            v = 2
        duration = self.end - self.start
        
        if verbosity > 0:
            print("******************************")
            print(f"Start of queries - Verbosity level {v}" + (" (original)" if v == 3 else ""))
            print("******************************")
            
            index = 1
            for q in self.queries:
                print("-=-=-=-==-=")
                print(f"No. {index}")
                print(f"Model: {q.model_name}")
                print(f"Time: {q.time}")
                print("-")
                print(q.query[v])
                print("-=-=-=-==-=")
                index += 1

            print("******************************")
            print("End of queries")

        print("******************************")
        print("Overview of the queries:")
        print(f"\tConnections: {len(self.connections)}")
        print(f"\tQueries: {len(self.queries)}")
        print(f"\tTime: {duration: .6f}s")
        print("******************************")
