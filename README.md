# Introduction

Bizcard Extraction is a Python application built with Streamlit, EasyOCR, OpenCV, regex function, and MySQL database. It allows users to extract information from business cards and store it in a MySQL database for further analysis. The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.

# EasyOCr 

EasyOCR is a Python computer language Optical Character Recognition (OCR) module that is both flexible and easy to use. OCR technology is useful for a variety of tasks, including data entry automation and image analysis. It enables computers to identify and extract text from photographs or scanned documents.

# Approach

# 1.Install the required packages:

Need to install Python, Streamlit,easyOCR, and a database management system like SQLite or MySQL.

# Libaries used:

Pandas - To Create a DataFrame with the scraped data
Psycopg2 - To store and retrieve the data
Streamlit - To Create Graphical user Interface
EasyOCR - To extract text from images

# 2.Design the user interface: 

Create a simple and intuitive user interface using Streamlit that guides users through the process of uploading the business card image and extracting its information.

# 3.Implement the image processing and OCR: 

Use easyOCR to extract the relevant information from the uploaded business card image.

# 4.Display the extracted information: 

Once the information has been extracted,display it in a clean and organized manner in the Streamlit GUI.

# 5.Implement database integration: 

Use a database management system like SQLite or MySQL or Postgre SQL to store the extracted information along with the uploaded business card image.
