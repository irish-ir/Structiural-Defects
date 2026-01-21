import streamlit as st 
import datetime as dt
import os 
from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import datetime as dt
from PIL import Image

# Configure the model:
gemini_api_key=os.getenv('GOOGLE_API_KEY1')
genai.configure(api_key=gemini_api_key)

model = genai.GenerativeModel('gemini-2.5-flash')

# Let's create Sidebar for image upload
st.sidebar.title(':red[Upload the image here:]')
uploaded_image=st.sidebar.file_uploader('Image',type=['jpeg','jpg','png','jfif'],accept_multiple_files=True)
uploaded_image=[Image.open(img) for img in uploaded_image]

if uploaded_image:
    
    st.sidebar.success('Image has been uploaded successfully')
    st.sidebar.subheader(':blue[Uploaded Image]')
    st.sidebar.image(uploaded_image)      

# LET'S CREATE THE MAIN PAGE 
st.title(':orange[STRUCTURAL DEFECT:-]:blue[AI Assisted Structural Defect Identifier]')
st.markdown('### :green[This application takes the image of the structural defect from the  ]')
title=st.text_input('Enter the Title of the report:')
name=st.text_input('Enter the name of the person who has prepared the report:')
desig=st.text_input('Enter the designation of the person who have made the report:')
orgz=st.text_input('Enter the name of the organization:')

if st.button('Submit'):
    with st.spinner('Processing.....'):
        prompt = f'''
            <role> You are an expert structural engineer with 20 + years of experience.
            <Goal> You need to prepare a detailed report on the structural defect shown in the images provided by the user.
            <Context> Images are shared by the user has been attached.
            <Format> Follow the steps to prepare the report
            * Add title at the top of the report. The title pro
            * next add name,designation and organization and date of a person who has prepared the report 
            also include the data. Following are the detail]
            name:{name}
            designation:{desig}
            organization:{orgz}
            data:{dt.datetime.now().date()}
            * Identify and classify the defect for eg: crack,spalling,
            * There could be more than one defects in images. I
            * For each defect identified provide a short description of its potential impact on the structure.Also mentioning if the effect is inevitable or not or avoiadable.
            * Provide the short term and long term solutiion for   Along with an estimated cost in INR and estimated time.
            * What precautionary measures can be taken to avoid 

            <Instruction> 
            * The report generated should be in the word format.
            * Use bullet points and tablular format where ever possible .
            * Make sure the report does not exceeeds 3 pages.
            
            '''
        response= model.generate_content([prompt,*uploaded_image],
                                         generation_config={'temperature':0.9})
        st.write(response.text)

    if st.download_button(
        label= 'Click to download',
        data= response.text,
        file_name= 'structural_defect_report.txt',
        mime='text/plain'):
        st.success('Your file is downloaded.')