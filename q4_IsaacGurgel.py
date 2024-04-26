tables = lambda: {
    "PUBLISHERS": {'info': ["id_publisher", "name", "country"], 'alias': "p"},
    "BOOKCLUBS": {'info': ["id_club", "name", "id_publisher", "creation_date"], 'alias': "b"},
    "MEMBERS": {'info': ["id", "name", "country", "id_club"], 'alias': "m"},
    "BOOKS": {'info': ["id_book", "title", "genre", "release_date", "id_club"], 'alias': "bk"}
}

select = lambda table, alias, columns=None: f"SELECT {', '.join([ col for col in columns]) if columns else alias + '.*'} FROM {table} {alias}\n"

selectEqualColumns = lambda table1, table2: [c for c in tables()[table1]['info'] if c in tables()[table2]['info']]

innerJoinSelect = lambda table1, table2, join_condition: f" INNER JOIN {table2} {tables()[table2]['alias']} ON " + join_condition + "\n"

whereSelect = lambda where: f" WHERE {where}" if where else ""

generate_query = lambda main_table, main_alias, join_table, join_alias, join_condition, columns=None, where_clause=None: select(main_table, main_alias, columns) + innerJoinSelect(main_alias, join_table, join_condition) + whereSelect(where_clause)

print_query = lambda main_table, main_alias, join_table, join_alias, join_condition, columns=None, where_clause=None: print(generate_query(main_table, main_alias, join_table, join_alias, join_condition, columns, where_clause))

# Exemplo de uso:
print_query("BOOKS", "bk", "BOOKCLUBS", "b", "bk.id_club = b.id_club AND bk.release_date = b.creation_date", columns=["bk.title", "b.name"], where_clause="b.creation_date > '2020-01-01'")
