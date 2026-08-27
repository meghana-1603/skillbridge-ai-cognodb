from db.connection import get_driver

driver = get_driver()

def get_counts():
    with driver.session() as session:

        users = session.run(
            "MATCH (u:User) RETURN count(u) AS total"
        ).single()["total"]

        skills = session.run(
            "MATCH (s:Skill) RETURN count(s) AS total"
        ).single()["total"]

        companies = session.run(
            "MATCH (c:Company) RETURN count(c) AS total"
        ).single()["total"]

        courses = session.run(
            "MATCH (c:Course) RETURN count(c) AS total"
        ).single()["total"]

        return {
            "users": users,
            "skills": skills,
            "companies": companies,
            "courses": courses
        }


def get_all_users():
    with driver.session() as session:

        result = session.run("""
        MATCH (u:User)
        RETURN u.name AS name
        ORDER BY name
        """)

        return [record["name"] for record in result]
def get_user_profile(user_name):
    with driver.session() as session:

        result = session.run("""
        MATCH (u:User {name:$name})
        OPTIONAL MATCH (u)-[:HAS_SKILL]->(s:Skill)
        OPTIONAL MATCH (u)-[:WORKS_AT]->(c:Company)

        RETURN
            u.name AS name,
            u.email AS email,
            u.experience AS experience,
            c.name AS company,
            collect(DISTINCT s.name) AS skills
        """, name=user_name)

        return result.single()
def find_mentors(user_name):
    with driver.session() as session:

        result = session.run("""
        MATCH (me:User {name:$name})-[:HAS_SKILL]->(s:Skill)
              <-[:HAS_SKILL]-(mentor:User)

        WHERE mentor <> me

        RETURN
            mentor.name AS mentor,
            count(s) AS common_skills,
            collect(s.name) AS shared_skills

        ORDER BY common_skills DESC
        """, name=user_name)

        return list(result)
def get_all_companies():
    with driver.session() as session:

        result = session.run("""
        MATCH (c:Company)
        RETURN c.name AS name
        ORDER BY name
        """)

        return [record["name"] for record in result]


def get_company_users(company_name):
    with driver.session() as session:

        result = session.run("""
        MATCH (u:User)-[:WORKS_AT]->(c:Company {name:$name})
        OPTIONAL MATCH (u)-[:HAS_SKILL]->(s:Skill)

        RETURN
            u.name AS name,
            u.email AS email,
            collect(DISTINCT s.name) AS skills

        ORDER BY name
        """, name=company_name)

        return list(result)
def get_company_skills(company_name):
    with driver.session() as session:

        result = session.run("""
        MATCH (c:Company {name:$name})-[:REQUIRES_SKILL]->(s:Skill)

        RETURN s.name AS skill
        ORDER BY skill
        """, name=company_name)

        return [record["skill"] for record in result]
def get_company_skills(company_name):
    with driver.session() as session:

        result = session.run("""
        MATCH (c:Company {name:$name})-[:REQUIRES_SKILL]->(s:Skill)
        RETURN s.name AS skill
        ORDER BY skill
        """, name=company_name)

        return [record["skill"] for record in result]
