from bs4 import BeautifulSoup

def create_soup(content):
    return BeautifulSoup(content, "html.parser")

def select(content, selection=None):
    soup = create_soup(content)
    return soup.select(selection) if selection else soup

def find_all(content, selection):
    return create_soup(content).find_all(selection)

def find_all_(content, selection):
    return create_soup(content).find_all(*selection)

def find(content, selection):
    return create_soup(content).find(*selection)
