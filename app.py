import streamlit as st
from db.queries import( get_counts, get_all_users, get_user_profile,find_mentors,get_all_companies,
    get_company_users, get_company_skills)

st.set_page_config(
    page_title="SkillBridge AI",
    page_icon="🕸️",
    layout="wide"
)

counts = get_counts()

st.title("🕸️ SkillBridge AI")
st.subheader("Graph-Powered Career Networking Platform")

st.markdown("---")

col1, col2 = st.columns([2,1])

with col1:
    st.markdown("""
    ## Discover Career Connections

    Explore relationships between people, skills,
    companies and learning resources using
    a Graph Database.
    """)
st.header("User Explorer")

users = get_all_users()

selected_user = st.selectbox(
    "Select a User",
    users
)

profile = get_user_profile(selected_user)

left, right = st.columns([1,2])

with left:
    st.subheader("Profile")

    st.metric("Experience", f"{profile['experience']} yrs")

    company = profile["company"] if profile["company"] else "Student"
    st.metric("Company", company)

with right:
    st.subheader(profile["name"])

    st.write(profile["email"])

    st.write("### Skills")

    for skill in profile["skills"]:
        st.success(skill)

with col2:
    st.info("""
    **Backend**

    Python + Streamlit

    **Database**

    CognoDB
    """)

st.markdown("---")

st.markdown("## Live Database Statistics")

a,b,c,d = st.columns(4)

a.metric("👤 Users", counts["users"])
b.metric("💻 Skills", counts["skills"])
c.metric("🏢 Companies", counts["companies"])
d.metric("📚 Courses", counts["courses"])

st.markdown("---")
st.header("🤝 Mentor Recommendations")

mentors = find_mentors(selected_user)

if len(mentors) == 0:
    st.info("No mentors found.")
else:
    for mentor in mentors:
        with st.container(border=True):

            col1, col2 = st.columns([3,1])

            with col1:
                st.subheader(mentor["mentor"])
                st.write("**Shared Skills:** " +
                         ", ".join(mentor["shared_skills"]))

            with col2:
                st.metric("Match", mentor["common_skills"])
st.markdown("---")
st.header("🏢 Company Explorer")

companies = get_all_companies()

selected_company = st.selectbox(
    "Select a Company",
    companies
)

company_users = get_company_users(selected_company)

if len(company_users) == 0:
    st.info("No employees found.")
else:
    for user in company_users:
        with st.container(border=True):
            st.subheader(user["name"])
            st.write("**Email:**", user["email"])
            st.write("**Skills:**", ", ".join(user["skills"]))
st.subheader("🎯 Required Skills")

company_skills = get_company_skills(selected_company)

if len(company_skills) == 0:
    st.info("No required skills found.")
else:
    for skill in company_skills:
        st.success(skill)

st.success("Database connected successfully!")
