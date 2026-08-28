import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.write("DB_URI exists:", "DB_URI" in st.secrets)
st.write("DB_USER exists:", "DB_USER" in st.secrets)
st.write("DB_PASSWORD exists:", "DB_PASSWORD" in st.secrets)

if "DB_URI" in st.secrets:
    st.write("URI prefix:", st.secrets["DB_URI"][:8])
from db.queries import (
    get_counts,
    get_all_users,
    get_user_profile,
    find_mentors,
    get_all_companies,
    get_company_users,
    get_company_skills,
    get_skill_counts,
    get_company_counts,
)

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SkillBridge AI",
    page_icon="🕸️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1400px;
    }

    .hero {
        padding: 2rem;
        border-radius: 20px;
        background: linear-gradient(135deg, #111827, #1e293b);
        color: white;
        margin-bottom: 1.5rem;
    }

    .hero h1 {
        font-size: 3rem;
        margin-bottom: 0.3rem;
    }

    .hero p {
        font-size: 1.15rem;
        color: #cbd5e1;
    }

    .skill-badge {
        display: inline-block;
        padding: 0.35rem 0.75rem;
        margin: 0.25rem;
        border-radius: 999px;
        background: #e0e7ff;
        color: #3730a3;
        font-weight: 600;
        font-size: 0.85rem;
    }

    .match-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 999px;
        background: #dcfce7;
        color: #166534;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🕸️ SkillBridge AI")

    st.caption("Graph-Powered Career Networking")

    st.markdown("---")

    page = st.radio(
        "Navigate",
        [
            "🏠 Dashboard",
            "👤 User Explorer",
            "🤝 Mentor Network",
            "🏢 Company Explorer",
            "🕸️ Graph View",
        ],
    )

    st.markdown("---")

    st.caption("Technology Stack")

    st.write("Python • Streamlit")
    st.write("CognoDB • Neo4j Driver")
    st.write("Cypher")

# ============================================================
# DATABASE CONNECTION
# ============================================================

try:

    counts = get_counts()

except Exception:

    st.error(
        """
        ⚠️ **Database connection failed**

        SkillBridge AI could not connect to CognoDB.

        Please check your `.env` configuration and make sure
        the database instance is available.
        """
    )

    st.stop()

# ============================================================
# HERO
# ============================================================

st.markdown(
    """
<div class="hero">
<h1>🕸️ SkillBridge AI</h1>
<p>Discover career connections through people, skills, companies and learning resources.</p>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.header("📊 Platform Overview")

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👤 Users",
        counts["users"],
    )

    col2.metric(
        "🧠 Skills",
        counts["skills"],
    )

    col3.metric(
        "🏢 Companies",
        counts["companies"],
    )

    col4.metric(
        "📚 Courses",
        counts["courses"],
    )

    st.markdown("---")

    # --------------------------------------------------------
    # CHARTS
    # --------------------------------------------------------

    left, right = st.columns(2)

    # ========================================================
    # SKILLS DISTRIBUTION
    # ========================================================

    with left:

        st.subheader("🧠 Skills Distribution")

        skills_data = get_skill_counts()

        df = pd.DataFrame(skills_data)

        if not df.empty and "skill" in df.columns:

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=df["skill"],
                    y=df["users"],
                    text=df["users"],
                    textposition="auto",
                )
            )

            fig.update_layout(
                height=380,
                margin=dict(
                    l=20,
                    r=20,
                    t=30,
                    b=20,
                ),
                xaxis_title="Skill",
                yaxis_title="Users",
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
            )

        else:

            st.info(
                "No skill statistics available."
            )

    # ========================================================
    # COMPANY DISTRIBUTION
    # ========================================================

    with right:

        st.subheader("🏢 Employees by Company")

        company_data = get_company_counts()

        df2 = pd.DataFrame(company_data)

        if not df2.empty and "company" in df2.columns:

            fig2 = go.Figure()

            fig2.add_trace(
                go.Bar(
                    x=df2["company"],
                    y=df2["employees"],
                    text=df2["employees"],
                    textposition="auto",
                )
            )

            fig2.update_layout(
                height=380,
                margin=dict(
                    l=20,
                    r=20,
                    t=30,
                    b=20,
                ),
                xaxis_title="Company",
                yaxis_title="Employees",
            )

            st.plotly_chart(
                fig2,
                use_container_width=True,
            )

        else:

            st.info(
                "No company statistics available."
            )

    # --------------------------------------------------------
    # WHY GRAPH
    # --------------------------------------------------------

    st.markdown("---")

    st.header("💡 Why a Graph Database?")

    st.info(
        """
        SkillBridge AI is relationship-centric.

        A user is connected to skills, companies and other
        professionals. These relationships can be traversed
        naturally using a graph database.

        **Example:**

        User → Skill ← Mentor

        This makes mentor discovery and career relationship
        exploration easier to express using Cypher.
        """
    )

# ============================================================
# USER EXPLORER
# ============================================================

elif page == "👤 User Explorer":

    st.header("👤 User Explorer")

    users = get_all_users()

    if not users:

        st.info("No users found.")

        st.stop()

    selected_user = st.selectbox(
        "Select a user",
        users,
    )

    profile = get_user_profile(
        selected_user
    )

    if profile is None:

        st.warning(
            "User profile could not be found."
        )

        st.stop()

    left, right = st.columns(
        [1, 2]
    )

    # --------------------------------------------------------
    # PROFILE
    # --------------------------------------------------------

    with left:

        st.subheader("Profile")

        experience = (
            profile["experience"]
            if profile["experience"] is not None
            else 0
        )

        company = (
            profile["company"]
            if profile["company"]
            else "Student"
        )

        st.metric(
            "Experience",
            f"{experience} yrs",
        )

        st.metric(
            "Company",
            company,
        )

    # --------------------------------------------------------
    # SKILLS
    # --------------------------------------------------------

    with right:

        st.subheader(
            profile["name"]
        )

        st.write(
            profile["email"]
        )

        st.markdown("### 🧠 Skills")

        skills = profile["skills"]

        if skills:

            badges = ""

            for skill in skills:

                badges += (
                    f'<span class="skill-badge">'
                    f'{skill}'
                    f'</span>'
                )

            st.markdown(
                badges,
                unsafe_allow_html=True,
            )

        else:

            st.info(
                "No skills listed."
            )

# ============================================================
# MENTOR NETWORK
# ============================================================

elif page == "🤝 Mentor Network":

    st.header("🤝 Mentor Network")

    users = get_all_users()

    if not users:

        st.info("No users available.")

        st.stop()

    selected_user = st.selectbox(
        "Find mentors for",
        users,
    )

    st.caption(
        "Mentors are ranked by the number of shared skills."
    )

    mentors = find_mentors(
        selected_user
    )

    if not mentors:

        st.info(
            "No mentors found for this user."
        )

    else:

        for mentor in mentors:

            shared_skills = (
                mentor["shared_skills"]
            )

            common_skills = (
                mentor["common_skills"]
            )

            with st.container(
                border=True
            ):

                col1, col2 = st.columns(
                    [4, 1]
                )

                with col1:

                    st.subheader(
                        f"👤 {mentor['mentor']}"
                    )

                    st.write(
                        "Shared skills:"
                    )

                    if shared_skills:

                        badges = ""

                        for skill in shared_skills:

                            badges += (
                                f'<span class="skill-badge">'
                                f'{skill}'
                                f'</span>'
                            )

                        st.markdown(
                            badges,
                            unsafe_allow_html=True,
                        )

                with col2:

                    st.metric(
                        "Shared Skills",
                        common_skills,
                    )

                    st.markdown(
                        '<span class="match-badge">'
                        'Strong Match'
                        '</span>',
                        unsafe_allow_html=True,
                    )

# ============================================================
# COMPANY EXPLORER
# ============================================================

elif page == "🏢 Company Explorer":

    st.header("🏢 Company Explorer")

    companies = get_all_companies()

    if not companies:

        st.info(
            "No companies found."
        )

        st.stop()

    selected_company = st.selectbox(
        "Select a company",
        companies,
    )

    employees = get_company_users(
        selected_company
    )

    required_skills = get_company_skills(
        selected_company
    )

    left, right = st.columns(2)

    # --------------------------------------------------------
    # EMPLOYEES
    # --------------------------------------------------------

    with left:

        st.subheader("👥 Employees")

        if not employees:

            st.info(
                "No employees found."
            )

        else:

            for user in employees:

                with st.container(
                    border=True
                ):

                    st.subheader(
                        user["name"]
                    )

                    st.caption(
                        user["email"]
                    )

                    if user["skills"]:

                        st.write(
                            "**Skills:** "
                            + ", ".join(
                                user["skills"]
                            )
                        )

    # --------------------------------------------------------
    # REQUIRED SKILLS
    # --------------------------------------------------------

    with right:

        st.subheader(
            "🎯 Required Skills"
        )

        if not required_skills:

            st.info(
                "No required skills found."
            )

        else:

            for skill in required_skills:

                st.success(
                    f"✓ {skill}"
                )

# ============================================================
# GRAPH VIEW
# ============================================================

elif page == "🕸️ Graph View":

    st.header(
        "🕸️ Career Relationship Graph"
    )

    st.write(
        """
        Explore how users connect through shared skills.

        The graph demonstrates a multi-hop relationship:

        **User → Skill ← Mentor**
        """
    )

    users = get_all_users()

    if not users:

        st.info(
            "No graph data available."
        )

        st.stop()

    selected_user = st.selectbox(
        "Select a user",
        users,
    )

    profile = get_user_profile(
        selected_user
    )

    mentors = find_mentors(
        selected_user
    )

    # --------------------------------------------------------
    # GRAPH DATA
    # --------------------------------------------------------

    nodes = []

    edges = []

    positions = {}

    # --------------------------------------------------------
    # USER NODE
    # --------------------------------------------------------

    nodes.append(
        {
            "id": selected_user,
            "label": selected_user,
            "type": "User",
        }
    )

    positions[selected_user] = (
        0,
        0,
    )

    # --------------------------------------------------------
    # SKILL NODES
    # --------------------------------------------------------

    user_skills = (
        profile["skills"]
        if profile["skills"]
        else []
    )

    for i, skill in enumerate(
        user_skills
    ):

        skill_id = (
            f"skill_{i}"
        )

        nodes.append(
            {
                "id": skill_id,
                "label": skill,
                "type": "Skill",
            }
        )

        positions[skill_id] = (
            1,
            i - (
                len(user_skills) - 1
            ) / 2,
        )

        edges.append(
            (
                selected_user,
                skill_id,
            )
        )

    # --------------------------------------------------------
    # MENTOR NODES
    # --------------------------------------------------------

    for i, mentor in enumerate(
        mentors
    ):

        mentor_name = mentor[
            "mentor"
        ]

        nodes.append(
            {
                "id": mentor_name,
                "label": mentor_name,
                "type": "Mentor",
            }
        )

        positions[mentor_name] = (
            2,
            i - (
                len(mentors) - 1
            ) / 2,
        )

        for shared_skill in mentor[
            "shared_skills"
        ]:

            for node in nodes:

                if (
                    node["type"]
                    == "Skill"
                    and node["label"]
                    == shared_skill
                ):

                    edges.append(
                        (
                            mentor_name,
                            node["id"],
                        )
                    )

    # --------------------------------------------------------
    # EDGES
    # --------------------------------------------------------

    edge_x = []
    edge_y = []

    for source, target in edges:

        x0, y0 = positions[source]

        x1, y1 = positions[target]

        edge_x.extend(
            [
                x0,
                x1,
                None,
            ]
        )

        edge_y.extend(
            [
                y0,
                y1,
                None,
            ]
        )

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(
            width=2
        ),
        hoverinfo="none",
    )

    # --------------------------------------------------------
    # NODES
    # --------------------------------------------------------

    node_x = []
    node_y = []
    node_labels = []
    node_hover = []

    for node in nodes:

        x, y = positions[
            node["id"]
        ]

        node_x.append(x)

        node_y.append(y)

        node_labels.append(
            node["label"]
        )

        node_hover.append(
            f"{node['type']}: "
            f"{node['label']}"
        )

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=node_labels,
        textposition="top center",
        hovertext=node_hover,
        hoverinfo="text",
        marker=dict(
            size=30,
            line=dict(
                width=2
            ),
        ),
    )

    # --------------------------------------------------------
    # FIGURE
    # --------------------------------------------------------

    graph_fig = go.Figure(
        data=[
            edge_trace,
            node_trace,
        ]
    )

    graph_fig.update_layout(
        height=600,
        showlegend=False,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
        ),
        margin=dict(
            l=20,
            r=20,
            t=30,
            b=20,
        ),
    )

    st.plotly_chart(
        graph_fig,
        use_container_width=True,
    )

    st.success(
        "Graph traversal demonstrated: "
        "User → Skill ← Mentor"
    )

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "SkillBridge AI • Graph-powered career networking • CognoDB"
)
