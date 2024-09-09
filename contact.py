import streamlit as st
import mysql.connector


def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  
            password='', 
            database='Sasyam'  
        )
        return connection
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
        return None

def insert_contact_form_data(name, email, inquiry_type, message):
    connection = create_connection()
    if connection is None:
        st.error("Failed to connect to the database.")
        return

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO contact (name, email, inquiry_type, message) 
            VALUES (%s, %s, %s, %s)
            """,
            (name, email, inquiry_type, message)
        )

        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")
    else:
        st.success("Message successfully saved to the database.")

def app():
    st.title("Contact Us - Crop Disease Detection")

    
    st.write("""
    If you have any questions, feedback, or need further assistance, feel free to contact us. 
    We're here to help with anything related to crop disease detection.
    """)

    
    with st.form(key='contact_form'):
        name = st.text_input("Name")
        email = st.text_input("Email")
        inquiry_type = st.selectbox("What can we help you with?", 
                                    ["General Inquiry", "Technical Issue", "Feedback", "Other"])
        message = st.text_area("Message", height=150)
        
        submit_button = st.form_submit_button("Submit")

        if submit_button:
            insert_contact_form_data(name, email, inquiry_type, message)
            st.success(f"Thank you, {name}. We've received your message and will respond to {email} soon.")

    st.subheader("Contact Us")
    st.write("""
        Email: saysam@sasyam.com  
        Phone: +91 8563789078  
        Address: Prayagraj, U.P.
    """)

if __name__ == '__main__':
    app()
