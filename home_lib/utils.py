import requests
import json
from langcodes import standardize_tag
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

# Check API of this website https://www.abebooks.com/

GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')


def find_by_isbn_google_books(isbn):
    response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}&key={GOOGLE_API_KEY}')
    response_code = response.status_code
    response = response.json()

    if response_code == 200 and response['totalItems'] > 0:
        book = dict()
        book['title'] = response['items'][0]['volumeInfo']['title']
        book['authors'] = response['items'][0]['volumeInfo']['authors']
        book['isbn10'] = response['items'][0]['volumeInfo']['industryIdentifiers'][0]
        return response
    return


def find_by_isbn_open_library(isbn):
    book = dict()

    # Two urls need to be checked because in the first, supposedly more detailed route, language data is missing
    # and sometimes some other fields too
    urls = [
        f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json',
        f'https://openlibrary.org/isbn/{isbn}.json'
    ]

    resp_dict = [
        "response.json()[f'ISBN:{isbn}']",
        "response.json()"
    ]

    string_methods = dict()
    string_methods['title'] = "response.get('title')"
    string_methods['authors'] = "response.get('authors')[0].get('name')"
    string_methods['year'] = "response.get('publish_date').split(' ')[-1]"
    string_methods['isbn13'] = "response.get('identifiers').get('isbn_13')[0]"
    string_methods['img_small'] = "response.get('cover').get('small')"
    string_methods['img_medium'] = "response.get('cover').get('medium')"
    string_methods['language'] = "standardize_tag(response.get('languages')[0].get('key').split('/')[-1])"

    for i in range(2):
        response = requests.get(urls[i])
        response_code = response.status_code
        if response_code == 200:
            if response.json():
                response = eval(resp_dict[i])
                # Catch error raised due to inconsistent json scheme (missing dict keys), f.ex. isbn_10
                for k, v in string_methods.items():
                    # Check if the key exists and if it does check if its value is None
                    if not book.get(k):
                        try:
                            book[k] = eval(v)
                        except (TypeError, AttributeError) as e:
                            book[k] = None
    return book


LANGUAGE_CHOICES = [
    ('ab', 'Abkhazian'),
    ('af', 'Afrikaans'),
    ('sq', 'Albanian'),
    ('ar', 'Arabic'),
    ('hy', 'Armenian'),
    ('az', 'Azerbaijani'),
    ('be', 'Belarusian'),
    ('bs', 'Bosnian'),
    ('br', 'Breton'),
    ('bg', 'Bulgarian'),
    ('cs', 'Czech'),
    ('ce', 'Chechen'),
    ('zh', 'Chinese'),
    ('cu', 'Church Slavic; Old Slavonic; Church Slavonic; Old Bulgarian; Old Church Slavonic'),
    ('cy', 'Welsh'),
    ('cs', 'Czech'),
    ('da', 'Danish'),
    ('de', 'German'),
    ('nl', 'Dutch; Flemish'),
    ('el', 'Greek, Modern (1453-)'),
    ('en', 'English'),
    ('eo', 'Esperanto'),
    ('et', 'Estonian'),
    ('eu', 'Basque'),
    ('fo', 'Faroese'),
    ('fa', 'Persian'),
    ('fi', 'Finnish'),
    ('fr', 'French'),
    ('Ga', 'Georgian'),
    ('de', 'German'),
    ('gd', 'Gaelic; Scottish Gaelic'),
    ('ga', 'Irish'),
    ('gl', 'Galician'),
    ('gn', 'Guarani'),
    ('gu', 'Gujarati'),
    ('ht', 'Haitian; Haitian Creole'),
    ('he', 'Hebrew'),
    ('hi', 'Hindi'),
    ('hr', 'Croatian'),
    ('hu', 'Hungarian'),
    ('is', 'Icelandic'),
    ('id', 'Indonesian'),
    ('is', 'Icelandic'),
    ('it', 'Italian'),
    ('jv', 'Javanese'),
    ('ja', 'Japanese'),
    ('kl', 'Kalaallisut; Greenlandic'),
    ('kk', 'Kazakh'),
    ('ky', 'Kirghiz; Kyrgyz'),
    ('kg', 'Kongo'),
    ('ko', 'Korean'),
    ('ku', 'Kurdish'),
    ('la', 'Latin'),
    ('lv', 'Latvian'),
    ('lt', 'Lithuanian'),
    ('lb', 'Luxembourgish; Letzeburgesch'),
    ('mk', 'Macedonian'),
    ('mi', 'Maori'),
    ('mk', 'Macedonian'),
    ('mg', 'Malagasy'),
    ('mt', 'Maltese'),
    ('mn', 'Mongolian'),
    ('ms', 'Malay'),
    ('na', 'Nauru'),
    ('nv', 'Navajo; Navaho'),
    ('ne', 'Nepali'),
    ('nl', 'Dutch; Flemish'),
    ('nn', 'Norwegian Nynorsk; Nynorsk, Norwegian'),
    ('nb', 'Bokmål, Norwegian; Norwegian Bokmål'),
    ('no', 'Norwegian'),
    ('os', 'Ossetian; Ossetic'),
    ('pa', 'Panjabi; Punjabi'),
    ('fa', 'Persian'),
    ('pl', 'Polish'),
    ('pt', 'Portuguese'),
    ('ps', 'Pushto; Pashto'),
    ('qu', 'Quechua'),
    ('rm', 'Romansh'),
    ('ro', 'Romanian; Moldavian; Moldovan'),
    ('ru', 'Russian'),
    ('sa', 'Sanskrit'),
    ('sk', 'Slovak'),
    ('sl', 'Slovenian'),
    ('so', 'Somali'),
    ('es', 'Spanish; Castilian'),
    ('sr', 'Serbian'),
    ('su', 'Sundanese'),
    ('sw', 'Swahili'),
    ('sv', 'Swedish'),
    ('ta', 'Tamil'),
    ('tt', 'Tatar'),
    ('tl', 'Tagalog'),
    ('th', 'Thai'),
    ('bo', 'Tibetan'),
    ('tk', 'Turkmen'),
    ('tr', 'Turkish'),
    ('ug', 'Uighur; Uyghur'),
    ('uk', 'Ukrainian'),
    ('ur', 'Urdu'),
    ('uz', 'Uzbek'),
    ('vi', 'Vietnamese'),
    ('cy', 'Welsh'),
    ('wa', 'Walloon'),
    ('yi', 'Yiddish'),
    ('za', 'Zhuang; Chuang'),
    ('zh', 'Chinese'),
    ('zu', 'Zulu')
]

