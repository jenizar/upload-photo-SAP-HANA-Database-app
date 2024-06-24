import streamlit as st
import os
from hdbcli import dbapi

# EDA Pkg
import pandas as pd

# Image
from PIL import Image

@st.cache_data
def load_image(image_file):
    img = Image.open(image_file)
    return img
    
# Fxn to Save Uploaded File to Directory
def save_uploaded_file(uploadedfile):
    with open(os.path.join("employee",uploadedfile.name),"wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved file :{} in photo".format(uploadedfile.name))        
    
def main():
    st.title("Employee Services - Uploads Photo App")
    menu = ["Home","Dataset","Display","About"]
    choice = st.sidebar.selectbox("Menu",menu)
    
    if choice == "Home":
       st.subheader("Upload Photo")
       image_file = st.file_uploader("Upload Photo",type=['png','jpeg','jpg'])
       if image_file is not None:
          file_details = {"FileName":image_file.name,"FileType":image_file.type}
          st.write(file_details)
          st.write(type(image_file))
          img = load_image(image_file)
          new_image = img.resize((150, 200))
          st.image(new_image)
          imgfile1 = image_file.name
          folder1 = 'photo'
          con = dbapi.connect(
            address="4b25c31e-9856-4586-a8d0-b1caa0f89c02.hana.trial-us10.hanacloud.ondemand.com",
            port=443,
            user="DBADMIN",
            password="MyHanadb911_")
          cur=con.cursor()
          sql = "INSERT INTO EMPLOYEE.PHOTO(folder, imgfile) VALUES (?,?)"
          val = (folder1,imgfile1)
          cur.execute(sql, val)
          con.commit()
          #st.image(img,height=250,width=250)
          # Saving File
          
          # photo/imagename.png
          with open(os.path.join("photo",image_file.name),"wb") as f:
               f.write(image_file.getbuffer())
               
          st.success("File Saved")     
          
    elif choice == "Dataset":
        st.subheader("Dataset")
        datafile = st.file_uploader("Upload CSV",type=['csv'])
        if datafile is not None:
           file_details = {"FileName":datafile.name,"FileType":datafile.type}
           df = pd.read_csv(datafile)
           st.dataframe(df)

    elif choice == "Display":
        st.subheader("Display Photo")
        #image = Image.open('tempDir')
        #new_image = image.resize((100, 200))
        #st.image(new_image, caption='PyCharm')
        #s = 'Apple,Mango,Banana'
        #print(f'List of Items in CSV ={s.split(",")}')
        con = dbapi.connect(
            address="4b25c31e-9856-4586-a8d0-b1caa0f89c02.hana.trial-us10.hanacloud.ondemand.com",
            port=443,
            user="DBADMIN",
            password="MyHanadb911_")        
        cur=con.cursor()
        cur.execute("SELECT * FROM EMPLOYEE.PHOTO ORDER BY PID;")
        data = cur.fetchall()
        s = ""
        for row in data:      
            s += row[1] + '/' + row[2] + ',' 
        s = s[:-1]
        storimg = s.split(",")
        #print (s)
        #print (storimg)
        images = storimg    
        #images = ['photo/pic1.png', 'photo/pic2.png', 'photo/pic3.png']
        st.image(images, use_column_width=None, width=250, caption=["employee photo"] * len(images))
           
    else:
        st.subheader("About App")
        
if __name__== '__main__':
    main()     
                     
           
