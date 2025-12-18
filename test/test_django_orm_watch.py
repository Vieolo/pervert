from src.pervert.django_orm_watch import DjangoORMQuery

def test_parse_sql_query():
    # Testing an empty query
    # should not throw exception, but return empty data
    qq0 = DjangoORMQuery({})
    assert qq0.model_name == "unknown"
    assert qq0.query[1] == "None"
    assert qq0.query_data == {}
    assert qq0.query_type == "other"
    
    
    qr1 = 'SELECT "book_book"."id", "book_book"."created_at", "book_book"."self_updated_at", "book_book"."author_updated_at", "book_book"."deleted_at", "book_book"."added_by_id", "book_book"."owner_id", "book_book"."name", "book_book"."book_type", "book_book"."cover_image", "book_book"."ispn", "book_book"."website", "book_book"."price" FROM "book_book" WHERE "book_book"."id" = 1'
    qd1 = {
        "time": "10",
        "sql": qr1,
    }    
    qq1 = DjangoORMQuery(qd1)
    assert qq1.model_name == "book_book"
    assert qq1.query[1] == "SELECT (13 fields) FROM book_book"
    assert qq1.query[2] == 'SELECT (13 fields) FROM "book_book" WHERE "book_book"."id" = 1'
    assert qq1.query[3] == qr1
    assert qq1.query_data == qd1
    assert qq1.query_type == "select"
    
    