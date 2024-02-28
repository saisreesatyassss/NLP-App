from matplotlib import pyplot as plt
import streamlit as st
import nltk
from nltk import word_tokenize, FreqDist
import requests
from bs4 import BeautifulSoup 
from PyPDF2 import PdfReader
# imgUrl="https://th.bing.com/th/id/OIP.bjirIJDTGCmwGltnC6ubgAAAAA?rs=1&pid=ImgDetMain"
imgUrl="https://th.bing.com/th/id/OIP.4QUpOIbAZEzxiHeRZk2FEwAAAA?rs=1&pid=ImgDetMain"
st.image(imgUrl)
st.title("NLP App")

nltk.download('punkt')


def generate_word_frequency(text):
    words = word_tokenize(text)
    fdist = FreqDist(words)
    return fdist

def get_webpage_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        st.error(f"Failed to retrieve content. Status code: {response.status_code}")
        return None

def extract_tokens(text):
    soup = BeautifulSoup(text, 'html.parser')
    page_content = soup.get_text()
    tokens = word_tokenize(page_content)
    expressions = [token for token in tokens if any(char.isalpha() for char in token)]
    words = [token for token in tokens if token.isalpha()]
    numbers = [token for token in tokens if token.isnumeric()]
    return expressions, words, numbers

with st.sidebar:
    st.title("NLP App")
    
    choice=st.radio("Navigation", ["Paragraph", "webpage", "Pdf", "Text File"])
    st.info("This application is created by [  SAISRISATYA ](https://www.linkedin.com/in/padala-saisrisatya-subramaneswar-359998247/)")


if choice =="Paragraph":
    # Input text from the user
    user_input = st.text_area("Enter your text here:", "I'm Nishika. I am a junior studying in VIT-AP. I have 9.4 CGPA.\nI love to code.")

    if st.button("Generate Word Frequency"):
        # Generate word frequency distribution
        word_freq = generate_word_frequency(user_input)

        # Display total number of words
        st.write(f"The total number of words in the text is {len(word_freq)}")

        # Display the top 10 most common words
        st.write("Top 10 Most Common Words:")
        st.write(word_freq.most_common(10))

        # Plot word frequency distribution
        plt.figure(figsize=(10, 6))
        word_freq.plot(30, cumulative=False)
        st.pyplot()


elif choice =="webpage":
    st.title("Webpage Token Extractor")

    # Input URL from the user
    webpage_url = st.text_input("Enter the URL of the webpage:", 'https://www.gutenberg.org/cache/epub/64317/pg64317.txt')

    if st.button("Extract Tokens"):
        # Get webpage content
        webpage_content = get_webpage_content(webpage_url)

        if webpage_content:
            # Extract tokens
            expressions, words, numbers = extract_tokens(webpage_content)

            # Display the results
            st.write("Expressions:", expressions)
            st.write("Words:", words)
            st.write("Numbers:", numbers)


elif choice == "Pdf":
    st.write("Pdf")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

    if uploaded_file is not None:
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        st.write(text)

elif choice =="Text File":
    st.warning("Text File")
    uploaded_file = st.file_uploader("Upload a text file", type=["txt"])

    if uploaded_file is not None:
        text = uploaded_file.getvalue().decode("utf-8")
        st.write(text)

else:
    st.write(" Data")