from db.connection import get_driver

driver = get_driver()

# -----------------------------
# Nodes
# -----------------------------

users = [
    ("Meghana", "meghana@skillbridge.ai", 0),
    ("Varshitha", "varshitha@skillbridge.ai", 2),
    ("Sushritha", "sushritha@skillbridge.ai", 1),
    ("Harish", "harish@skillbridge.ai", 3),
    ("Badri", "badri@skillbridge.ai", 2),
]

skills = [
    ("Python", "Programming"),
    ("Java", "Programming"),
    ("SQL", "Database"),
    ("React", "Frontend"),
    ("Machine Learning", "AI"),
    ("Graph DB", "Database"),
]

companies = [
    ("Google", "Technology"),
    ("Amazon", "Technology"),
    ("Microsoft", "Technology"),
]

courses = [
    ("Complete Python", "Beginner"),
    ("Java Masterclass", "Intermediate"),
    ("SQL Bootcamp", "Beginner"),
    ("Graph Database Essentials", "Intermediate"),
]

# -----------------------------
# Relationships
# -----------------------------

user_skills = [
    ("Meghana", "Python"),
    ("Meghana", "SQL"),
    ("Meghana", "Machine Learning"),

    ("Varshitha", "Java"),
    ("Varshitha", "React"),

    ("Sushritha", "Python"),
    ("Sushritha", "Graph DB"),

    ("Harish", "Java"),
    ("Harish", "SQL"),

    ("Badri", "Python"),
    ("Badri", "React"),
]

works_at = [
    ("Varshitha", "Google"),
    ("Sushritha", "Amazon"),
    ("Harish", "Microsoft"),
    ("Badri", "Amazon"),
]

requires = [
    ("Google", "Python"),
    ("Google", "React"),
    ("Amazon", "Java"),
    ("Amazon", "SQL"),
    ("Microsoft", "Graph DB"),
    ("Microsoft", "Python"),
]

teaches = [
    ("Complete Python", "Python"),
    ("Java Masterclass", "Java"),
    ("SQL Bootcamp", "SQL"),
    ("Graph Database Essentials", "Graph DB"),
]

# -----------------------------
# Load Data into Graph
# -----------------------------

with driver.session() as session:

    # Clear existing graph
    session.run("MATCH (n) DETACH DELETE n")

    # Create Users
    for name, email, exp in users:
        session.run(
            """
            CREATE (:User {
                name: $name,
                email: $email,
                experience: $exp
            })
            """,
            name=name,
            email=email,
            exp=exp,
        )

    # Create Skills
    for name, category in skills:
        session.run(
            """
            CREATE (:Skill {
                name: $name,
                category: $category
            })
            """,
            name=name,
            category=category,
        )

    # Create Companies
    for name, industry in companies:
        session.run(
            """
            CREATE (:Company {
                name: $name,
                industry: $industry
            })
            """,
            name=name,
            industry=industry,
        )

    # Create Courses
    for title, level in courses:
        session.run(
            """
            CREATE (:Course {
                title: $title,
                level: $level
            })
            """,
            title=title,
            level=level,
        )

    # User -> Skill
    for user, skill in user_skills:
        session.run(
            """
            MATCH (u:User {name: $user})
            MATCH (s:Skill {name: $skill})
            CREATE (u)-[:HAS_SKILL]->(s)
            """,
            user=user,
            skill=skill,
        )

    # User -> Company
    for user, company in works_at:
        session.run(
            """
            MATCH (u:User {name: $user})
            MATCH (c:Company {name: $company})
            CREATE (u)-[:WORKS_AT]->(c)
            """,
            user=user,
            company=company,
        )

    # Company -> Skill
    for company, skill in requires:
        session.run(
            """
            MATCH (c:Company {name: $company})
            MATCH (s:Skill {name: $skill})
            CREATE (c)-[:REQUIRES]->(s)
            """,
            company=company,
            skill=skill,
        )

    # Course -> Skill
    for course, skill in teaches:
        session.run(
            """
            MATCH (c:Course {title: $course})
            MATCH (s:Skill {name: $skill})
            CREATE (c)-[:TEACHES]->(s)
            """,
            course=course,
            skill=skill,
        )

print("Graph database seeded successfully!")

driver.close()
