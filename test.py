from db.connection import get_driver

driver = get_driver()

with driver.session() as session:
    result = session.run("RETURN 'Connected Successfully!' AS msg")
    print(result.single()["msg"])

driver.close()
