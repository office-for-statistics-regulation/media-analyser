## Media Analyser

This Media analyser has been developed by the Office for Statistical Regulation (OSR) to help track important media articles relating to our [domains](https://osr.statisticsauthority.gov.uk/what-we-do/our-domains/). We extract media article titles and links using Google News, Bing News and newscatcher. Note: Google News will block you if you automate this process. As a result, we only automate the Bing News and newscatcher services as they provide free-tier API access.

### Getting
To clone locally use:

`git clone https://github.com/office-for-statistics-regulation/media-analyser`

### Setting
To install requirements cd to the cloned folder and use:

`pip install -r requirements.txt`

Please enter you [Bing News](https://www.microsoft.com/en-us/bing/apis/bing-news-search-api) and/or [newscatcher](https://rapidapi.com/newscatcher-api-newscatcher-api-default/api/newscatcher) credentials to `credentials_EMPTY.py` and rename to credentials.py. Do not push this information to a public place! .gitignore should prevent this from happening.

Edit `config.py` with your desired search terms and which APIs you want to use.

### Using
To run:

`python get-media.py`

This will save the tweets to outputs/<api_name><search_term>.csv.

### How we use the data
We collect media articles to check the use of statistics within the media in our working [domains](https://osr.statisticsauthority.gov.uk/what-we-do/our-domains/) areas. Currently we just store the article title, link and other metadata and not the article text. Our next stage will be to extract text from the articles.




