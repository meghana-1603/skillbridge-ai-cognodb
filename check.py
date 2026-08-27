from db.connection import get_driver

driver = get_driver()

with driver.session() as session:
    result = session.run("""
    MATCH (u:User {name:'Harish'})-[:HAS_SKILL]->(s)
    RETURN s.name
    """)

    for row in result:
        print(row["s.name"])
