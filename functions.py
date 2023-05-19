# %% packages install
import random

import gspread
import pandas as pd
import streamlit as st
from gsheetsdb import connect
from oauth2client.service_account import ServiceAccountCredentials

# %%
conn = connect()


@st.cache(ttl=300)
def run_query(query):
    '''
    Connect to the Google datasheets database
    and run it
    @st.cache is saving the function so we dont have to connect multiple times during one session
    Input:
    @query as an input

    Qutput:
    @rows return the rows of the Google sheet
    '''
    rows = conn.execute(query, headers=1)
    # rows = rows.fetchall()
    return rows


# %%
def get_dataset_api(sheetname: str):
    # English_sheet for English dataset
    # German_sheet for German dataset
    # Italian_sheet for italian dataset
    '''
    Get the Dataset via API and using the run_query function

    Input:
    @sheetname as string

    Qutput:
    @rows: return the rows of the Google sheet
    '''

    sheet_url = st.secrets["gsheets"][sheetname]
    rows = run_query(f'SELECT * FROM "{sheet_url}"')

    return rows


# %% Update google sheet

class update_google_sheet(object):
    '''
    update the Google sheet

    Input:
    @Dataset as string (Which dataset we would like to update)
    @ID as string (User ID)
    @Gender as string (User input)
    @Index as int (random Index)
    @label as string (User input)
    '''

    def __init__(self, Dataset: str, ID: str, Gender: str, Index: int, label: str):
        self.ID = ID
        self.Gender = Gender
        self.Index = Index
        self.Dataset = Dataset
        self.label = label

    def get_credentials(self):
        '''
        Connect to the API different way because we have to change the Google sheets

        Output:
        @sheet get the wanted sheet
        '''

        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets',
                 ' https://www.googleapis.com/auth/drive.file']

        creds = ServiceAccountCredentials.from_json_keyfile_name('ENTER YOUR JSON FILE HERE WITH YOUR CREDENTIALS',
                                                                 scope)

        client = gspread.authorize(creds)
        sheet = client.open(self.Dataset).sheet1

        return sheet

    def update_sheet(self):
        '''
        Change the Google sheet --> Updated it,  with the User input

        '''
        sheet = self.get_credentials()
        sheet.update_cell((self.Index + 2), 3, self.label)
        sheet.update_cell((self.Index + 2), 5, self.ID)
        sheet.update_cell((self.Index + 2), 6, self.Gender)


# %%
def convert_data_to_pandas(rows) -> pd.DataFrame:
    '''
    Convert the rows that we got from the function above --> @run_query and convert it to a pandas dataframe

    Output:
    @df pandas DataFrame
    '''

    Text_ID_list = [row.Text_ID for row in rows]
    Text_list = [row.Text for row in rows]
    Label_list = [row.Label for row in rows]
    Topic_list = [row.Topic for row in rows]
    Individual_ID_list = [row.Individual_ID for row in rows]
    Gender_list = [row.Gender for row in rows]
    Count_list = [row.Count for row in rows]

    dataset = {'Text_ID': Text_ID_list,
               'Text': Text_list,
               'Label': Label_list,
               'Topic': Topic_list,
               'Individual_ID': Individual_ID_list,
               'Gender': Gender_list,
               'Count': Count_list
               }
    df = pd.DataFrame(dataset)

    return df


# %% get google_sheet
def get_google_sheets(language: str) -> pd.DataFrame:
    '''
    Getting the Google sheets with the given language
    Input:
    @language as string
    Output:
    @Google sheet for the respective language as a dataframe
    '''

    if language == 'German':
        rows = get_dataset_api('German_sheet')
        german_data_sheet = convert_data_to_pandas(rows)
        # german_data = Spread("German_dataset_template", client=client)
        # german_data_sheet = german_data.sheet_to_df().reset_index(drop=True) #to pandas dataframe
        return german_data_sheet
    elif language == 'English':
        rows = get_dataset_api('English_sheet')
        english_data_sheet = convert_data_to_pandas(rows)
        # english_data = Spread("English_dataset_template", client=client)
        # english_data_sheet = english_data.sheet_to_df().reset_index(drop=True) #to pandas dataframe
        return english_data_sheet
    elif language == 'Italian':
        rows = get_dataset_api('Italian_sheet')
        italian_data_sheet = convert_data_to_pandas(rows)
        # italian_data = Spread("Italian_Dataset_Template", client=client)
        # italian_data_sheet = italian_data.sheet_to_df().reset_index(drop=True) #to pandas dataframe
        return italian_data_sheet


# %% Check ID
def generate_random_ID(language: str):
    '''
    Generating a random Id for the User
    Input:
    @language as string

    Output:
    @number as string
    '''

    data = get_google_sheets(language)

    data['Individual_ID'] = data['Individual_ID'].astype(str)

    number = random.randint(1000, 9999)
    number = str(number)
    if data['Individual_ID'].str.contains(number).any():
        new_number = random.randint(1000, 9999)
        new_number = str(new_number)
        return new_number
    else:
        number = str(number)
        return number


def get_data_for_annotation(language: str, number):
    '''
    Get the data for the annotation
    Input:
    @language as string
    @number how many data you would like to have. You have to put a 1 in here to make the code work the
    way it is supposed to.

    Output:
    @conv_string_de returns one random Text for the user
    '''
    data = get_google_sheets(language)

    number_int = int(number)
    get_random_DE = data[data['Count'].isnull()].sample(n=number_int)  # new version
    # get_random_DE = data.query("Count == '' ").sample(n=number_int) #old version
    conv_string_de = get_random_DE['Text']
    # print(conv_string_de)
    return conv_string_de


# %%


def english_page(form, language):
    '''
    Display the sidebar for the english page

    Input:
    @form - tool from streamlit to create a form
    @language selected language of the user saved it session state
    '''

    gender = form.radio(
        "What is your gender ?",
        ('Male', 'Female', 'Diverse'))
    st.session_state['gender'] = gender  # st.session state is storing variables
    st.session_state['language'] = language
    st.session_state['sheet_name'] = 'English_dataset_template'

    number = form.number_input('How much do you wish to annotate? At least 10 texts must be annotated.', min_value=10,
                               max_value=250)
    st.session_state['number'] = number  # stores the number of texts the user wants to label
    start_annotation = form.form_submit_button('Start annotation')

    if start_annotation:
        ID_input = generate_random_ID(language)  # Id of the user
        st.session_state["ID"] = ID_input  # store ID of the user
        st.session_state['annotation_left'] = number
        form.success("Now we can start labeling - Have fun 🥳")


def german_page(form, language):
    '''
    Display the sidebar for the german page

    Input:
    @form - tool from streamlit to create a form
    @language selected language of the user saved it session state
    '''

    gender = form.radio(
        "Was ist dein Geschlecht ?",
        ('Mann', 'Frau', 'Divers'))

    st.session_state['gender'] = gender  # st.session state is storing variables
    st.session_state['language'] = language
    st.session_state['sheet_name'] = 'German_dataset_template'
    number = form.number_input('Wie viele Texte möchtest du annotieren? Mindestens 10 Texte müssen annotiert werden.',
                               min_value=10, max_value=250)
    st.session_state['number'] = number  # stores the number of texts the user wants to label
    start_annotation = form.form_submit_button('Starte die annotation')

    if start_annotation:
        ID_input = generate_random_ID(language)  # Id of the user
        st.session_state["ID"] = ID_input  # store ID of the user
        st.session_state['annotation_left'] = number
        form.success("Jetzt können wir anfangen zu labeln - Viel Spaß 🥳")


def italian_page(form, language):
    '''
    Display the sidebar for the italian page

    Input:
    @form - tool from streamlit to create a form
    @language selected language of the user saved it session state
    '''
    gender = form.radio(
        "What is your gender ?",
        ('Male', 'Female', 'Diverse'))
    st.session_state['gender'] = gender  # st.session state is storing variables
    st.session_state['language'] = language
    st.session_state['sheet_name'] = 'Italian_Dataset_Template'

    number = form.number_input('How much do you wish to annotate? At least 10 texts must be annotated.', min_value=10,
                               max_value=250)
    st.session_state['number'] = number  # stores the number of texts the user wants to label
    start_annotation = form.form_submit_button('Start annotation')

    if start_annotation:
        ID_input = generate_random_ID(language)  # Id of the user
        st.session_state["ID"] = ID_input  # store ID of the user
        st.session_state['annotation_left'] = number
        form.success("Now we can start labeling - Have fun 🥳")


# %%

def text_data_html(text: str) -> str:
    """ HTML scripts to display text to be labelled.

    Input:
    @text as string insert the return text from the function @get_data_for_annotation
    """
    style = """
        border: none;
        border-radius: 5px;
        margin-bottom: 1em;
        padding: 20px;
        height: auto;
        box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    """
    return f"""
        <div style="{style}">
            {text}
        </div>
    """
