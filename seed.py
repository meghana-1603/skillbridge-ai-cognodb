from db.connection import get_driver

driver = get_driver()

with driver.session() as session:

    # Clear existing graph
    session.run("MATCH (n) DETACH DELETE n")

    # Create Users
    session.run("""
    CREATE (m:User {
        name: 'Meghana',
        email: 'meghana@gmail.com',
        experience: 0
    })
    CREATE (b:User {
        name: 'Badri',
        email: 'badri@gmail.com',
        experience: 2
    })
    CREATE (h:User {
        name: 'Harish',
        email: 'harish@gmail.com',
        experience: 3
    })
    CREATE (s:User {
        name: 'Sushritha',
        email: 'sushritha@gmail.com',
        experience: 1
    })
    """)

    # Create Skills
    session.run("""
    CREATE (:Skill {name: 'Python'})
    CREATE (:Skill {name: 'Java'})
    CREATE (:Skill {name: 'SQL'})
    CREATE (:Skill {name: 'Machine Learning'})
    """)

    # Create Companies
    session.run("""
    CREATE (:Company {name: 'Amazon'})
    CREATE (:Company {name: 'Google'})
    CREATE (:Company {name: 'Microsoft'})
    """)

    # Create Courses
    session.run("""
    CREATE (:Course {name: 'Python for Beginners'})
    CREATE (:Course {name: 'Java Programming'})
    CREATE (:Course {name: 'SQL Fundamentals'})
    CREATE (:Course {name: 'Machine Learning Basics'})
    """)

    # User -> Skill relationships
    session.run("""
    MATCH (m:User {name: 'Meghana'})
    MATCH (b:User {name: 'Badri'})
    MATCH (h:User {name: 'Harish'})
    MATCH (s:User {name: 'Sushritha'})

    MATCH (py:Skill {name: 'Python'})
    MATCH (ja:Skill {name: 'Java'})
    MATCH (sq:Skill {name: 'SQL'})
    MATCH (ml:Skill {name: 'Machine Learning'})

    MERGE (m)-[:HAS_SKILL]->(py)
    MERGE (m)-[:HAS_SKILL]->(sq)
    MERGE (m)-[:HAS_SKILL]->(ml)

    MERGE (b)-[:HAS_SKILL]->(py)

    MERGE (h)-[:HAS_SKILL]->(ja)
    MERGE (h)-[:HAS_SKILL]->(sq)

    MERGE (s)-[:HAS_SKILL]->(py)
    """)

    # User -> Company relationships
    session.run("""
    MATCH (b:User {name: 'Badri'})
    MATCH (s:User {name: 'Sushritha'})
    MATCH (h:User {name: 'Harish'})

    MATCH (a:Company {name: 'Amazon'})
    MATCH (ms:Company {name: 'Microsoft'})

    MERGE (b)-[:WORKS_AT]->(a)
    MERGE (s)-[:WORKS_AT]->(a)
    MERGE (h)-[:WORKS_AT]->(ms)
    """)

    # Company -> Required Skills
    session.run("""
    MATCH (a:Company {name: 'Amazon'})
    MATCH (g:Company {name: 'Google'})
    MATCH (ms:Company {name: 'Microsoft'})

    MATCH (py:Skill {name: 'Python'})
    MATCH (ja:Skill {name: 'Java'})
    MATCH (sq:Skill {name: 'SQL'})
    MATCH (ml:Skill {name: 'Machine Learning'})

    MERGE (a)-[:REQUIRES_SKILL]->(py)
    MERGE (a)-[:REQUIRES_SKILL]->(sq)

    MERGE (g)-[:REQUIRES_SKILL]->(py)
    MERGE (g)-[:REQUIRES_SKILL]->(ml)

    MERGE (ms)-[:REQUIRES_SKILL]->(ja)
    MERGE (ms)-[:REQUIRES_SKILL]->(sq)
    """)

print("Database seeded successfully!")

driver.close()
