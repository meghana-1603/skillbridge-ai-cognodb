from db.connection import get_driver

driver = get_driver()

with driver.session() as session:
    result = session.run("""
    MATCH (me:User {name:$name})-[:HAS_SKILL]->(s:Skill)
          <-[:HAS_SKILL]-(mentor:User)
    WHERE mentor <> me
    RETURN mentor.name AS mentor,
           count(s) AS common,
           collect(s.name) AS skills
    ORDER BY common DESC
    """, name="Meghana")

    for row in result:
        print(row["mentor"], row["common"], row["skills"])

driver.close()
