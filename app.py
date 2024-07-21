import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")

# Load the data
@st.cache_data
def load_data(file):
    df = pd.read_excel(file)
    df['SAP ID'] = df['SAP ID'].apply(lambda x: f'{x:.0f}')  # Convert SAP ID to string without commas
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

# Creating a list of all subjects columns
subjects = [col for col in data.columns if 'Subject' in col]
all_subjects = data[subjects].values.flatten()
unique_subjects = list(set(all_subjects))

subject = st.sidebar.multiselect('Subject', options=unique_subjects)

# Apply filters
filtered_data = data

if roll_no:
    filtered_data = filtered_data[filtered_data['Roll No'].isin(roll_no)]

if sap_id:
    filtered_data = filtered_data[filtered_data['SAP ID'].isin(sap_id)]

if name:
    filtered_data = filtered_data[filtered_data['Name'].isin(name)]

if branch:
    filtered_data = filtered_data[filtered_data['Branch'].isin(branch)]

if campus:
    filtered_data = filtered_data[filtered_data['Campus'].isin(campus)]

if major:
    filtered_data = filtered_data[filtered_data['Major'].isin(major)]

if division:
    filtered_data = filtered_data[filtered_data['Division'].isin(division)]

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


st.write(filtered_data[columns_to_show])


# Add charts
st.header("Data Visualization")

# Drop rows with 'Unknown' in any column
filtered_data = filtered_data.replace('Unknown', pd.NA).dropna()

# Layout for charts: 3 charts per row with space between them
fig, axs = plt.subplots(2, 3, figsize=(20, 10))
# fig.tight_layout(pad=5.0)
fig.subplots_adjust(hspace=0.525, wspace=0.125)

# Chart 1: Distribution of students across branches
sns.countplot(data=filtered_data, x='Branch', ax=axs[0, 0])
axs[0, 0].set_title('Distribution of Students Across Branches')
axs[0, 0].tick_params(axis='x', rotation=90)

# Chart 2: Distribution of students across campuses
sns.countplot(data=filtered_data, x='Campus', ax=axs[0, 1])
axs[0, 1].set_title('Distribution of Students Across Campuses')
axs[0, 1].tick_params(axis='x', rotation=90)

# Chart 3: Distribution of students across majors
sns.countplot(data=filtered_data, x='Major', ax=axs[0, 2])
axs[0, 2].set_title('Distribution of Students Across Majors')
axs[0, 2].tick_params(axis='x', rotation=90)

# Chart 4: Subject enrollment count
subject_counts = filtered_data[subjects].melt(var_name='Subject Column', value_name='Subject').dropna()
top_subjects = subject_counts['Subject'].value_counts().nlargest(20).index  # Top 20 subjects
sns.countplot(data=subject_counts[subject_counts['Subject'].isin(top_subjects)], y='Subject', order=top_subjects, ax=axs[1, 0])
axs[1, 0].set_title('Top 20 Subject Enrollment Count')

# Chart 5: Count of students per branch and campus
sns.countplot(data=filtered_data, x='Branch', hue='Campus', ax=axs[1, 1])
axs[1, 1].set_title('Count of Students per Branch and Campus')
axs[1, 1].tick_params(axis='x', rotation=90)

# Chart 6: Count of students per branch and major
sns.countplot(data=filtered_data, x='Branch', hue='Major', ax=axs[1, 2])
axs[1, 2].set_title('Count of Students per Branch and Major')
axs[1, 2].tick_params(axis='x', rotation=90)

# Hide unused subplots
axs[1, 2].axis('off')

# Display charts
st.pyplot(fig)
