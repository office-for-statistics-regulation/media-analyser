from pygooglenews import GoogleNews
import pandas as pd
import requests
import json
import re

import credentials
import config


def googleNewsSearch(search_terms):
	gn = GoogleNews(lang='en', country='GB')
	search = gn.search(search_terms)
	results = search['entries']
	df = pd.DataFrame(columns=['Title', 'Link', 'Published_Date', 'Publisher', 'id', 'rank'])
	r = 1
	for result in results:
		if result.source.title != 'GOV.UK':
			df = df.append({'Title': result.title,
							'Link': result.link,
							'Published_Date': result.published,
							'Publisher': result.source.title,
							'id': result.id,
							'rank': r}, ignore_index=True)
			r += 1

	return df


def bingNewsSearch(search_terms):
	search_url = 'https://api.bing.microsoft.com/v7.0/news/search'
	headers = {'Ocp-Apim-Subscription-Key': credentials.subscription_key}
	params = {'q': search_terms, 'textDecorations': True, 'textFormat': 'HTML', 'cc': 'en-GB'}
	response = requests.get(search_url, headers=headers, params=params)
	response.raise_for_status()
	search_results = json.dumps(response.json())
	results = json.loads(search_results)
	df = pd.DataFrame(columns=['Title', 'Link', 'Published_Date', 'Publisher', 'id', 'rank'])
	r = 1
	for result in results['value']:
		df = df.append({'Title': re.sub('<[^<]+?>', '', result['name']),
						'Link': result['url'],
						'Published_Date': result['datePublished'][0:10],
						'Publisher': result['provider'][0]['name'],
						'id': result['url'].split('/')[-1],
						'rank': r}, ignore_index=True)
		r += 1
	return df


def newscatcherSearch(search_terms):
	df = pd.DataFrame(columns=['Title', 'Link', 'Published_Date', 'Publisher', 'id', 'rank'])
	r = 1

	search_url = 'https://newscatcher.p.rapidapi.com/v1/search'
	headers = {'x-rapidapi-key': credentials.newscatcher_key, 'x-rapidapi-host': 'newscatcher.p.rapidapi.com'}

	for i in range(1, 3):
		params = {'q': search_terms, 'lang': 'en', 'sort_by': 'relevancy', 'page': str(i), 'media': 'True',
				  'country': 'GB'}
		response = requests.get(search_url, headers=headers, params=params)
		response.raise_for_status()
		search_results = json.dumps(response.json())
		results = json.loads(search_results)

		for result in results['articles']:
			df = df.append({'Title': result['title'],
							'Link': result['link'],
							'Published_Date': result['published_date'][0:10],
							'Publisher': result['rights'],
							'id': result['_id'],
							'rank': r}, ignore_index=True)
			r += 1
	return df


def run(search_terms):

	if config.googleNews == True:
		google_df = googleNewsSearch(search_terms)
		google_df.to_csv(f'outputs/google_{search_terms}.csv')
	if config.bingNews == True:
		bing_df = bingNewsSearch(search_terms)
		bing_df.to_csv(f'outputs/bing_{search_terms}.csv')
	if config.newscatcherNews == True:
		newscatcher_df = newscatcherSearch(search_terms)
		newscatcher_df.to_csv(f'outputs/newscatcher_{search_terms}.csv')


if __name__ == "__main__":
	run(config.search_terms)
