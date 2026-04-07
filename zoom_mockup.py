import streamlit as st
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Zoom AI: Standup Synthesizer",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Custom Zoom Styling ---
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;700;900&display=swap');
        
        .stApp { background-color: #FFFFFF !important; }
        
        .stApp, .stApp p, .stApp label, div[data-testid="stMarkdownContainer"] {
            color: #0F172A !important;
            font-family: 'Lato', sans-serif !important;
        }
        
        .stApp h1, .stApp h2, .stApp h3 {
            color: #232333 !important;
            font-family: 'Lato', sans-serif !important;
            font-weight: 700 !important;
        }
        
        /* Unified Button Heights and Alignment */
        .stButton>button {
            min-height: 54px !important;
            display: flex;
            align-items: center;
            justify-content: center;
            line-height: 1.2;
        }
        
        /* Default Primary Buttons (Zoom Blue) */
        .stButton>button[kind="primary"] {
            background-color: #0B5CFF !important;
            color: white !important;
            border-radius: 8px; border: none; font-weight: 700; padding: 0.5rem 1rem;
        }
        .stButton>button[kind="primary"] * { color: white !important; }
        .stButton>button[kind="primary"]:hover { background-color: #094bce !important; }
        
        /* Secondary Buttons */
        .stButton>button[kind="secondary"] {
            background-color: transparent !important;
            color: #0B5CFF !important;
            border: 2px solid #0B5CFF !important;
            border-radius: 8px; font-weight: 700; padding: 0.5rem 1rem;
        }
        .stButton>button[kind="secondary"] * { color: #0B5CFF !important; }
        .stButton>button[kind="secondary"]:hover { background-color: #F0F4FF !important; }
        
        /* Tertiary Buttons (Expander Arrows) */
        .stButton>button[kind="tertiary"] {
            background-color: transparent !important; color: #64748B !important; border: none !important; padding: 0 !important;
            font-size: 1.2rem; min-height: auto !important; 
        }
        .stButton>button[kind="tertiary"]:hover { color: #0B5CFF !important; background-color: transparent !important; }
        
        /* Vertical Divider for Main Columns */
        div[data-testid="stElementContainer"]:has(.main-columns-wrapper) + div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) {
            border-right: 1px solid #E2E8F0;
            padding-right: 2.5rem;
        }
        
        /* Custom Target for the Orange CTA Button (Applied outside the column to prevent misalignment) */
        div[data-testid="stElementContainer"]:has(.action-buttons-wrapper) + div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) button {
            background-color: #f26d21 !important;
            border-color: #f26d21 !important;
            color: white !important;
        }
        div[data-testid="stElementContainer"]:has(.action-buttons-wrapper) + div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) button:hover {
            background-color: #d95e1a !important;
            border-color: #d95e1a !important;
        }
        
        /* Radio Toggle Alignment Fix */
        div[data-testid="stRadio"] {
            margin-top: -15px;
        }
        div[data-testid="stRadio"] > div {
            justify-content: flex-end;
        }
        
        /* Tags & Text */
        .source-tag {
            background-color: #F0F4FF; color: #0B5CFF !important; padding: 3px 10px;
            border-radius: 12px; font-size: 0.8em; font-weight: 700; display: inline-block; margin-right: 12px;
        }
        .source-desc { color: #475569 !important; font-size: 0.95em; }
        .item-heading { font-size: 1.1em; font-weight: 700; color: #232333; margin-bottom: 8px; display: inline-block;}
        
        /* Expanded Details */
        .expanded-text {
            color: #64748B !important; font-size: 0.9em; line-height: 1.5; margin-top: 12px; padding-left: 12px; border-left: 2px solid #E2E8F0;
        }
        
        /* Tooltip */
        .custom-tooltip { position: relative; display: inline-block; cursor: help; margin-left: 6px; }
        .custom-tooltip .tooltiptext {
            visibility: hidden; width: max-content; background-color: #232333; color: #FFFFFF !important;
            text-align: center; border-radius: 6px; padding: 6px 12px; position: absolute; z-index: 100;
            bottom: 130%; left: 50%; transform: translateX(-50%); opacity: 0; transition: opacity 0.2s;
            font-size: 0.75rem; font-family: 'Lato', sans-serif; box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        }
        .custom-tooltip .tooltiptext::after {
            content: ""; position: absolute; top: 100%; left: 50%; margin-left: -5px;
            border-width: 5px; border-style: solid; border-color: #232333 transparent transparent transparent;
        }
        .custom-tooltip:hover .tooltiptext { visibility: visible; opacity: 1; }
        
        /* Mock Video Interface */
        .video-feed-mock {
            background-color: #1E1E2D; height: 400px; border-radius: 12px; position: relative; overflow: hidden;
            display: flex; align-items: center; justify-content: center; color: #64748B; font-weight: 700;
        }
        .teleprompter-overlay {
            position: absolute; bottom: 20px; right: 20px; width: 350px; height: 180px;
            background: rgba(15, 23, 42, 0.85); backdrop-filter: blur(8px); border-radius: 8px;
            padding: 16px; overflow: hidden; border: 1px solid rgba(255,255,255,0.1);
        }
        .scrolling-text {
            color: #FFFFFF; font-size: 1.1em; line-height: 1.6; font-weight: 500;
            animation: scrollUp 20s linear infinite; text-align: left;
        }
        @keyframes scrollUp {
            0% { transform: translateY(180px); }
            100% { transform: translateY(-100%); }
        }
        
        /* Mock Mail Interface */
        .mail-feed-mock {
            background-color: #F8FAFC; border-radius: 12px; padding: 24px; border: 1px solid #E2E8F0;
            color: #0F172A; font-family: 'Lato', sans-serif; font-size: 1.05em; line-height: 1.6;
        }
        .mail-header { border-bottom: 1px solid #E2E8F0; padding-bottom: 16px; margin-bottom: 16px; }
        .mail-field { margin-bottom: 8px; }
        .mail-label { font-weight: 700; color: #64748B; width: 80px; display: inline-block; }
    </style>
""", unsafe_allow_html=True)

# --- Mock Data Initialization ---
if 'tasks' not in st.session_state:
    st.session_state.tasks = [
        {"id": 1, "title": "Update AI Companion PRD", "desc": "Added the section on agentic routing and MCP.", "details": "Pending final review from the security architecture team.<br>ETA for sign-off is EOD Thursday.", "type": "Zoom Docs", "people": True, "names": "Alice and Bob", "selected": True, "expanded": False},
        {"id": 2, "title": "Blocker Discussion", "desc": "Chatted with engineering regarding API limits.", "details": "Explored alternative rate-limiting strategies.<br>Charlie is drafting the revised technical spec.", "type": "Zoom Team Chat", "people": True, "names": "Charlie from Engineering", "selected": True, "expanded": False},
        {"id": 3, "title": "User Journey Mapping", "desc": "Drafted the flow for the new auto-ticket agent.", "details": "Includes edge cases for failed third-party authentication.<br>Need the design team to review the wireframes.", "type": "Zoom Whiteboard", "people": False, "names": "", "selected": False, "expanded": False},
        {"id": 4, "title": "Client Sync: Aaron Co.", "desc": "Held a discovery call regarding enterprise deployment.", "details": "They requested an integration with their custom internal CRM.<br>Budget is approved for Q3 rollout.", "type": "Zoom Calendar", "people": True, "names": "Sarah (Sales)", "selected": True, "expanded": False},
    ]

# State variables for actions
if 'action_taken' not in st.session_state:
    st.session_state.action_taken = None
if 'current_script' not in st.session_state:
    st.session_state.current_script = ""

# --- Modal Dialogs ---
@st.dialog("Add Workspace Sources")
def add_sources_modal():
    workspace = st.selectbox("Select Workspace", ["Zoom Team Chat", "Zoom Docs", "Zoom Mail", "Zoom Calendar", "Zoom Whiteboard"])
    search_query = st.text_input("Search query...", placeholder="e.g., Q3 roadmap")
    if st.button("Retrieve Context", type="primary"):
        with st.spinner("Searching workspace..."):
            time.sleep(1)
            st.session_state.tasks.append({
                "id": len(st.session_state.tasks) + 1, "title": f"Search Result for '{search_query}'", "desc": f"Context pulled dynamically from {workspace}.", "details": "Dynamic retrieval successful.<br>Ready to be included in standup.", "type": workspace, "people": False, "names": "", "selected": True, "expanded": False
            })
            st.success("Context added to standup queue!")
            time.sleep(1)
            st.rerun()

@st.dialog("Meeting in Progress", width="large")
def join_standup_modal():
    clean_script = st.session_state.current_script.replace("**", "").replace("\n", "<br><br>")
    st.markdown(f"""
        <div class="video-feed-mock">
            <span>🎥 Waiting for others to turn on cameras...</span>
            <div class="teleprompter-overlay">
                <div class="scrolling-text">{clean_script}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    st.caption("Your generated script is scrolling in the teleprompter overlay on the bottom right.")

@st.dialog("Draft Email Update", width="large")
def send_mail_modal():
    selected_people = [t['names'] for t in st.session_state.tasks if t['selected'] and t['people']]
    teammates = ", ".join(selected_people) if selected_people else "Product Team"
    
    intro_text = "Hey team, I won't be able to make it to the standup call today, so I'm dropping my updates here asynchronously.<br><br>"
    clean_script = intro_text + st.session_state.current_script.replace("**", "").replace("\n", "<br>")
    
    st.markdown(f"""
        <div class="mail-feed-mock">
            <div class="mail-header">
                <div class="mail-field"><span class="mail-label">To:</span> {teammates}</div>
                <div class="mail-field"><span class="mail-label">Subject:</span> Asynchronous Standup Updates</div>
            </div>
            <div class="mail-body">
                {clean_script}
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    col1, col2 = st.columns([0.8, 0.2])
    with col2:
        if st.button("Send ✨", type="primary", use_container_width=True):
            st.success("Sent!")
            time.sleep(1)
            st.session_state.action_taken = None
            st.rerun()

# --- Main App Layout ---
st.title("✨ Standup Synthesizer")
st.markdown("Product standup in 15m. Choose which updates you'd like to share, and I'll generate a live script for you.")
st.divider()

# Inject the wrapper class BEFORE the columns so we can natively add the vertical border to the first column
st.markdown('<div class="main-columns-wrapper" style="display:none;"></div>', unsafe_allow_html=True)
col_left, col_main = st.columns([1.3, 1.9], gap="large")

# --- LEFT COLUMN: Context Selection ---
with col_left:
    st.subheader("Tasks since last standup")
    
    for index, task in enumerate(st.session_state.tasks):
        with st.container():
            chk_col, txt_col, exp_col = st.columns([0.08, 0.84, 0.08], vertical_alignment="center")
            
            with chk_col:
                is_checked = st.checkbox("", value=task["selected"], key=f"chk_{task['id']}")
                if is_checked != task["selected"]:
                    st.session_state.action_taken = None
                st.session_state.tasks[index]["selected"] = is_checked
                
            with txt_col:
                people_icon = f'<span class="custom-tooltip">👥<span class="tooltiptext">This item relates to {task["names"]} in the call</span></span>' if task["people"] else ""
                
                st.markdown(f"""
                    <div>
                        <span class="item-heading">{task['title']}</span>{people_icon}<br>
                        <span class="source-tag">{task['type']}</span> <span class="source-desc">{task['desc']}</span>
                    </div>
                """, unsafe_allow_html=True)
                
                if task["expanded"]:
                    st.markdown(f"<div class='expanded-text'>{task['details']}</div>", unsafe_allow_html=True)
            
            with exp_col:
                button_label = "∧" if task["expanded"] else "∨"
                if st.button(button_label, key=f"exp_btn_{task['id']}", type="tertiary"):
                    st.session_state.tasks[index]["expanded"] = not task["expanded"]
                    st.rerun()

            st.markdown("<hr style='margin: 12px 0px; opacity: 0.2;'>", unsafe_allow_html=True)

    if st.button("➕ Add Sources", use_container_width=True, type="secondary"):
        add_sources_modal()

# --- MAIN COLUMN: Teleprompter ---
with col_main:
    header_col, toggle_col = st.columns([0.6, 0.4], vertical_alignment="bottom")
    with header_col:
        st.subheader("Your Standup Script")
    with toggle_col:
        verbosity = st.radio("Verbosity", ["Brief", "Detailed"], horizontal=True, label_visibility="collapsed")
    
    selected_items = [t for t in st.session_state.tasks if t["selected"]]
    
    if not selected_items:
        st.info("Please select at least one context item from the left to generate your script.")
    else:
        if verbosity == "Brief":
            script_text = "**Hey team, here are my quick updates.**\n\n"
            script_text += "Yesterday, I mainly focused on "
            titles = [f"**{t['title']}**" for t in selected_items]
            if len(titles) == 1:
                script_text += f"{titles[0]}."
            elif len(titles) == 2:
                script_text += f"{titles[0]} and {titles[1]}."
            else:
                script_text += f"{', '.join(titles[:-1])}, and {titles[-1]}."
        else:
            script_text = "**Hey team, here's what I've been working on.**\n\n"
            for i, t in enumerate(selected_items):
                clean_details = t['details'].replace('<br>', ' ').strip()
                if i == 0:
                    script_text += f"First off, I spent some time on the **{t['title']}**. I {t['desc'].lower()} "
                elif i == len(selected_items) - 1 and len(selected_items) > 1:
                    script_text += f"Finally, for the **{t['title']}**, I {t['desc'].lower()} "
                else:
                    script_text += f"I also looked into the **{t['title']}**. I {t['desc'].lower()} "
                
                if t['expanded'] or len(selected_items) < 3:
                    script_text += f"{clean_details} "
                script_text += "\n\n"

        script_text += "\n\nToday, I'll be focusing on bridging these workflows into our new prototype. "
        
        people_items = [t for t in selected_items if t["people"]]
        if people_items:
            target_person = people_items[0]["names"].split(" ")[0] 
            script_text += f"\n\n**@{target_person}**, regarding the {people_items[0]['title']}, do we have the green light to push that to staging today?"
        else:
            script_text += f"\n\nDoes anyone have blockers I can help clear?"
        
        st.session_state.current_script = script_text
        st.success(script_text, icon="🎙️")
        
        st.markdown("<div style='color: #94A3B8; font-size: 0.85em; margin-top: -10px; margin-bottom: 24px; padding-left: 5px;'>Always check AI generated text for mistakes.</div>", unsafe_allow_html=True)
        
        if st.session_state.action_taken is None:
            # Inject CSS hook before columns to prevent interior button misalignment
            st.markdown('<div class="action-buttons-wrapper" style="display:none;"></div>', unsafe_allow_html=True)
            btn_col1, btn_col2 = st.columns(2)
            
            with btn_col1:
                if st.button("**Ready? Link script and join standup**", type="primary", use_container_width=True):
                    st.session_state.action_taken = 'join'
                    st.rerun()
            with btn_col2:
                if st.button("**Won't be joining? Send updates over mail**", type="secondary", use_container_width=True):
                    st.session_state.action_taken = 'mail'
                    st.rerun()
        else:
            status_placeholder = st.empty()
            if st.session_state.action_taken == 'join':
                st.balloons()
                for i in range(5, 0, -1):
                    status_placeholder.success(f"✅ Script successfully linked. Joining the meeting in **{i}**...")
                    time.sleep(1)
                status_placeholder.success("✅ Script successfully linked. Meeting in progress.")
                join_standup_modal()
                
            elif st.session_state.action_taken == 'mail':
                for i in range(5, 0, -1):
                    status_placeholder.success(f"✅ Updates formatted. Opening mail client in **{i}**...")
                    time.sleep(1)
                status_placeholder.success("✅ Draft ready to review and send.")
                send_mail_modal()