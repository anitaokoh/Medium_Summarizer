# Medium Summarizer App

This is a web app that scrapes medium post get inputting the post url, sumarizes it into 5- 10 sentences using the extractive summarization method , get 5 keywords in the articles based on importance(not frequency) using TFIDF and then outputs the summary and the keywords.

**Some of the tools used**
- App framework tools like Streamlit(first attempt), Heroku
- Extractive summarization tool like Sumy(LSA model)
- Webscraping libraries like BeautifulSoup and Requests
- URL verification library like TldExtract
- Text preprocessing libraries like Spacy(heavy duty), Sumy
- Text vectorization library like TFIDFVectorizer and CountVectorizer in Scikit-learn
- Others like HTML etc

_The most difficult part was trying to understand the algorithm behind the summarization model and using Streamlit to wrap all the components together._

**Here is a demo of the app** 


_You can find the link to the app here_

**Further improvements to be done are**
- Moving from extractive summarizer to abstractive summarizer
- Improvemnet in building a good summarizer from scratch
- Improvement on the scraping part as well as the interface.


_Feel free to go through my [draft_work](https://github.com/anitaokoh/Medium_summarizer/tree/master/scratch_work) and [jupyter_notebooks](https://github.com/anitaokoh/Medium_summarizer/tree/master/work_book)
