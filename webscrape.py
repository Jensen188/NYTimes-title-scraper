import requests
from bs4 import BeautifulSoup
import nltk 
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt

#Download the required modules
nltk.download('punkt')
nltk.download('stopwords')

if __name__ == "__main__":
    url="https://www.nytimes.com/section/world"
    r=requests.get(url)
    r_content=r.content

## if connected
    try:
        if r.status_code==200:
            soup=BeautifulSoup(r_content,"html.parser")
            head_news = soup.find_all("h3",class_="css-1ykb5sd e1hr934v2")
            other_news = soup.find_all("a",class_="css-8hzhxf")
            data=set()

            ## getting titles
            for news_element in head_news:
                news_title=news_element.find("a").get_text(strip=True)
                data.add(news_title)

            for news_element in other_news:
                news_title=news_element.find("h3").get_text(strip=True)
                data.add(news_title)
                
            #go through every page 
            for x in range (1,12):
                latest_news =soup.find_all("h3",class_="css-1j88qqx e15t083i0")
                for news_element in latest_news:
                    news_title=news_element.get_text(strip=True)
                    data.add(news_title)

                r=requests.get(url+"?page="+str(x))
                r_content=r.content
                soup=BeautifulSoup(r_content,"html.parser")

                #Convert set to string 
                text=" ".join(data)
            
                tokens = word_tokenize(text)

                # Remove stopwords
                stop_words = set(stopwords.words('english'))
                filtered_tokens = [word.lower() for word in tokens if word.isalpha() and word.lower() not in stop_words]

            # Frequency Distribution
            freq_dist = FreqDist(filtered_tokens)
            print(freq_dist)
            # Extracting Keywords (replace 5 with the number of top keywords you want)
            top_keywords = freq_dist.most_common(5)
            print("Top Keywords:", top_keywords)

            # Generating WordCloud
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(filtered_tokens))

            # Display WordCloud
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.show()

    except Exception as e:
        print(f"Error while connecting to page: {e}")

        
