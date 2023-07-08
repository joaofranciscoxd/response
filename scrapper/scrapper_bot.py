import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import os
import logging
from datetime import datetime
from scrapper.database import Base, Fact, PreviewLink, FeaturedImage


def configure_logger():
    '''
    Configures the logger.
    '''
    logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

class RequestError(ConnectionError):
    pass

def send_get_request(url):
    '''
    Sends a GET request to the specified URL 
    and returns the response.
    '''
    try:
        response = requests.get(url)
    except:
        logging.info('Error in request function.')
        raise RequestError("Could not return any reponse.Check for any connection problem or blocking.")
    return response

def parse_wikipedia_page(response):
    '''
    Parses the HTML content of the Wikipedia page using BeautifulSoup 
    and returns the parsed soup object.
    '''
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

def extract_facts(soup):
    '''
    Extracts the facts, preview links, and featured images from the parsed soup object 
    and returns them as a list of dictionaries.
    '''
    facts = []
    did_you_know_section = soup.find("div", {"id": "mp-dyk"})
    for index, fact_item in enumerate(did_you_know_section.find_all("li")):
        fact_content = fact_item.text.strip()
        preview_links = []
        for link in fact_item.find_all("a"):
            preview_content = link.get("title")
            preview_url = "https://en.wikipedia.org" + link.get("href")
            preview_links.append({"content": preview_content, "url": preview_url})
        featured_image = None
        if index == 0:
            element = did_you_know_section.find_all("a")
            if len(element) != 0:
                image_element = element[0]
                if image_element and "image" in image_element.get("class", []):
                    image_url = "https://en.wikipedia.org" + image_element.get("href")
                    image_caption = image_element.get("title")
                    featured_image = {"url": image_url, "caption": image_caption}
        facts.append({"content": fact_content, "preview_links": preview_links, "featured_image": featured_image})
    return facts

def exclude_archived_facts(facts):
    '''
    Excludes the archived facts from the list of facts
    and returns the filtered list.
    '''
    facts_data = []
    found_archive = False
    for fact in facts:
        if found_archive:
            break
        if 'Archive' in fact['content']:
            found_archive = True
        else:
            facts_data.append(fact)
    return facts_data

def create_database_tables(engine):
    '''
    Creates the necessary database tables based on the SQLAlchemy models.
    '''   
    Base.metadata.create_all(engine)

def store_facts_in_database(facts_data, session):
    '''
    Stores the facts data in the database by creating or updating existing facts.
    '''
    for fact_data in facts_data:
        existing_fact = session.query(Fact).filter(Fact.content == fact_data["content"]).first()
        if existing_fact:
            existing_fact.preview_links = []
            fact = existing_fact
        else:
            fact = Fact(content=fact_data["content"])
        
        for preview_link_data in fact_data["preview_links"]:
            existing_link = session.query(PreviewLink).filter(PreviewLink.url == preview_link_data["url"]).first()
            if existing_link:
                preview_link = existing_link
            if not existing_link:
                preview_link = PreviewLink(url=preview_link_data["url"])
            fact.preview_links.append(preview_link)
        
        featured_image_data = fact_data["featured_image"]
        if featured_image_data:
            existing_image = session.query(FeaturedImage).filter(FeaturedImage.image_url == featured_image_data["url"]).first()
            if existing_image:
                featured_image = existing_image
            if not existing_image:
                featured_image = FeaturedImage(
                    image_url=featured_image_data["url"],
                    caption=featured_image_data["caption"]
                )
            fact.featured_image = featured_image
            
        session.add(fact)



def scrape_wikipedia():
    configure_logger()
    logging.info('Web scraping started.')
    response = send_get_request("https://en.wikipedia.org/wiki/Main_Page")
    soup = parse_wikipedia_page(response)
    facts = extract_facts(soup)
    facts_data = exclude_archived_facts(facts)
    
    database_file = "wiki_data.db"
    database_exists = os.path.isfile(database_file)
    engine = create_engine(f"sqlite:///{database_file}")
    if not database_exists:
        # Create the tables if the database doesn't exist
        Base.metadata.create_all(engine)
        logging.info('Database created.')
    Session = sessionmaker(bind=engine)
    session = Session()

    store_facts_in_database(facts_data, session)
    session.commit()

    session.close_all()

    logging.info('Web scraping completed.')