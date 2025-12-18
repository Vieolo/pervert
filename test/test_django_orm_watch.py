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
    qd1 = {"time": "10", "sql": qr1}
    qq1 = DjangoORMQuery(qd1)
    assert qq1.model_name == "book_book"
    assert qq1.query[1] == "SELECT (13 fields) FROM book_book"
    assert qq1.query[2] == 'SELECT (13 fields) FROM "book_book" WHERE "book_book"."id" = 1'
    assert qq1.query[3] == qr1
    assert qq1.query_data == qd1
    assert qq1.query_type == "select"
    
    qr2 = '''INSERT INTO "book_tag" ("created_at", "added_by_id", "book_id", "name") VALUES ('2025-12-18 10:21:52.423966', 1, 1, 'biography') RETURNING "book_tag"."id"'''
    qd2 = {"time": "10", "sql": qr2}
    qq2 = DjangoORMQuery(qd2)
    assert qq2.model_name == "book_tag"
    assert qq2.query[1] == "INSERT INTO book_tag (4 fields)"
    assert qq2.query[2] == 'INSERT INTO book_tag (4 fields) RETURNING "book_tag"."id"'
    assert qq2.query[3] == qr2
    assert qq2.query_data == qd2
    assert qq2.query_type == "insert"
    
    qr3 = '''UPDATE "book_book" SET "created_at" = '2025-12-18 09:55:33.090100', "self_updated_at" = '2025-12-18', "author_updated_at" = NULL, "deleted_at" = NULL, "added_by_id" = 1, "owner_id" = 1, "name" = 'org 1', "book_type" = 'non-fiction', "cover_image" = '', "ispn" = "1234", "website" = NULL, "price" = 1299 WHERE "book_book"."id" = 1'''
    qd3 = {"time": "10", "sql": qr3}
    qq3 = DjangoORMQuery(qd3)
    assert qq3.model_name == "book_book"
    assert qq3.query[1] == "UPDATE book_book (12 fields)"
    assert qq3.query[2] == 'UPDATE book_book (12 fields) WHERE "book_book"."id" = 1'
    assert qq3.query[3] == qr3
    assert qq3.query_data == qd3
    assert qq3.query_type == "update"
    
    
    qr4 = 'DELETE FROM "book_tag" WHERE "book_tag"."id" IN (1)'
    qd4 = {"time": "10", "sql": qr4}
    qq4 = DjangoORMQuery(qd4)
    assert qq4.model_name == "book_tag"
    assert qq4.query[1] == "DELETE FROM book_tag"
    assert qq4.query[2] == qr4
    assert qq4.query[3] == qr4
    assert qq4.query_data == qd4
    assert qq4.query_type == "delete"
    