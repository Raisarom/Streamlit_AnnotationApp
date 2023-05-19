import random

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
from streamlit_option_menu import option_menu

from functions import italian_page, german_page, english_page, get_data_for_annotation
from functions import text_data_html, get_sql_data_pd, update_sql_database_ger, \
    update_sql_database_en, update_sql_database_it

st.set_page_config(page_title="Hate speech", page_icon=":speech_balloon:", layout="centered")
# %% Navigation bar
selected = option_menu(
    menu_title=None,
    options=["Home", "Annotation", "Interview"],
    icons=["house-heart", "ui-checks", "question-square"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
)

# %% Homepage
if selected == "Home":
    # get data from excel API
    # german_data = get_google_sheets('German')
    # english_data = get_google_sheets('English')
    # italian_data = get_google_sheets('Italian')

    # get data from SQL databases
    german_data = get_sql_data_pd('German')
    english_data = get_sql_data_pd('English')
    italian_data = get_sql_data_pd('Italian')

    with st.container():
        # size of the Datasets old version
        # de_size = len(german_data.query("Count == '' "))
        # en_size = len(english_data.query("Count == '' "))
        # it_size = len(italian_data.query("Count == '' "))

        # new version
        de_size = len(german_data[german_data['Count'].isnull()])
        en_size = len(english_data[english_data['Count'].isnull()])
        it_size = len(italian_data[italian_data['Count'].isnull()])

        _, col1, col2, col3, _ = st.columns(5)
        col1.metric("English", en_size)
        col2.metric("German", de_size)
        col3.metric("Italian", it_size)

        st.markdown(
            "<h1 style='text-align: center; color: black;'>Welcome to my annotation web application for hate speech detection on Social Media</h1>",
            unsafe_allow_html=True)
        st.markdown(
            "<h2 style='text-align: center; color: black;'>Help me to create a meaningful dataset for hate speech detection </h2>",
            unsafe_allow_html=True)
        image = Image.open('/Users/raisageleta/Documents/GitHub/Text_annotation_webApp/title_picture.jpeg')
        st.image(image)

        st.markdown(
            "<h4 style='text-align: center; color: black;'>Please read the readme before beginning the annotation."
            " There you'll discover all the details regarding my project, as well as the terms and conditions you have to accept to participate in this study. "
            "The download button is located below.</h2>", unsafe_allow_html=True)

    # %% Download button
    with open("INSERT YOUR TERMS OF AGREEMENT PDF HERE", "rb") as pdf_file:
        PDFbyte = pdf_file.read()
    _, _, _, col, _, _, _ = st.columns([1] * 6 + [1.18])
    # clicked = col.button('Button')
    col.download_button(label="Download Readme",
                        data=PDFbyte,
                        file_name="Terms_read_me.pdf",
                        mime='application/octet-stream')

    st.info(
        'If there are any discrepancies when participating via cell phone - Here is a short tutorial | Falls es Unstimmigkeiten gibt, bei der Teilnahme via Handy - Hier ist ein kurzes Tutorial ')

    #video_file = open('******Text_annotation_webApp/Tutorial_mobile.mp4', 'rb')
    # video_file = open('Test.mp4', 'rb')
    #video_bytes = video_file.read()

    st.video(video_bytes)
if selected == "Annotation":

    agree = st.sidebar.checkbox(
        label='I confirm that I have read the terms and conditions and agree to the processing of my personal data| Ich bestätige, dass ich die Allgemeinen Teilnahmebedingungen gelesen habe und mit der Verarbeitung meiner persönlichen Daten einverstanden bin.',
        disabled=False,
        help='Please read the Readme for further details. This is available for download on the homepage | Für nährere Informationen, ließ bitte das Readme. Dies befindet sich auf der Startseite zum downloaden')

    if agree:
        st.sidebar.info('Great, after accepting the terms and conditions, you can start annotating the dataset.')

        st.sidebar.title("Settings")
        language = st.sidebar.selectbox(
            'Please select the language of your choice.'
            ' Bitte wähle die Sprache deiner Wahl aus.',
            ('No language selected', 'German', 'English', 'Italian')
        )
        st.session_state["Language"] = language
        # st.write(st.session_state)
        form = st.sidebar.form("my form")

        if 'English' in language:

            english_page(form, language)

            st.markdown(
                "<h5 style='text-align: center; color: black;'>Now we can start the fun part! Let's get ready for annotation</h5>",
                unsafe_allow_html=True)  #
            get_data = get_data_for_annotation('English', 1)  # get random data

            length_data = st.session_state.number
            # st.write('This is the current number', length_data)
            # list_data_number = [*range(0,length_data ,1)]
            # st.session_state['Text'] = get_data
            # st.session_state['annotation_left'] = length_data

            # st.write(length_data)
            st.session_state["Text"] = get_data
            # st.write(st.session_state)
            get_indexes = st.session_state.Text.index.tolist()
            st.session_state['Index'] = get_indexes
            # st.write('This are all Indexes',st.session_state.Index)
            # index_text = get_indexes[0]

            get_text = get_data.loc[get_indexes[0]]

            st.session_state.current_Text = get_text

            # st.write(st.session_state.current_Text)

            st.session_state.current_index = get_indexes[0]

            # if 'current_Text' not in st.session_state:
            # st.session_state.current_Text = get_text

            if 'gender' not in st.session_state:
                st.session_state.gender = 'W'

            if 'ID' not in st.session_state:
                st.session_state.ID = '0000'

            if "annotations" not in st.session_state:
                st.session_state.annotations = {}
                # st.session_state.current_Text = get_text
                # st.session_state.current_index = get_indexes[0]

            if 'counter' not in st.session_state:
                st.session_state.counter = 0

            if 'annotation_left' not in st.session_state:
                st.session_state.annotation_left = - 1


            def annotate(label):
                st.session_state.annotations[st.session_state.current_index] = label
                if st.session_state.Index:
                    st.session_state.current_index = random.choice(st.session_state.Index)
                    # st.write(st.session_state.current_Index)
                    # generate random index and than new session with the new index and the given Text
                    # st.session_state.newtextID[ID] = st.stessiom_state.text
                    # st.session_state.Index.remove(st.session_state.current_index)
                    st.session_state.counter += 1
                    st.session_state['annotation_left'] = st.session_state.number - st.session_state.counter
                    # update_google_sheet("English_dataset_template", label) #old version
                    update_sql_database_en(label)


            # st.write(st.session_state.current_Index)
            # st.write(get_indexes[0])

            # st.write('This is the curret Text',  st.session_state.current_Text)

            Genders = st.session_state.gender
            ID = st.session_state.ID
            # st.write(Genders, ID)

            if st.session_state.annotation_left == -1:
                st.warning(
                    "Before you start annotating, please fill in the SETTING on the left and press 'Start annotation'."
                    " Note that you can annotate multiple languages!"
                    " Nevertheless, you may only participate once each language, so consider in advance how many texts you wish to annotate."
                    " At least 10 texts must be annotated. The texts are short, ranging from 3 to 50 words."
                    " IMPORTANT: Loading after each annotation takes some time, please wait until the page has loaded and then continue annotating.")

            elif st.session_state.annotation_left:
                st.write(
                    "Annotated:",
                    len(st.session_state.annotations),
                    "– Remaining:",
                    st.session_state.annotation_left,
                )
                st.write(text_data_html(st.session_state.current_Text), unsafe_allow_html=True)
                st.button("This is no hate!0️⃣", on_click=annotate, args=("0",),
                          help='e.g. „I don’t like what you are saying“ ')
                st.button("This is intimidates!1️⃣", on_click=annotate, args=("1",),
                          help='e.g., “deport illegals,” “Muslims not welcomed”, „If I were you, I would kill myself„')
                st.button("This is offends or discriminates!2️⃣", on_click=annotate, args=("2",),
                          help='e.g., “Muslim [expletive],” “You look like a tranny ”')
                st.button("This is promotes violence!3️⃣", on_click=annotate, args=("3",),
                          help='e.g., “attack mosque,” “kill Muslims”, „i will punch you in the face „) ')


            elif st.session_state.annotation_left == 0:
                st.balloons()
                st.success(
                    f"🎈 Ready! All {len(st.session_state.annotations)} texts have been annotated. Thank you for your participation, if you still have time I would be happy if you would answer some questions in the interview. "
                )

        if 'German' in language:

            german_page(form, language)

            st.markdown(
                "<h5 style='text-align: center; color: black;'>Jetzt können wir mit dem spaßigen Teil anfangen! Auf geht's zum Annotieren</h5>",
                unsafe_allow_html=True)  #
            get_data = get_data_for_annotation('German', 1)  # get random data

            length_data = st.session_state.number
            # st.write(st.session_state)
            # list_data_number = [*range(0,length_data ,1)]
            # st.session_state['Text'] = get_data
            # st.session_state['annotation_left'] = length_data

            # st.write(length_data)
            st.session_state["Text"] = get_data
            # st.write(st.session_state)
            get_indexes = st.session_state.Text.index.tolist()
            st.session_state['Index'] = get_indexes
            # st.write('This are all Indexes',st.session_state.Index)
            # index_text = get_indexes[0]

            get_text = get_data.loc[get_indexes[0]]

            st.session_state.current_Text = get_text

            st.session_state.current_index = get_indexes[0]

            # if 'current_Text' not in st.session_state:
            # st.session_state.current_Text = get_text

            if 'gender' not in st.session_state:
                st.session_state.gender = 'W'

            if 'ID' not in st.session_state:
                st.session_state.ID = '0000'

            if "annotations" not in st.session_state:
                st.session_state.annotations = {}
                # st.session_state.current_Text = get_text
                # st.session_state.current_index = get_indexes[0]

            if 'counter' not in st.session_state:
                st.session_state.counter = 0

            if 'annotation_left' not in st.session_state:
                st.session_state.annotation_left = - 1


            def annotate(label):
                st.session_state.annotations[st.session_state.current_index] = label
                if st.session_state.Index:
                    st.session_state.current_index = random.choice(st.session_state.Index)
                    # st.write(st.session_state.current_Index)
                    # generate random index and than new session with the new index and the given Text
                    # st.session_state.newtextID[ID] = st.stessiom_state.text
                    # st.session_state.Index.remove(st.session_state.current_index)
                    st.session_state.counter += 1
                    st.session_state['annotation_left'] = st.session_state.number - st.session_state.counter
                    # update_google_sheet("German_dataset_template", label) #old version
                    update_sql_database_ger(label)


            # st.write(st.session_state.current_Index)
            # st.write(get_indexes[0])

            # st.write('This is the curret Text',  st.session_state.current_Text)

            Genders = st.session_state.gender
            ID = st.session_state.ID
            # st.write(Genders, ID)

            st.write(st.session_state)
            if st.session_state.annotation_left == -1:
                st.warning(
                    "Bevor du zu Annotieren beginnst, fülle bitte links das SETTING aus und drücke 'Start annotation'."
                    " Beachte, dass du mehrere Sprachen annotieren kannst!"
                    " Aber du solltest nur einmal pro Sprache teilnehmen, daher mache dir vorher Gedanken, wie viele Texte du annotieren möchtest."
                    " Mindestens 10 Texte müssen annotiert werden. Die Texte sind kurz und umfassen zwischen 3 und 50 Wörtern."
                    " WICHTIG: Das Laden nacch jeder Annotation braucht etwas Zeit, bitte warte bis die Seite geladen hat und annotiere dann weiter.")

            elif st.session_state.annotation_left:
                st.write(
                    "Annotiert:",
                    len(st.session_state.annotations),
                    "– Übrig:",
                    st.session_state.annotation_left,
                )

                st.write(text_data_html(st.session_state.current_Text), unsafe_allow_html=True)
                st.button("Das ist kein Hass!0️⃣", on_click=annotate, args=("0",),
                          help='z. B. "Ich mag nicht, was du sagst" ')
                st.button("Das ist Einschüchterung!1️⃣", on_click=annotate, args=("1",),
                          help='z. B. "Illegale abschieben", "Muslime nicht willkommen", "Wenn ich du wäre, würde ich mich umbringen"')
                st.button("Das ist Beleidigung oder Diskriminierung!2️⃣", on_click=annotate, args=("2",),
                          help='z. B. "Muslim [Schimpfwort]", "Du siehst aus wie eine Transe" ')
                st.button("Das fördert Gewalt!3️⃣", on_click=annotate, args=("3",),
                          help='z. B. "Moschee angreifen", "Muslime töten", "ich werde dir ins Gesicht schlagen"')

            # st.write(st.session_state)

            elif st.session_state.annotation_left == 0:
                st.balloons()
                st.success(
                    f"🎈 Fertig! Alle {len(st.session_state.annotations)} Texte wurden annotiert. Vielen Dank für deine Teilnahme, falls du noch Zeit hast würde ich mich freuen wenn du im Interview einige Fragen beantworten würdest."
                )

            # st.write("### Annotations")
            # st.write(st.session_state.annotations)

        if 'Italian' in language:

            italian_page(form, language)

            st.markdown(
                "<h5 style='text-align: center; color: black;'>Now we can start the fun part! Let's get ready for annotation</h5>",
                unsafe_allow_html=True)  #
            get_data = get_data_for_annotation('Italian', 1)  # get random data

            length_data = st.session_state.number
            # st.write('This is the current number', length_data)
            # list_data_number = [*range(0,length_data ,1)]
            # st.session_state['Text'] = get_data
            # st.session_state['annotation_left'] = length_data

            # st.write(length_data)
            st.session_state["Text"] = get_data
            # st.write(st.session_state)
            get_indexes = st.session_state.Text.index.tolist()
            st.session_state['Index'] = get_indexes
            # st.write('This are all Indexes',st.session_state.Index)
            # index_text = get_indexes[0]

            get_text = get_data.loc[get_indexes[0]]

            st.session_state.current_Text = get_text

            st.session_state.current_index = get_indexes[0]

            # if 'current_Text' not in st.session_state:
            # st.session_state.current_Text = get_text

            if 'gender' not in st.session_state:
                st.session_state.gender = 'W'

            if 'ID' not in st.session_state:
                st.session_state.ID = '0000'

            if "annotations" not in st.session_state:
                st.session_state.annotations = {}
                # st.session_state.current_Text = get_text
                # st.session_state.current_index = get_indexes[0]

            if 'counter' not in st.session_state:
                st.session_state.counter = 0

            if 'annotation_left' not in st.session_state:
                st.session_state.annotation_left = - 1


            def annotate(label):
                st.session_state.annotations[st.session_state.current_index] = label
                if st.session_state.Index:
                    st.session_state.current_index = random.choice(st.session_state.Index)
                    # st.write(st.session_state.current_Index)
                    # generate random index and than new session with the new index and the given Text
                    # st.session_state.newtextID[ID] = st.stessiom_state.text
                    # st.session_state.Index.remove(st.session_state.current_index)
                    st.session_state.counter += 1
                    st.session_state['annotation_left'] = st.session_state.number - st.session_state.counter
                    # update_google_sheet("Italian_Dataset_Template", label) old version
                    update_sql_database_it(label)


            # st.write(st.session_state.current_Index)
            # st.write(get_indexes[0])
            st.write(st.session_state)

            # st.write('This is the curret Text',  st.session_state.current_Text)

            Genders = st.session_state.gender
            ID = st.session_state.ID
            # st.write(Genders, ID)

            if st.session_state.annotation_left == -1:
                st.warning(
                    "Before you start annotating, please fill in the SETTING on the left and press 'Start annotation.'"
                    " Note that you can annotate multiple languages!"
                    " Nevertheless, you may only participate once each language, so consider in advance how many texts you wish to annotate."
                    " At least 10 texts must be annotated. The texts are short, ranging from 3 to 50 words."
                    " IMPORTANT: Loading after each annotation takes some time, please wait until the page has loaded and then continue annotating.")

            elif st.session_state.annotation_left:
                st.write(st.session_state)
                st.write(
                    "Annotated:",
                    len(st.session_state.annotations),
                    "– Remaining:",
                    st.session_state.annotation_left,
                )
                st.write(text_data_html(st.session_state.current_Text), unsafe_allow_html=True)
                st.button("This is no hate!0️⃣", on_click=annotate, args=("0",),
                          help='e.g. „I don’t like what you are saying“ ')
                st.button("This intimidates!1️⃣", on_click=annotate, args=("1",),
                          help='e.g., “deport illegals,” “Muslims not welcomed”, „If I were you, I would kill myself„')
                st.button("This offends or discriminates!2️⃣", on_click=annotate, args=("2",),
                          help='e.g., “Muslim [expletive],” “You look like a tranny ”')
                st.button("This promotes violence!3️⃣", on_click=annotate, args=("3",),
                          help='e.g., “attack mosque,” “kill Muslims”, „i will punch you in the face „) ')

            # st.write(st.session_state)
            elif st.session_state.annotation_left == 0:
                st.balloons()
                st.success(
                    f"🎈 Ready! All {len(st.session_state.annotations)} texts have been annotated. Thank you for your participation, if you still have time I would be happy if you would answer some questions in the interview. "
                )
            # st.write("### Annotations")
            # st.write(st.session_state.annotations)

# %% Interview page
if selected == "Interview":

    language_int = st.selectbox(
        'Please select your language'
        '| Bitte wähle die Sprache aus.',
        ('No language selected', 'German', 'English')
    )

    if 'English' in language_int:
        # st.markdown("<h5 style='text-align: center; color: black;'>I would appreciate your participation in my survey. Each question can be answered on a voluntary basis. You are not required to answer questions that make you feel uncomfortable. All responses are confidential and cannot be traced. I hope you like the interview, and I appreciate your participation.</h5>", unsafe_allow_html=True)#
        st.info(
            'I would appreciate your participation in my survey. Each question can be answered on a voluntary basis. You are not required to answer questions that make you feel uncomfortable. All responses are confidential and cannot be traced. I hope you like the interview, and I appreciate your participation.')

        src = "https://docs.google.com/forms/d/e/1FAIpQLScQ55y1FMKaUY1pLueEZ6kT_-pufrCxfH6j8lrVK5IoUd3sRA/viewform?embedded=true"
        st.components.v1.iframe(src, width=640, height=1017, scrolling=True)

    if 'German' in language_int:
        # st.markdown("<h5 style='text-align: center; color: black;'>Ich würde mich über deine Teilnahme an meiner Umfrage freuen. Die Beantwortung jeder Frage ist freiwillig. Du bist nicht verpflichtet, Fragen zu beantworten, bei denen du dich unwohl fühlen. Alle Antworten sind vertraulich und können nicht zurückverfolgt werden. Ich hoffe, dass dir das Interview gefallen hat, und bedanke mich für deine Teilnahme.</h5>", unsafe_allow_html=True)
        st.info(
            'Ich würde mich über deine Teilnahme an meiner Umfrage freuen. Die Beantwortung jeder Frage ist freiwillig. Du bist nicht verpflichtet, Fragen zu beantworten, bei denen du dich unwohl fühlst. Alle Antworten sind vertraulich und können nicht zurückverfolgt werden. Ich hoffe, dass dir das Interview gefallen hat, und bedanke mich für deine Teilnahme.')
        src = "https://docs.google.com/forms/d/e/1FAIpQLScSm_tXOfw34c79LJlq5YpVo-mDuIcEGle3bMMWe5qG4FaRmg/viewform?embedded=true"
        st.components.v1.iframe(src, width=640, height=1017, scrolling=True)
