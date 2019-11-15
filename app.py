from  sklearn.feature_extraction.text import TfidfVectorizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from bs4 import BeautifulSoup
import streamlit as st
import numpy as np
import tldextract
import requests
import spacy

nlp = spacy.load('en_core_web_sm', disable = ['tagger', 'ner'])


viable_domain = ['medium', 'towardsdatascience', 'fritz']
LANGUAGE = 'english'
COUNT = 10

correct = 'Looks like a medium post'
warning = 'This url does not look like it is coming from medium. Please know that this may affect the quality of the highlights of the post'
error = 'This url does not seem correct. Please paste the correct url'
def validate_url(url):
    if requests.get(url).status_code == 200:
        ext = tldextract.extract(url)
        if ext.domain in viable_domain:
            message = correct
        else:
            message = warning
    else:
        message = error
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

def summarize(string):
    new_string = string.replace('.', '. ').strip()
    lsa = LsaSummarizer(Stemmer(LANGUAGE))
    lsa.stop_words = get_stop_words(LANGUAGE)
    parser = PlaintextParser.from_string(new_string, Tokenizer(LANGUAGE))
    lsa_summary = lsa(parser.document, COUNT)
    lsa_s = [str(sent) for sent in lsa_summary]
    summary = ' '.join(lsa_s)
    return summary

def vectorize(string):
    work = nlp(string)
    clean_text = []
    for word in work:
        if not word.is_stop:
            if word.is_alpha:
                clean_text.append(word.lemma_)
    new_string = ' '.join(clean_text)
    tf = TfidfVectorizer(stop_words='english', lowercase= False)
    out = tf.fit_transform([new_string])
    feature_names = np.array(tf.get_feature_names())
    return out, feature_names

def get_top_tf_idf_words(response, top_n, feature_names):
    sorted_nzs = np.argsort(response.data)[:-(top_n+1):-1]
    return feature_names[response.indices[sorted_nzs]]



def main():
    """Summarizing app"""

    st.title('Medium Post Summarizer')
    # st.subheader('using Extractive method')
    # <h2> Summarizer ML App</h2>

    html_temp = """
    <div style="background-color:skyblue;padding:15px">
    <h2> About Summarizer ML App</h2>
    <p> This <b>Extractive Summarizer</b> give about 10-sentence highlights of an article as well as keywords used. Just enough to help you decide if you want to read more or not. Works best on medium posts</p>
    </div>
    <br>
    """

    st.markdown(html_temp, unsafe_allow_html=True)

    url = st.text_input("Enter a Medium post URL")
    if st.button("Scrape"):
        if url == '':
            st.error('Please input a url')
        else:
            try :
                message = validate_url(url)
                if message == 'This url does not seem correct. Please paste the correct url':
                    st.error(message)
                elif message == 'This url does not look like it is coming from medium. Please know that this may affect the quality of the highlights of the post so try a medium post link':
                    st.warning(message)
                else:
                   st.text('\n')
                   st.text('\n')
                   head, content = scrape_url(url)
                   summary = summarize(content)
                   out , feature_names = vectorize(content)
                   keywords = [get_top_tf_idf_words(response,5, feature_names ) for response in out]
                   st.text(f'\n\n\n')
                   st.text(f'Title : {head}')
                   st.info(summary)
                   st.warning(f'Keywords : {keywords[0][0]}, {keywords[0][1]}, {keywords[0][2]}, {keywords[0][3]}, {keywords[0][4]}')
            except:
                st.error('Check what you pasted')



        # else:
        # message = validate_url(url)
        # if message == error:
        #     st.error(message)
        # elif message == warning:
        #     st.warning(message)
        # else:

        # head, content = scrape_url(url)
        # summary = summarize(content)
        # out , feature_names = vectorize(content)
        # keywords = [get_top_tf_idf_words(response,5, feature_names ) for response in out]
        # st.text(f'\n\n\n')
        # st.text(f'Title : {head}')
        # st.info(summary)
        # st.warning(f'Keywords : {keywords[0][0]}, {keywords[0][1]}, {keywords[0][2]}, {keywords[0][3]}, {keywords[0][4]}')
        # st.markdown()
        # st.text('Please check the link again')
    if st.button("Thanks"):
        st.balloons()








if __name__ == '__main__':
    main()
