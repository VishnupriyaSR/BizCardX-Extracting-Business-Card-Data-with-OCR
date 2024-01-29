#PANDAS AND NUMPY
import pandas as pd
import numpy as np

#REGULAR EXPRESSION
import re

#STREAMLIT
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image

#EASYOCR
import easyocr 

#POSTGRE-SQL DB
import psycopg2

#IMAGE PROCESSING LIBRARIES
import cv2
import os
import matplotlib.pyplot as plt
import io

#Connect to the POSTgre-SQL Server
mydb=psycopg2.connect(host="localhost",user="postgres",password="vishnu",database="BizCardX",port=5432)
cursor=mydb.cursor()

# card="create table if not exists card_data(card_holder text,designation text,mobile_num varchar(100),email text,website text,area text,city text,state text,company_name text,pincode varchar(50),businesscard bytea)"
# cursor.execute(card)

# CONVERTING IMAGE TO BINARY TO UPLOAD TO SQL DATABASE
def img_to_binary(file):
    # Convert image data to binary format
    with open(file, 'rb') as file:
        binaryData = file.read()
    return binaryData

#Extract text from uploaded business card
def extract_text(card):
    extract_dict = {"CardHolder_Name": [],"Designation": [],"Mobile_Number": [],"Email": [],"Website": [],
                    "Area": [],"City": [],"State": [],"Company_Name": [],"Pincode": [],"Image":img_to_binary(saved_img)} 
    extract_dict['CardHolder_Name'].append(result[0])
    extract_dict['Designation'].append(result[1])

    for ind, i in enumerate(result):

      # To get MOBILE NUMBER
        if "-" in i:
            extract_dict["Mobile_Number"].append(i)
            if len(extract_dict["Mobile_Number"]) > 1:
                extract_dict["Mobile_Number"] = "  and  ".join(extract_dict["Mobile_Number"])

        # To get EMAIL ID
        elif "@" in i:
            lwr = i.lower()
            extract_dict["Email"].append(lwr)

        # To get WEBSITE_URL
        elif "www " in i.lower() or "www." in i.lower():
            extract_dict ["Website"].append(i)
        elif "WWW" in i:
            extract_dict ["Website"] = result[4] + "." + result[5]

        # To get AREA
        if re.findall('^[0-9].+, [a-zA-Z]+', i):
            extract_dict["Area"].append(i.split(',')[0])
        elif re.findall('[0-9] [a-zA-Z]+', i):
             extract_dict["Area"].append(i)
       # To get Company Name
        elif i == "selva" or i == "digitals":
            extract_dict["Company_Name"].append(i)
            if len(extract_dict["Company_Name"]) > 1:
                extract_dict["Company_Name"] = " ".join(extract_dict["Company_Name"])
        elif i == "GLOBAL" or i == "INSURANCE":
            extract_dict["Company_Name"].append(i)
            if len(extract_dict["Company_Name"]) > 1:
                extract_dict["Company_Name"] = " ".join(extract_dict["Company_Name"])
        elif i == "BORCELLE" or i == "AIRLINES":
            extract_dict["Company_Name"].append(i)
            if len(extract_dict["Company_Name"]) > 1:
                extract_dict["Company_Name"] = " ".join(extract_dict["Company_Name"])
        elif i == "Family" or i == "Restaurant":
            extract_dict["Company_Name"].append(i)
            if len(extract_dict["Company_Name"]) > 1:
                extract_dict["Company_Name"] = " ".join(extract_dict["Company_Name"])
        elif i == "Sun Electricals":
            extract_dict["Company_Name"].append(i)
            if len(extract_dict["Company_Name"]) > 1:
                extract_dict["Company_Name"] = " ".join(extract_dict["Company_Name"])
                
        # To get CITY NAME
        match1 = re.findall('.+St , ([a-zA-Z]+).+', i)
        match2 = re.findall('.+St,, ([a-zA-Z]+).+', i)
        match3 = re.findall('^[E].*', i)
        if match1:
             extract_dict["City"].append(match1[0])
        elif match2:
             extract_dict["City"].append(match2[0])
        elif match3:
             extract_dict["City"].append(match3[0])

        # To get STATE
        state_match = re.findall('[a-zA-Z]{9} +[0-9]', i)
        if state_match:
            extract_dict["State"].append(i[:9])
        elif re.findall('^[0-9].+, ([a-zA-Z]+);', i):
            extract_dict["State"].append(i.split()[-1])
        if len(extract_dict["State"]) == 2:
            extract_dict["State"].pop(0)     

       # To get PINCODE
        if len(i) == 6 and i.isdigit():
            extract_dict["Pincode"].append(i)
        elif re.findall('[a-zA-Z]{9} +[0-9]', i):
            extract_dict["Pincode"].append(i[10:])

       
    return extract_dict

 # FUNCTION TO CREATE DATAFRAME
def create_df(extract_dict):
    df = pd.DataFrame(extract_dict)
    return df
       
# Configuring Streamlit GUI
#Title

st.markdown("<h1 style='text-align: center; color: violet;'>BizCardX: Extracting Business Card Data with OCR </h1>", unsafe_allow_html=True)

selected = option_menu(None,
                           options = ["Home","Upload and Extract Data","Modify"],
                           icons = ["house","cloud-upload","pencil-square"],
                           default_index=0,
                           orientation="horizontal",
                           styles={"container": {"width": "100%"},
                                   "icon": {"color": "white", "font-size": "24px"},
                                   "nav-link": {"font-size": "24px", "text-align": "center", "margin": "-2px"},
                                   "nav-link-selected": {"background-color": "#6F36AD"}})

# # # MENU 1 - Home
if selected == "Home":
    col1,col2=st.columns(2)
    with col1:
        st.image("design-creative-business-cards.jpg")
        
        
    with col2:
        st.write("## :green[**Bizcard is a Python application designed to extract information from business cards**]")

        st.write("###:green[**Overview**] An Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR. The extracted information include the company name, card holder name, designation, mobile number, email address, website URL, area, city, state,and pin code.The application allow users to save the extracted information into a database along with the uploaded business card image. The database store multiple entries, each with its own business card image and extracted information.")
        st.write(":green[**Technologies Used**]-**Python,Streamlit,EasyOCR,Image Processing and DBMS-POSTGRESQL**") 
        
        
# UPLOAD AND EXTRACT MENU

if selected == "Upload and Extract Data":

    if st.button("Stored data"):
        cursor.execute(
            "select card_holder,designation,mobile_num,email,website,area,city,state,company_name,pincode from card_data")
        updated_df = pd.DataFrame(cursor.fetchall(),
                                  columns=["CardHolder_Name", "Designation", "Mobile_Number",
                                           "Email","Website", "Area", "City", "State","Company_Name","Pincode"])
        st.write(updated_df)
        
        
    col1,col2=st.columns(2)
    with col1:
        st.subheader(":blue[Upload a Business Card]")
        image = st.file_uploader("upload here", label_visibility="collapsed", type=["png", "jpeg", "jpg"])
        st.markdown("### You have uploaded the card")  

        # DISPLAYING THE UPLOADED CARD
        st.image(image, width=650, caption='Uploaded Image')

        st.markdown(f'<style>.css-1aumxhk img {{ max-width: 300px; }}</style>',unsafe_allow_html=True)
        
    # DISPLAYING THE CARD Details
    with col2:
        reader = easyocr.Reader(['en'], model_storage_directory=".")    
        saved_img = os.getcwd() + "\\" + "uploaded_cards" + "\\" + image.name
        result = reader.readtext(saved_img, detail=0, paragraph=False)
        ext_text = extract_text(result)
        df1 = pd.DataFrame(ext_text)
        st.success("### Data Extracted!")
        st.write(df1)

           
        if st.button("UPLOAD TO SQL DATABASE"):
            with st.spinner("Uploading..."):
                for i, row in df1.iterrows():
                    query = """INSERT INTO card_dataa(card_holder,designation,mobile_num,email,website,area,city,state,company_name,pincode,businesscard)
                                         VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
                    cursor.execute(query, tuple(row))
                    mydb.commit()

                st.success("#### Uploaded to database successfully!")

        if st.button("VIEW DATA"):
            cursor.execute("select * from card_dataa")
            #cursor.execute("select card_holder,designation,mobile_num,email,website,area,city,state,company_name,pincode from card_data")
            updated_df = pd.DataFrame(cursor.fetchall(),
                                      columns=["CardHolder_Name", "Designation", "Mobile_Number",
                                               "Email","Website", "Area", "City", "State","Company_Name","Pincode","Image"])
            st.write(updated_df)

#MODIFY MENU
if selected == "Modify":
    st.markdown("# :blue[Data Modification]")
    select = option_menu(None,
                         options=["ALTER", "DELETE"],
                         default_index=0,
                         orientation="horizontal",
                         styles={"container": {"width": "100%"},
                                 "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px"},
                                 "nav-link-selected": {"background-color": "#6495ED"}})
    if select=="ALTER":
        
        try:
            st.markdown("### :orange[Select Card Holder]")
            cursor.execute("SELECT card_holder FROM card_data")
            output = cursor.fetchall()
            cards = [item for sublist in output for item in sublist]
            selected_card = st.selectbox("Select a name for updating data", cards)



            st.markdown("### :blue[Update Card-Data]")
            cursor.execute("select card_holder,designation,mobile_num,email,website,area,city,state,company_name,pincode from card_dataa                               WHERE card_holder=%s",(selected_card,))        
            result = cursor.fetchone()

         # DISPLAYING ALL THE INFORMATIONS
            # st.text_input('Header', 'Default text Value') 
            card_holder= st.text_input("CardHolder_Name", result[0])
            designation = st.text_input("Designation", result[1])
            mobile_num = st.text_input("Mobile_Number", result[2])
            email = st.text_input("Email_ID", result[3])
            website = st.text_input("Website", result[4])
            area = st.text_input("Area", result[5])
            city = st.text_input("City", result[6])
            state = st.text_input("State", result[7])
            company_name=st.text_input("Company_Name",result[8])
            pincode = st.text_input("Pincode", result[9])

            # -----Saving the changes to the SQL Database-----
            if st.button("Commit changes to DataBase"):
                cursor.execute("UPDATE card_dataa SET card_holder=%s, designation=%s, "
                                "mobile_num=%s, email=%s, website=%s, area=%s, city=%s, state=%s,"
                                "company_name=%s,pincode=%s WHERE card_holder=%s ", (card_holder, designation,
                                                                          mobile_num, email, website,
                                                                          area, city, state, company_name, pincode, selected_card))
                mydb.commit()
                st.success("Updated Successfully!!")


            if st.button("View Updated Data"):
                cursor.execute("select card_holder,designation,mobile_num,email,website,area,city,state,company_name,pincode from card_dataa")
                updated_df = pd.DataFrame(cursor.fetchall(),
                                          columns=["CardHolder_Name", "Designation", "Mobile_Number",
                                                   "Email","Website", "Area", "City", "State","Company_Name","Pincode"])
                st.write(updated_df)

        except:
            st.warning("There is no data available in the database")
            
    if select=="DELETE":
        st.markdown('<div style="height: 50px;"></div>',unsafe_allow_html=True)
        st.markdown("### :orange[Delete a Card]")
        cursor.execute("SELECT card_holder FROM card_dataa")
        output = cursor.fetchall()
        cards = [item for sublist in output for item in sublist]
        selected_card = st.selectbox("Select a card holder name to Delete", cards)
        st.write(f"##### Click the below button to confirm the deletion of :red[**{selected_card}'s**] card")

        if st.button("Yes Delete Card"):
            cursor.execute("DELETE FROM card_dataa WHERE card_holder=%s",(selected_card,))
            mydb.commit()
            st.success("Successfully Deleted!!")
    
# DISPLAY FINAL UPDATED DATA
        st.markdown('<div style="height: 50px;"></div>', unsafe_allow_html=True)
        st.markdown("### :orange[Final Data]")
        if st.button("Click to view updated data"):
            cursor.execute("select card_holder,designation,mobile_num,email,website,area,city,state,company_name,pincode from card_dataa")
            updated_df = pd.DataFrame(cursor.fetchall(),
                                              columns=["CardHolder_Name", "Designation", "Mobile_Number",
                                                       "Email","Website", "Area", "City", "State","Company_Name","Pincode"])
            st.write(updated_df)

