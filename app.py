import streamlit as st
from bs4 import BeautifulSoup
import requests
import tldextract

viable_domain = ['medium', 'towardsdatascience', 'fritz']

def validate_url(url):
    if requests.get(url).status_code == 200:
        ext = tldextract.extract(url)
        if ext.domain in viable_domain:
            message = 'Looks like a medium post'
        else:
            message = 'This url does not look like it is coming from medium. Please know that this may affect the quality of the highlights of the post'
    else:
        message = 'This url does not seem coorect. Please paste the correct url'
    return message

def scrape_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    topic = soup.find('h1')
    head = topic.text
    fetch = soup.find_all('p')
    new = [i.text for i in fetch]
    content = ' '.join(new)[:-11]
    return head, content

def summarize():
    return summary

def main():
    """Summarizing app"""

    st.title('Medium Post Summarizer')
    # st.subheader('using Extractive method')

    html_temp = """
    <div style="background-color:orange;padding:15px">
    <h2> Summarizer ML App</h2>
    </div>
    <br>
    """

    st.markdown(html_temp, unsafe_allow_html=True)

    url = st.text_input("Enter a Medium post URL")
    if st.button("Scrape"):
        if url == '':
            st.error('Please input a url')
        else:
            message = validate_url(url)
            if message == "This url does not seem coorect. Please paste the correct url":
                st.error(message)
            elif message == :
                st.warning(message)
            else:
                st.success(message)
        # st.text('link is correct')
        head, content = scrape_url(url)
        st.success(head)
        st.success(content)
        html_temp1 = """
        <div style="background-color:magenta;padding:15px">
        <h2>{{head}}</h2>
        </div>
        <br>
        """
        st.markdown(html_temp1, unsafe_allow_html=True)







if __name__ == '__main__':
    main()
