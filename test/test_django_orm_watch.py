from src.pervert.django_orm_watch import DjangoORMQuery

def test_parse_sql_query():
    # Testing an empty query
    # should not throw exception, but return empty data
    q = DjangoORMQuery({})
    assert q.model_name == "unknown"
    assert q.query[1] == "None"
    assert q.query_data == {}
    assert q.query_type == "other"
    
    