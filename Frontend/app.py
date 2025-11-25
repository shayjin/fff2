import streamlit as st
import requests
import time
import datetime
import os

# page config
st.set_page_config(page_title="Health Buddy", layout="wide", page_icon="🩺")

# Get API URL from environment variable, default to localhost for local development
API_BASE = os.getenv("API_BASE_URL", "https://s-aof7.onrender.com")

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stTabs [role="tablist"] {
        justify-content: center;
    }
</style>
""", unsafe_allow_html=True)

if "patient_id" not in st.session_state:
    st.session_state.patient_id = None
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "tab_data" not in st.session_state:
    st.session_state.tab_data = {
        "conditions": None,
        "meds": None,
        "labs": None,
        "summary": None
    }

st.markdown("""
<div class="main-header">
    <h1>🩺 Health Buddy</h1>
    <p style="opacity: 0.9; margin: 0;">AI-Powered Medical Assistant</p>
</div>
""", unsafe_allow_html=True)

if not st.session_state.patient_id:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("Welcome! Login to view your records or create a new profile.")

        login_tab, create_tab = st.tabs(["🔑 Existing Patient", "📝 Create New Patient"])

        with login_tab:
            with st.form("login_form"):
                st.subheader("Access Your Records")
                p_id_input = st.text_input("Enter Patient ID", placeholder="e.g., 12345")
                submitted = st.form_submit_button("Login", use_container_width=True)

                if submitted:
                    if not p_id_input.strip():
                        st.error("Please enter a valid ID.")
                    else:
                        with st.spinner("Connecting to server..."):
                            try:
                                r = requests.post(
                                    f"{API_BASE}/patient",
                                    json={"patient_id": p_id_input},
                                    timeout=5
                                )

                                if r.status_code == 200:
                                    st.session_state.tab_data = {k: None for k in st.session_state.tab_data}
                                    st.session_state.chat_history = []
                                    st.session_state.patient_id = p_id_input
                                    st.success(f"Logged in as {p_id_input}")
                                    time.sleep(0.5)
                                    st.rerun()
                                else:
                                    st.error(f"Server Error: {r.status_code}")
                            except requests.exceptions.ConnectionError:
                                st.error("Cannot connect to backend.")
                            except Exception as e:
                                st.error(f"Error: {e}")

        with create_tab:
            with st.form("create_patient_form"):
                st.subheader("Create Comprehensive Profile")
                st.caption("The AI will generate the FHIR records for you.")

                c_first, c_last = st.columns(2)
                with c_first:
                    given_name = st.text_input("First Name")
                with c_last:
                    family_name = st.text_input("Last Name")

                c_gender, c_dob = st.columns(2)
                with c_gender:
                    gender = st.selectbox("Gender", ["male", "female", "other", "unknown"])
                with c_dob:
                    birth_date = st.date_input("Date of Birth", min_value=datetime.date(1900, 1, 1))

                st.markdown("---")
                st.caption("Optional Medical History")
                conditions_input = st.text_area("Conditions", placeholder="e.g. Diabetes, etc")
                meds_input = st.text_area("Medications", placeholder="e.g. Insulin, Lisinopril")
                labs_input = st.text_area("Lab Results", placeholder="e.g. Glucose 140 mg/dL")

                create_submitted = st.form_submit_button("Create Patient Record", use_container_width=True)

                if create_submitted:
                    if not given_name or not family_name:
                        st.error("Name is required.")
                    else:
                        prompt = (
                            f"Perform the following steps sequentially:\n"
                            f"1. Create a new patient in the FHIR server. Name: {given_name} {family_name}, Gender: {gender}, DOB: {birth_date}.\n"
                        )
                        if conditions_input.strip():
                            prompt += f"2. Create active Conditions: {conditions_input}.\n"
                        if meds_input.strip():
                            prompt += f"3. Create active MedicationRequests: {meds_input}.\n"
                        if labs_input.strip():
                            prompt += f"4. Create Observations (Labs): {labs_input}.\n"

                        prompt += "5. IMPORTANT: Final response must include the new Patient ID."

                        with st.spinner("AI is working right now..."):
                            try:
                                r = requests.post(
                                    f"{API_BASE}/ask",
                                    json={"query": prompt},
                                    timeout=90
                                )
                                if r.status_code == 200:
                                    data = r.json()
                                    st.success("Process Complete!")
                                    st.info(data.get("answer", ""))
                                    st.warning("Please copy the ID above and switch to the Login tab.")
                                else:
                                    st.error(f"Failed. Server Code: {r.status_code}")
                            except Exception as e:
                                st.error(f"Connection Error: {e}")
    st.stop()

st.success(f"🟢 **Active Session:** Patient `{st.session_state.patient_id}`")

def fetch_tab_data(key, query_text, force_refresh=False):
    if force_refresh or st.session_state.tab_data[key] is None:
        with st.spinner(f"AI is retrieving {key}..."):
            try:
                r = requests.post(f"{API_BASE}/ask", json={"query": query_text}, timeout=60)
                if r.status_code == 200:
                    st.session_state.tab_data[key] = r.json().get("answer", "No info found.")
                else:
                    st.session_state.tab_data[key] = "Error fetching data."
            except:
                st.session_state.tab_data[key] = "onnection Error."
    return st.session_state.tab_data[key]

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🩺 Conditions",
    "💊 Meds",
    "🧪 Labs",
    "📊 Summary",
    "➕ Add Data"
])

with tab1:
    st.subheader("Medical Conditions")
    if st.session_state.tab_data["conditions"] is None:
        if st.button("Load Conditions", key="load_conditions"):
            fetch_tab_data("conditions", "List my active medical conditions in a clean bulleted list.", force_refresh=True)
            st.rerun()
        st.info("Click to load your conditions")
    else:
        st.markdown(st.session_state.tab_data["conditions"])

with tab2:
    st.subheader("Medications")
    if st.session_state.tab_data["meds"] is None:
        if st.button("Load Medications", key="load_meds"):
            fetch_tab_data("meds", "What medications am I currently taking? List them with dosage.", force_refresh=True)
            st.rerun()
        st.info("Click to load your medications")
    else:
        st.markdown(st.session_state.tab_data["meds"])

with tab3:
    st.subheader("Lab Results")
    if st.session_state.tab_data["labs"] is None:
        if st.button("Load Lab Results", key="load_labs"):
            fetch_tab_data("labs", "Summarize my recent lab results and observations.", force_refresh=True)
            st.rerun()
        st.info("Click to load your lab results")
    else:
        st.markdown(st.session_state.tab_data["labs"])

with tab4:
    st.subheader("Health Summary")
    if st.session_state.tab_data["summary"] is None:
        if st.button("Load Summary", key="load_summary"):
            fetch_tab_data("summary", "Give me a comprehensive summary of my health status.", force_refresh=True)
            st.rerun()
        st.info("Click to load your health summary")
    else:
        st.markdown(st.session_state.tab_data["summary"])

with tab5:
    st.subheader("📝 Add to Medical Record")
    st.caption("Use the AI Agent to update your FHIR records.")

    with st.form("add_data_form"):
        st.markdown("**General Note & Upload**")

        clinical_note = st.text_area("Type Clinical Note", placeholder="e.g., Patient visited Dr. K today...")
        uploaded_file = st.file_uploader("Or upload a text document (.txt)", type=["txt"])

        st.markdown("---")
        st.markdown("**Specific Updates** (Leave empty if not adding anything)")

        col_a, col_b = st.columns(2)
        with col_a:
            new_cond = st.text_input("Add Condition(s)", placeholder="e.g., Fibrosis")
            new_med = st.text_input("Add Medication(s)", placeholder="e.g., Amoxicillin 500mg")
        with col_b:
            new_lab = st.text_input("Add Lab Result", placeholder="e.g., Body Weight 150lbs")

        submit_update = st.form_submit_button("Update Records", use_container_width=True)

    if submit_update:
        file_content = ""
        if uploaded_file is not None:
            try:
                file_content = uploaded_file.read().decode("utf-8")
            except Exception as e:
                st.error(f"Error reading file: {e}")

        if not (clinical_note or file_content or new_cond or new_med or new_lab):
            st.error("Please enter text, upload file, or fill in specific fields.")
        else:
            prompt = f"Update the records for the current patient.\n"

            if clinical_note:
                prompt += f"Note Context: {clinical_note}\n"

            if file_content:
                prompt += f"Uploaded Document Content:\n---\n{file_content}\n---\n(Extract relevant medical info from the document above and update records accordingly)\n"

            if new_cond:
                prompt += f"Action: Create a new Condition resource for '{new_cond}'.\n"
            if new_med:
                prompt += f"Action: Create a new MedicationRequest resource for '{new_med}'.\n"
            if new_lab:
                prompt += f"Action: Create a new Observation resource for '{new_lab}'.\n"

            prompt += "Confirm clearly what was created or updated in the system based on these inputs."

            with st.spinner("AI is reading and updating your records..."):
                try:
                    r = requests.post(f"{API_BASE}/ask", json={"query": prompt}, timeout=60)
                    if r.status_code == 200:
                        st.success("Update Successful!")
                        st.markdown(r.json().get("answer", ""))
                        st.session_state.tab_data = {k: None for k in st.session_state.tab_data}
                        st.info("Data tabs have been reset. Click them to see updated info.")
                    else:
                        st.error(f"Update failed: {r.status_code}")
                except Exception as e:
                    st.error(f"Error: {e}")

st.divider()
st.subheader("💬 Chat with your Health Data")
st.caption("Ask questions like: 'How is my overall health?' or 'Are my medications making sense?'")

for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"], unsafe_allow_html=True)

user_input = st.chat_input("Type your question here.")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})

    with st.spinner("🤔Thinking..."):
        try:
            response = requests.post(
                f"{API_BASE}/ask",
                json={"query": user_input},
                timeout=60
            )

            data = response.json()

            if response.status_code != 200:
                answer = f"Server returned error {response.status_code}"
            elif "error" in data:
                answer = f"Backend error: {data['error']}"
            else:
                answer = data.get("answer", "No response from server")
                accuracy = data.get("accuracy_score")
                if accuracy is not None:
                    answer += f"\n\n*(Answer confidence: {accuracy})*"

        except requests.exceptions.ConnectionError:
            answer = "Cannot reach backend API."
        except requests.exceptions.Timeout:
            answer = "Request timed out after 60 seconds."
        except Exception as e:
            answer = f"Error: {str(e)}"

    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    st.rerun()

with st.sidebar:
    st.write(f"Logged in as: **{st.session_state.patient_id}**")
    if st.button("🚪 Logout", type="primary"):
        try:
            requests.delete(f"{API_BASE}/patient")
        except:
            pass
        st.session_state.patient_id = None
        st.session_state.chat_history = []
        st.session_state.tab_data = {k: None for k in st.session_state.tab_data}

        st.rerun()
