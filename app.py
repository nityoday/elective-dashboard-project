import streamlit as st
import pandas as pd
from streamlit_extras.colored_header import colored_header
from streamlit_extras.let_it_rain import rain

st.set_page_config(layout="wide")

@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    df['SAP ID'] = df['SAP ID'].apply(lambda x: f'{x:.0f}')  # Convert SAP ID to string without commas
    df = df.drop(columns=['Subject 1', 'Subject 2','Subject 3'])
    return df

data = load_data('student_electives.xlsx')

# Sidebar filters
st.sidebar.header('Choose Filters')
branch = st.sidebar.multiselect('Branch', options=data['Branch'].unique())
campus = st.sidebar.multiselect('Campus', options=data['Campus'].unique())
major = st.sidebar.multiselect('Major', options=data['Major'].unique())
division = st.sidebar.multiselect('Division', options=data['Division'].unique())
st.sidebar.write('Find by Identity Filters')
roll_no = st.sidebar.multiselect('Roll No', options=data['Roll No'].unique())
sap_id = st.sidebar.multiselect('SAP ID', options=data['SAP ID'].unique())
name = st.sidebar.multiselect('Name', options=data['Name'].unique())

include_mandatory_subjects = st.sidebar.checkbox(
    'Include Mandatory Subjects',
    value=False,
    help='Includes mandatory subjects for all students in the data',
    key='include_mandatory_subjects',
    disabled = True
) # Disabled for now. May include later with respect to dropping columns Subject 1,2,3

filtered_data = data

subjects = [col for col in data.columns if 'Subject' in col]
all_subjects = data[subjects].values.flatten()
unique_subjects = list(set(all_subjects))

subject = st.sidebar.multiselect('Subject', options=unique_subjects)

filter_dict = {
    'Roll No': roll_no,
    'SAP ID': sap_id,
    'Name': name,
    'Branch': branch,
    'Campus': campus,
    'Major': major,
    'Division': division
}

# Apply filters dynamically
# filtered_data = data.copy()

for column, values in filter_dict.items():
    if values:
        filtered_data = filtered_data[filtered_data[column].isin(values)]

if subject:
    subject_filter = filtered_data[subjects].apply(lambda row: any(subj in subject for subj in row), axis=1)
    filtered_data = filtered_data[subject_filter]

st.sidebar.header('Columns to Display')
show_roll_no = st.sidebar.checkbox('Roll No', value=True)
show_sap_id = st.sidebar.checkbox('SAP ID', value=True)
show_name = st.sidebar.checkbox('Name', value=True)
show_branch = st.sidebar.checkbox('Branch', value=True)
show_campus = st.sidebar.checkbox('Campus', value=True)
show_major = st.sidebar.checkbox('Major', value=True)
show_division = st.sidebar.checkbox('Division', value=True)
show_all_subjects = st.sidebar.checkbox('Subjects', value=True)

columns_to_show = []
if show_roll_no:
    columns_to_show.append('Roll No')
if show_sap_id:
    columns_to_show.append('SAP ID')
if show_name:
    columns_to_show.append('Name')
if show_branch:
    columns_to_show.append('Branch')
if show_campus:
    columns_to_show.append('Campus')
if show_major:
    columns_to_show.append('Major')
if show_division:
    columns_to_show.append('Division')
if show_all_subjects:
    columns_to_show.extend(subjects)

st.dataframe(filtered_data[columns_to_show], hide_index=True)

colored_header(
        label="Data Visualization",
        description="The charts will update as you update filters",
        color_name="violet-70",
    )

filtered_data = filtered_data.replace('Unknown', pd.NA).dropna()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader('Distribution of Students Across Branches')
    branch_counts = filtered_data['Branch'].value_counts().sort_index()
    st.bar_chart(branch_counts, use_container_width=True)

with col2:
    st.subheader('Distribution of Students Across Campuses')
    campus_counts = filtered_data['Campus'].value_counts().sort_index()
    st.bar_chart(campus_counts, use_container_width=True)

with col3:
    st.subheader('Distribution of Students Across Majors')
    major_counts = filtered_data['Major'].value_counts().sort_index()
    st.bar_chart(major_counts, use_container_width=True)

st.subheader('Top 20 Subject Enrollment Distribution')
subject_counts = filtered_data[subjects].melt(var_name='Subject Column', value_name='Subject').dropna()
top_subjects = subject_counts['Subject'].value_counts().nlargest(20).sort_values(ascending=False)
top_subjects_df = top_subjects.reset_index()
top_subjects_df.columns = ['Subject', 'Number of Students']
top_subjects_df = top_subjects_df.sort_values(by='Number of Students', ascending=False)

top_subjects_chart_data = top_subjects_df.set_index('Subject')['Number of Students']
st.bar_chart(top_subjects_chart_data, use_container_width=True)

st.subheader('Least 10 Subject Enrollment Count Distribution')
least_subjects = subject_counts['Subject'].value_counts().nsmallest(10).sort_values()
least_subjects_df = least_subjects.reset_index()
least_subjects_df.columns = ['Subject', 'Number of Students']
least_subjects_df = least_subjects_df.sort_values(by='Number of Students', ascending=True)

least_subjects_chart_data = least_subjects_df.set_index('Subject')['Number of Students']
st.bar_chart(least_subjects_chart_data, use_container_width=True)

col4, col5 = st.columns(2)

with col4:
    st.subheader('Count of Students per Branch and Campus')
    branch_campus_counts = filtered_data.groupby(['Branch', 'Campus']).size().unstack().fillna(0)
    st.bar_chart(branch_campus_counts, use_container_width=True)

with col5:
    st.subheader('Count of Students per Branch and Major')
    branch_major_counts = filtered_data.groupby(['Branch', 'Major']).size().unstack().fillna(0)
    st.bar_chart(branch_major_counts, use_container_width=True)


# def plot_with_rotated_labels(data, title):
#     fig, ax = plt.subplots()
#     data.plot(kind='bar', ax=ax)
#     ax.set_title(title)
#     plt.xticks(rotation=45, ha='right')
#     st.pyplot(fig)

# st.subheader('Top 20 Subject Enrollment Count (Adjusted Labels)')
# plot_with_rotated_labels(top_subjects, 'Top 20 Subject Enrollment Count')

# st.subheader('Least 10 Subject Enrollment Count (Adjusted Labels)')
# plot_with_rotated_labels(least_subjects, 'Least 10 Subject Enrollment Count')

st.markdown(
    """
    <div style="text-align: right;">
        <p style="font-size: 16px; color: #666666; font-family: 'Arial', sans-serif;">
           ✨ Bringing ideas to life, by <strong>Nityoday Tekchandani</strong>.
        </p>
        <!--
        <a href="https://github.com/nityoday/elective-dashboard-project" target="_blank" style="text-decoration: none;">
            <button style="font-size: 14px; padding: 10px 20px; color: #ffffff; background-color: #007BFF; border: none; border-radius: 5px; cursor: pointer;">
                Feel free to contribute to this project :)
            </button>
        </a>
        -->
    </div>
    """,
    unsafe_allow_html=True
)

if st.button("Feel free to contribute to this project :) "):
    st.markdown('<a href="https://github.com/nityoday/elective-dashboard-project" target="_blank" style="text-decoration: none; color: #007BFF; font-size: 22px;">View this project on GitHub</a>', unsafe_allow_html=True)
    rain(
        emoji="🌟",
        font_size=24,
        falling_speed=3,
        animation_length=2,
    )

# possible future feature inclusions:
# https://arnaudmiribel.github.io/streamlit-extras/extras/altex/
# https://arnaudmiribel.github.io/streamlit-extras/extras/app_logo/