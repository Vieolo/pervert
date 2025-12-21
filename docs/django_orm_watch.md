# DjangoORMWatch
This class provides helper functions to list and monitor the frequency and the structure of the SQL queries. Monitoring and profiling the SQL queries is necessary as it is very easy to overlook the number of queries made and thier scope during the handling of a request.

## Basic Usage
Here is a basic usage. It involves creating an instance of `DjangoORMWatch` at the start of the code and then call stop on the instance when the code to be evaluated is completed. The `stop` function returns a reference of the self and you can either use the `print` function to print all of the data or use the data of the instance.

Have in mind that `DjangoORMWatch` works only when `DEBUG` is set to True

```python
from pervpy.django_orm_watch import DjangoORMWatch

# Start the watcher instance
watch = DjangoORMWatch()

# Run your code, making the queries
#
# The code does not need to be a single query. You can use `DjangoORMWatch` on
# any size of code, during the normal run, or unit tests
books = Book.objects.filter(name__icontains="dragon")
# or
invoke_a_view()

# Stop the watch and print the result
watch.stop().print(verbosity=1)
```

## Static usage
In many cases you may not be able to create an instance and have access to the instance at the end of your code. This may happen, for example, if you are evaluating the entire lifecycle of a request. In such cases, you can use the static functions to get the queries. The main functionalities remain intact but a few minor features may be lost.

```python
# To reset the queries in the connection
DjangoORMWatch.reset_queries()

# Run your code
invoke_a_view()

# Call the `eval` function to get the queries. Eval calls the `stop` function
# under the hood and your can use the return value as a normal `DjangoORMWatch` instance
#
# Note that you do not need to call the `eval` and `reset_queries` in the same place, but
# of course, `reset_queries` should be called first
DjangoORMWatch.eval().print(verbosity=1)
```