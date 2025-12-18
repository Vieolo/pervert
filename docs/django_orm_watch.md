# DjangoORMWatch
This class provides helper functions to list and monitor the frequency and the structure of the SQL queries. Monitoring and profiling the SQL queries is necessary as it is very easy to overlook the number of queries made and thier scope during the handling of a request.

## Usage
Here is a sample usage:

```python
from pervpy.django_orm_watch import DjangoORMWatch

# Start the watcher instance
watch = DjangoORMWatch()

# Run your code, making the queries
books = Book.objects.filter(name__icontains="dragon")

# Stop the watch and print the result
watch.stop().print(verbosity=1)
```