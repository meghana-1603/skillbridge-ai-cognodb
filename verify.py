from db.connection import get_driver

driver = get_driver()

with driver.session() as session:
    result = session.run("""
        MATCH (u:User)-[:HAS_SKILL]->(s:Skill)
        RETURN u.name AS user, collect(s.name) AS skills
    """)

    for row in result:
        print(f"{row['user']} -> {row['skills']}")

driver.close()
