from scrapper.database import Fact
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import spacy
import requests
import re
import datetime
from scrapper.database import Fact
import logging
import warnings
warnings.filterwarnings("ignore")

engine = create_engine("sqlite:///wiki_data.db")
Session = sessionmaker(bind=engine)
session = Session()

def configure_logger():
    '''
    Configures the logger.
    '''
    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

def analyze_and_suggest():
    configure_logger()
    logging.info('Starting to analyze.')
    '''Retrieve the newly scraped facts from the database
    '''
    new_facts = session.query(Fact).filter(Fact.analyzed == False).all()

    '''Perform analysis and generate suggestions
    '''
    for fact in new_facts:
        internal_links = generate_internal_links(fact)
        campaign_parameters = generate_campaign_parameters(fact)

        '''Update the fact in the database with the suggestions
        '''
        fact.internal_links = str(internal_links)[1:-1]
        fact.campaign_parameters = str(campaign_parameters)
        fact.analyzed = True

        '''Commit the changes to the database an close session
        '''
        session.add(fact)
    session.commit()
    session.close_all()
    logging.info('Finished to analyze.')

def generate_internal_links(fact):
    '''Extract relevant keywords or topics from the fact content
    '''
    keywords = extract_keywords(fact.content)

    '''Generate internal links based on article categories and keyword matching
    '''
    internal_links = []
    for keyword in keywords:
        related_articles = find_related_articles(keyword)
        internal_links.extend(related_articles)

    return internal_links

def generate_campaign_parameters(fact):
    '''Generate campaign parameters based on fact metadata or tags
    '''
    metadata = extract_metadata(fact)
    campaign_parameters = {}

    '''Generate campaign parameters based on temporal relevance
    '''
    if metadata['temporal_relevance']:
        campaign_parameters['date'] = metadata['date']

    '''Generate campaign parameters based on fact length
    '''
    if metadata['fact_length']:
        campaign_parameters['length'] = metadata['fact_length']

    return campaign_parameters

def extract_keywords(content):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(content.replace('... ',''))
    
    '''Filter out stopwords and punctuation
    '''
    keywords = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    
    return sorted(list(set(keywords)))

def find_related_articles(keyword):
    base_url = "https://en.wikipedia.org/w/api.php"

    '''Set parameters for the API request. Limit the number of search results
    '''
    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": keyword,
        "srlimit": 5
    }

    '''Send the API request
    '''
    response = requests.get(base_url, params=params)
    data = response.json()

    '''Extract the page titles from the search results
    '''
    titles = [result["title"] for result in data["query"]["search"]]

    '''Generate internal links by appending the titles to the Wikipedia URL
    '''
    internal_links = [f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}" for title in titles]
    
    return internal_links


def extract_metadata(fact):
    metadata = {}

    '''Extract temporal relevance metadata
    '''
    metadata['temporal_relevance'] = check_temporal_relevance(fact)
    metadata['date'] = get_date(fact)

    '''Extract fact length metadata
    '''
    metadata['fact_length'] = get_fact_length(fact)

    return metadata

def check_temporal_relevance(fact):
    '''Perform logic to check if the fact is temporally relevant
    '''
    '''Checks if the fact mentions a specific year or date
    '''
    '''Return True if relevant, False otherwise
    '''

    '''Example: Check if the fact contains a year between years from 1800 to 2023
    '''
    year_pattern = r"\b(18\d{2}|19\d{2}|20[01]\d|202[0-2]|2023)\b"
    if re.search(year_pattern, fact.content):
        return True
    else:
        return False
    
def get_date(fact):
    '''
    Extract the date from the fact content if it follows a specific format
    '''
    date_pattern = r"\b(\d{4}-\d{2}|\d{4})\b"

    match = re.search(date_pattern, fact.content)
    if match:
        date_str = match.group(0)
        if len(date_str) == 4:
            # Only the year is mentioned, complete with month and day
            date_str += "-01-01"
        elif len(date_str) == 7:
            # Year and month are mentioned, complete with day
            date_str += "-01"
        return datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    else:
        return None


    
def get_fact_length(fact):
    '''Calculate the length of the fact content
    '''
    words = fact.content.split()
    return len(words)

