import app
import math
# from dotenv import load_dotenv
# load_dotenv()
from helpers import create_csv
# from app import models

from bs4 import BeautifulSoup
from flask_mail import Message

import csv
from datetime import date
import datetime
from io import BytesIO, StringIO
import os
import re
import time
import ssl
import urllib.request as r
ssl._create_default_https_context = ssl._create_unverified_context

# def db_insert_lead(lead):
#     if lead['rooms'] != None and not lead['rooms'].isdigit():
#         lead['rooms'] = None
#     if lead['baths'] != None and not lead['baths'].isdigit():
#         lead['baths'] = None
#     new_lead = find_or_create(
#         db_session, models.SalesLead, 
#         url=lead['url'], rooms=lead['rooms'], 
#         square_feet=lead['square_feet'],
#         baths=lead['baths'], rent=lead['rent'], 
#         buildingType=lead['buildingType'], 
#         inserted_at=lead['inserted_at'],
#         city=lead['city']
#         )
#     if len(lead['numbers']) > 0:
#         for number in lead['numbers']:
#             new_number = find_or_create(
#                 db_session,
#                 models.PhoneNumber,
#                 phone_number=number,
#             )
#             new_slpn = find_or_create(
#                 db_session,
#                 models.SalesLeadPhoneNumber,
#                 sales_lead_id=new_lead.id,
#                 phone_number_id=new_number.id,
#             )
#             db_session.commit()
#     return 'lead inserted'

def get_kijiji_leads():
    leads = []
    all_properties = []
    city_data = [
        {"name": "city-of-toronto", "code": "c37l1700273"},
        {'name': 'etobicoke', 'code': "c37l1700273"},
        {'name': 'scarborough', 'code': "c37l1700273"},
        {'name': 'north-york', 'code': "c37l1700273"},
        {"name": "mississauga-peel-region", "code": "c37l1700276"},
        {"name": "markham-york-region", "code": "c37l1700274"},
        {"name": "vancouver", "code": "c37l1700287"},
        {"name": "richmond-bc", "code": "c37l1700288"},
        {"name": "burnaby-new-westminster", "code": "c37l1700286"},
        {"name": "laval-rive-nord", "code": "c37l1700278"},
        {"name": "longueuil-rive-sud", "code": "c37l1700279"},
        {"name": "calgary", "code": "c30349001l1700199"},
        {"name": "edmonton", "code": "c30349001l1700203"},
        {"name": "winnipeg", "code": "c30349001l1700192"},
        {"name": "hamilton", "code": "c30349001l80014"},
        {"name": "kingston-on", "code": "c30349001l1700183"},
        {"name": "city-of-halifax", "code": "c30349001l1700321"},
        {"name": "ville-de-montreal", "code": "c30349001l1700281"},
        {"name": "ottawa", "code": "c30349001l1700185"},
        {"name": "ville-de-quebec", "code": "c30349001l1700124"},
        {"name": "kitchener-waterloo", "code": "c30349001l1700212"},
        {"name": "london", "code": "c30349001l1700214"},
        {"name": "victoria-bc", "code": "c30349001l1700173"},
        {"name": "oshawa-durham-region", "code": "c30349001l1700275"},
        {"name": "windsor-area-on", "code": "c30349001l1700220"},
        {"name": "saskatoon", "code": "c30349001l1700197"},
        {"name": "st-catharines", "code": "c30349001l80016"},
        {"name": "regina", "code": "c30349001l1700196"},
        {"name": "st-johns", "code": "c30349001l1700113"},
        {"name": "kelowna", "code": "c30349001l1700228"},
        {"name": "barrie", "code": "c30349001l1700006"},
        {"name": "sherbrooke-qc", "code": "c30349001l1700156"},
        {"name": "guelph", "code": "c30349001l1700242"},
        {"name": "abbotsford", "code": "c30349001l1700140"},
        {"name": "trois-rivieres", "code": "c30349001l1700150"},
        {"name": "moncton", "code": "c30349001l1700001"},
        {"name": "saguenay", "code": "c30349001l1700179"},
        {"name": "oakville-halton-region", "code": "c30349001l1700277"},
        {"name": "red-deer", "code": "c30349001l1700136"},
        {"name": "brantford", "code": "c30349001l1700206"},
        {"name": "delta-surrey-langley", "code": "c30349001l1700285"},
        {"name": "nanaimo", "code": "c30349001l1700263"},
        {"name": "lethbridge", "code": "c30349001l1700230"},
        {"name": "peterborough", "code": "c30349001l1700218"},
        {"name": "kamloops", "code": "c30349001l1700227"},
    ]
    for i in range(1,4):
        for url in city_data:
            print('scraping leads in: ', url['name'])
            try:
                if(url['name'] == 'etobicoke'):
                    soup = BeautifulSoup(
                    r.urlopen(f"https://www.kijiji.ca/b-for-rent/city-of-toronto/page-{i}/{url['code']}?ll=43.620495%2C-79.513198&address=Etobicoke%2C+Toronto%2C+ON&radius=7.0"),
                    'html.parser',
                    )
                    all_properties.append('etobicoke')
                    all_properties += soup.findAll("a", {"class": "title"})
                    all_properties.append('')
                elif(url['name'] == 'scarborough'):
                    soup = BeautifulSoup(
                        r.urlopen(f"https://www.kijiji.ca/b-for-rent/city-of-toronto/page-{i}/{url['code']}?ll=43.776426%2C-79.231752&address=Scarborough%2C+Toronto%2C+ON&radius=7.0"),
                        'html.parser',
                    )
                    all_properties.append('scarborough')
                    all_properties += soup.findAll("a", {"class": "title"})
                    all_properties.append('')
                elif(url['name'] == 'north-york'):
                    soup = BeautifulSoup(
                        r.urlopen(f"https://www.kijiji.ca/b-for-rent/city-of-toronto/page-{i}/{url['code']}?ll=43.761538%2C-79.411079&address=North+York%2C+Toronto%2C+ON&radius=7.0"),
                        'html.parser',
                    )
                    all_properties.append('north-york')
                    all_properties += soup.findAll("a", {"class": "title"})
                    all_properties.append('')
                elif(url['name'] == 'city-of-toronto'):
                    soup = BeautifulSoup(
                        r.urlopen(f"https://www.kijiji.ca/b-for-rent/city-of-toronto/page-{i}/{url['code']}?ll=43.653226%2C-79.383184&address=Toronto%2C+ON&radius=7.0"),
                        'html.parser',
                    )
                    all_properties.append('city-of-toronto')
                    all_properties += soup.findAll("a", {"class": "title"})
                    all_properties.append('')
                else:
                    soup = BeautifulSoup(
                        r.urlopen(f"https://www.kijiji.ca/b-for-rent/{url['name']}/page-{i}/{url['code']}"),
                        'html.parser',
                    )
                    all_properties += soup.findAll("a", {"class": "title"})
            except Exception as e:
                print('this is what errored: ', e, url['name'], url['code'])
    region = None
    for i in range(len(all_properties)):
        if all_properties[i] == 'etobicoke':
            region = 'e'
            continue
        elif all_properties[i] == 'city-of-toronto':
            region = 't'
            continue
        elif all_properties[i] == 'north-york':
            region = 'n'
            continue
        elif all_properties[i] == 'scarborough':
            region = 's'
            continue
        elif all_properties[i] == '':
            region = None
            continue
        try:
            lead = {
                'numbers': [],
                'url': f"https://www.kijiji.ca{all_properties[i]['href']}"
            }
            flag=False
            while not flag:
                soup = BeautifulSoup(r.urlopen(f"{lead['url']}?siteLocale=en_CA"), 'html.parser')
                if len(soup.body) == 0:
                    import time
                    time.sleep(25)
                    print("waiting...", i, lead['url'])
                else:
                    flag=True
            if soup.find('div', {'class': 'titleAttributes-2381855425'}) != None:
                lead['buildingType'] = soup.select('div.titleAttributes-2381855425')[0].find_all('li')[0].span.text
            else:
                lead['buildingType'] = None
            if soup.find('div', {'class': 'titleAttributes-2381855425'}) != None:
                lead['rooms'] = soup.select('div.titleAttributes-2381855425')[0].find_all('li')[1].span.text[-1]
            elif soup.find('dt', string='Bedrooms') != None:
                lead['rooms'] = soup.find('dt', string='Bedrooms').find_next('dd').find_next('dd').text[-1]
            else:
                lead['rooms'] = None
            if soup.find('div', {'class': 'titleAttributes-2381855425'}) != None:
                lead['baths'] = soup.select('div.titleAttributes-2381855425')[0].find_all('li')[2].span.text
            elif soup.find('dt', string='Bathrooms') != None:
                lead['baths'] = soup.find('dt', string='Bathrooms').find_next('dd').find_next('dd').text
            else:
                lead['baths'] = None
            if soup.find('div', {'class': 'priceWrapper-1165431705'}) == None:
                if soup.find('div', {'class': 'priceContainer-1419890179'}) == None:
                    lead['rent'] = None
                else:
                    lead['rent'] = soup.find('div', {'class': 'priceContainer-1419890179'}).span.span.text.replace(".00", "")
            else:
                if soup.find('div', {'class': 'priceWrapper-1165431705'}).span.text != None:
                    lead['rent'] = soup.find('div', {'class': 'priceWrapper-1165431705'}).span.text.replace(".00", "") 
                elif soup.find('div', {'class': 'priceWrapper-1165431705'}).span.font != None:
                    lead['rent'] = soup.find('div', {'class': 'priceWrapper-1165431705'}).span.font.font.text.replace(".00", "") 
                else:
                    lead['rent'] = None
            if lead['rent'] != None:
                lead['rent'] = lead['rent'].replace("$", "").replace(" ", "")
                if lead['rent'][-3:] == ",00":
                    lead['rent'] = lead['rent'][:-3]
                lead['rent'] = lead['rent'].replace(",", "").replace(" ", "").replace(u'\xa0', "")
                if lead['rent'].isdigit(): lead['rent'] = int(lead['rent'])
                else: lead['rent'] = None
            if soup.find('div', {'class': 'locationContainer-2867112055'}) != None:
                lead['address'] = soup.find('div', {'class': 'locationContainer-2867112055'}).span.text
            else:
                lead['address'] = None
            lead['inserted_at'] = datetime.datetime.utcnow()
            if soup.find('div', {'class': 'descriptionContainer-3261352004'}).div != None:
                description = soup.find('div', {'class': 'descriptionContainer-3261352004'}).div
                split = [re.sub('[\)\(\-]', '', i) for i in re.sub('[<\>\.]', ' ', str(description)).split()]
            else:
                description = []
            if(region == 'e'): 
                lead['city'] = 'etobicoke'
            elif(region == 's'): 
                lead['city'] = 'scarborough'
            elif(region == 'n'): 
                lead['city'] = 'north-york'
            elif(region == 't'): 
                lead['city'] = 'city-of-toronto'
            else: 
                lead['city'] = lead['url'].split('/')[4]
            
            if len(soup.find_all('div', {'class': 'attributeCard-1535740193'})) > 1:
                lead['square_feet'] = soup.find_all('div', {'class': 'attributeCard-1535740193'})[1].ul.find_all('li')[0].dl.dd.text
                lead['square_feet'] = lead['square_feet'].replace(',', '').replace(' ', '').replace('.', '')
                if lead['square_feet'] == '1' or not lead['square_feet'].isdigit():
                    lead['square_feet'] = None
            else:
                lead['square_feet'] = None
        except Exception as e:
            print("The error was:", e)
            print('this is what errored:', all_properties[i], i)
    leads = [{'city': 'Toronto', 'Address': '123 gay st', 'url':'https://www.google.com', 'rooms': 4, 'rent': 1234, 'buildingType':'House', 'square_feet': 123, 'inserted_at':datetime.datetime.utcnow()}]
    csv_detailed_leads = create_csv(
        ['city', 'Address', 'Url', 'Rooms', 'Price', 'Building Type', 'Square Feet', 'Inserted at'],
        [[i['city'], i.get('address'), i['url'], i['rooms'], i['rent'], i['buildingType'], i['square_feet'], i['inserted_at']] for i in leads if i['rooms'] and i['rent'] and i['buildingType'] and i['square_feet']]
    )
    todays_date = date.today().strftime("%d/%m/%Y")
    csvfile = StringIO()
    csvwriter = csv.writer(csvfile)
    for i in csv_detailed_leads:
        csvwriter.writerow(i)
    with app.app.app_context():
        msg = Message(
                f"Singlekey Kijiji Sales Leads for {todays_date}",
                sender=os.environ['GMAIL_ACCOUNT'],
                recipients=['seb7wake@gmail.com'],
            )
        msg.attach(
                f"detailed_leads_for_{todays_date}.csv", "text/csv", csv_detailed_leads.getvalue()
            )
        app.mail.send(msg)
    print('email to dev team')

def get_padmapper_leads():
    leads = []
    all_properties=[]
    cities = [
        "Thttps://www.padmapper.com/apartments/toronto-on?sort=newest&max-days=3&box=-79.4605435,43.6262675,-79.2817466,43.7400758",
        'Ehttps://www.padmapper.com/apartments/toronto-on?sort=newest&max-days=3&box=-79.6189628,43.5998434,-79.4503642,43.7072133',
        'Shttps://www.padmapper.com/apartments/toronto-on?sort=newest&max-days=3&box=-79.3793099,43.7009853,-79.0629883,43.9019335',
        'Nhttps://www.padmapper.com/apartments/toronto-on?sort=newest&max-days=3&box=-79.437066,43.7081059,-79.2525564,43.8253867',
        "https://www.padmapper.com/apartments/mississauga-on?sort=newest&max-days=3&box=-80.06629943847656,43.51619059561274,-79.28352355957031,43.71106791821883",
        "https://www.padmapper.com/apartments/markham-on?sort=newest&max-days=3&box=-79.46685791015625,43.76216815555818,-79.16885375976562,43.95130472827632",
        "https://www.padmapper.com/apartments/vancouver-bc?sort=newest&max-days=3&box=-123.29269409179688,49.15487827243112,-122.99468994140625,49.33888168149418",
        'https://www.padmapper.com/apartments/richmond-bc?sort=newest&max-days=3&box=-123.24085235595703,49.08623417811704,-122.9428482055664,49.25772233075704',
        'https://www.padmapper.com/apartments/burnaby-bc?sort=newest&max-days=3&box=-123.1076431274414,49.152520559304264,-122.80963897705078,49.32377937629472',
        'https://www.padmapper.com/apartments/laval-qc?sort=newest&max-days=3&box=-73.9984130859375,45.42255200704734,-73.40240478515625,45.78955188566187',
        'https://www.padmapper.com/apartments/longueuil-qc?sort=newest&max-days=3&box=-73.59260559082031,45.415322477757584,-73.29460144042969,45.599146119878384',
        "https://www.padmapper.com/apartments/edmonton-ab?sort=newest&max-days=3&box=-113.78711700439453,53.39725097813456,-113.20003509521484,53.697519537449374",
        "https://www.padmapper.com/apartments/calgary-ab?sort=newest&max-days=3&box=-114.3838119506836,50.85971044158446,-113.7967300415039,51.177621156752494",
        "https://www.padmapper.com/apartments/winnipeg-mb?sort=newest&max-days=3&box=-97.4435806274414,49.703611804493306,-96.85649871826172,50.02935766319773",
        "https://www.padmapper.com/apartments/hamilton-on?sort=newest&max-days=3&box=-80.1723861694336,43.049321576177284,-79.5853042602539,43.4175176458317",
        "https://www.padmapper.com/apartments/kingston-on?sort=newest&max-days=3&box=-76.50460481643677,44.22121470199021,-76.46791219711304,44.24384631410915",
        "https://www.padmapper.com/apartments/halifax-ns?sort=newest&max-days=3&box=-63.6861262,44.5875614,-63.4721257,44.7186078",
        "https://www.padmapper.com/apartments/victoria-bc?sort=newest&max-days=3&box=-123.393987,48.402595,-123.315834,48.450464",
        "https://www.padmapper.com/apartments/oshawa-on?sort=newest&max-days=3&box=-78.9059405,43.851947,-78.800533,43.961309",
        "https://www.padmapper.com/apartments/windsor-on?sort=newest&max-days=3&box=-83.091032,42.251065,-82.895456,42.343049",
        "https://www.padmapper.com/apartments/montreal-qc?sort=newest&max-days=3&box=-73.947666,45.414663,-73.476198,45.704299",
        'https://www.padmapper.com/apartments/ottawa-on?sort=newest&max-days=3&box=-76.3573669,44.967174,-75.247642,45.528544',
        "https://www.padmapper.com/apartments/quebec-qc?sort=newest&max-days=3&box=-71.4890791,46.747745,-71.169858,46.9562333",
        "https://www.padmapper.com/apartments/waterloo-on?sort=newest&max-days=3&box=-80.623629,43.432526,-80.480983,43.526278",
        "https://www.padmapper.com/apartments/london-on?sort=newest&max-days=3&box=-81.369029,42.918082,-81.132438,43.060633",
        "https://www.padmapper.com/apartments/saskatoon-sk?sort=newest&max-days=3&box=-106.7672028,52.069697,-106.539042,52.1897099",
        "https://www.padmapper.com/apartments/st-catharines-on?sort=newest&max-days=3&box=-79.3208386466293,43.104578488916,-79.1774444158111,43.2482105674397",
        "https://www.padmapper.com/apartments/regina-sk?sort=newest&max-days=3&box=-104.709767,50.3966587,-104.5113979,50.5091863", 
        "https://www.padmapper.com/apartments/st-john's-nl?sort=newest&max-days=3&box=-53.0378682465712,47.3307832067435,-52.6194085039606,47.6340067805987",
        "https://www.padmapper.com/apartments/kelowna-bc?sort=newest&max-days=3&box=-119.537272,49.781233,-119.342996,49.970334",
        "https://www.padmapper.com/apartments/barrie-on?sort=newest&max-days=3&box=-79.745636,44.318188,-79.602103,44.425795",
        "https://www.padmapper.com/apartments/sherbrooke-qc?sort=newest&max-days=3&box=-71.970318,45.34453,-71.8185179,45.453297",
        "https://www.padmapper.com/apartments/guelph-on?sort=newest&max-days=3&box=-80.3271214,43.49376,-80.171171,43.587955", 
        "https://www.padmapper.com/apartments/abbotsford-bc?sort=newest&max-days=3&box=-122.460156,49.0023765,-122.183221,49.142423",
        "https://www.padmapper.com/apartments/trois-rivieres-qc?sort=newest&max-days=3&box=-72.6506258,46.310004,-72.5300174,46.3991621",
        "https://www.padmapper.com/apartments/moncton-nb?sort=newest&max-days=3&box=-64.884268,46.065489,-64.685619,46.132895",
        "https://www.padmapper.com/apartments/saguenay-qc?sort=newest&max-days=3&box=-71.486706,48.236914,-70.70431,48.503736",
        "https://www.padmapper.com/apartments/oakville-on?sort=newest&max-days=3&box=-79.797134,43.37168,-79.624986,43.522772",
        "https://www.padmapper.com/apartments/red-deer-ab?sort=newest&max-days=3&box=-113.861624,52.230158,-113.742331,52.317562",
        "https://www.padmapper.com/apartments/brantford-on?sort=newest&max-days=3&box=-80.3288671,43.1018656,-80.1942212,43.1936027",
        "https://www.padmapper.com/apartments/lethbridge-ab?sort=newest&max-days=3&box=-112.914631,49.650883,-112.773778,49.734862",
        "https://www.padmapper.com/apartments/surrey-bc?sort=newest&max-days=3&box=-122.919972,49.002256,-122.679052,49.206734",
        "https://www.padmapper.com/apartments/nanaimo-bc?sort=newest&max-days=3&box=-124.051672,49.085425,-123.909906,49.231442",
        "https://www.padmapper.com/apartments/peterborough-on?sort=newest&max-days=3&box=-78.381858,44.258262,-78.299706,44.343177",
        "https://www.padmapper.com/apartments/kamloops-bc?sort=newest&max-days=3&box=-120.473361,50.615508,-120.054227,50.782523"
    ]
    for city in cities:
        if(city[0].isupper()):
            soup = BeautifulSoup(r.urlopen(city[1:]), 'html.parser')
        else:
            soup = BeautifulSoup(r.urlopen(city), 'html.parser')
        try:
            all_properties = soup.find_all('a', {'class': 'ListItemMobile_bubbleLink__3bC_L'})
        except:
            print('No listings were found in this city')
        for i in range(len(all_properties)):
            lead = {
                'url': f"https://www.padmapper.com{all_properties[i]['href']}",
            }
            try:
                soup = BeautifulSoup(r.urlopen(lead['url']), 'html.parser')
                if soup.find('div', {'class': 'col BubbleDetail_colSummaryIcon__7_KKM'}) != None:
                    lead['address'] = soup.find('div', {'class', 'col BubbleDetail_colAddress__SsF9D'}).h1.span.text.split(u'\xa0')[0]
                    lead['rooms'] = soup.find_all('div', {'class': 'BubbleDetail_imageText__33oD_'})[0].text[0]
                    lead['rent'] = soup.find('div', {'class': 'col BubbleDetail_colPrice__2mVzj'}).text.replace('$', '').replace(',', '')
                    if not lead['rent'].isdigit(): lead['rent'] = None
                    lead['baths'] = soup.find_all('div', {'class': 'BubbleDetail_imageText__33oD_'})[1].text[0]
                    if not lead['baths'].isdigit():
                        lead['baths'] = None
                    if soup.find_all('div', {'class': 'BubbleDetail_imageText__33oD_'})[4].text.isdigit():
                        lead['square_feet'] = soup.find_all('div', {'class': 'BubbleDetail_imageText__33oD_'})[4].text.split(' ')[0].replace(',', '').replace('.', '')
                    else:
                        lead['square_feet'] = None
                elif soup.find('div', {'class': 'Floorplan_floorplansContainer__2Rtwg'}) != None:
                    if len(soup.find_all('div', {'class': 'Floorplan_floorplansContainer__2Rtwg'})) > 1:
                        for k in range(len(soup.find('div', {'class': 'Floorplan_floorplansContainer__2Rtwg'}))):
                            lead = {
                                'url': f"https://www.padmapper.com{all_properties[i]['href']}",
                            }
                            lead['address'] = soup.find('h1', {'class', 'FullDetail_street__zq-XK'}).text.split(u'\xa0')[0]
                            lead['rooms'] = soup.find_all('div', {'class': 'Floorplan_title__179XB'})[k].text[0]
                            if not lead['rooms'].isdigit(): lead['rooms'] = None
                            if soup.find_all('div', {'class': 'Floorplan_floorplanPanel__25nE5'})[k].find_all('div')[0].find_all('div')[1].text == 'UNAVAILABLE': continue
                            lead['square_feet'] = None
                            lead['baths'] = None
                            if soup.find_all('div', {'class': 'Floorplan_title__179XB'}) != None:
                                lead['rent'] = soup.find_all('div', {'class': 'Floorplan_priceRange__x-BQo'})[k].span.text.replace('$', '').replace(',', '')
                            else:
                                lead['rent'] = None
                            if lead['rent'] != None: 
                                lead['rent'] = lead['rent'].replace(b'\xe2\x80\x94'.decode('utf-8'), ' ')
                                if ' ' in lead['rent']:
                                    rents = lead['rent'].split(' ')
                                    lead['rent'] = math.ceil((int(rents[0])+int(rents[1]))/2)  
                                else:
                                    if not lead['rent'].isdigit():lead['rent'] = None
                            lead['buildingType'] = 'Apartment'
                            lead['inserted_at'] = datetime.datetime.utcnow()
                            lead['numbers'] = ''
                            if(city[0].isupper()):
                                if city[0] == 'T': lead['city'] = 'city-of-toronto'
                                elif city[0] == 'E': lead['city'] = 'etobicoke'
                                elif city[0] == 'S': lead['city'] = 'scarborough'
                                elif city[0] == 'N': lead['city'] = 'north-york'
                            else:
                                lead['city'] = city.split('?')[0].split('/')[-1]
                            leads.append(lead)
                        continue
                    else:
                        lead['address'] = soup.find('h1', {'class', 'FullDetail_street__zq-XK'}).text.split(u'\xa0')[0]
                        lead['rooms'] = soup.find_all('div', {'class': 'Floorplan_title__179XB'})[0].text[0]
                        if not lead['rooms'].isdigit(): lead['rooms'] = None
                        lead['square_feet'] = None
                        if not lead['square_feet'].isdigit(): lead['square_feet'] = None
                        lead['baths'] = None
                        if soup.find_all('div', {'class': 'Floorplan_title__179XB'}) != None:
                            lead['rent'] = soup.find_all('div', {'class': 'Floorplan_priceRange__x-BQo'})[0].span.text.replace('$', '').replace(',', '')
                        else:
                            lead['rent'] = None
                        if lead['rent'] != None: 
                            lead['rent'] = lead['rent'].replace(b'\xe2\x80\x94'.decode('utf-8'), ' ')
                            if ' ' in lead['rent']:
                                rents = lead['rent'].split(' ')
                                lead['rent'] = math.ceil((int(rents[0])+int(rents[1]))/2)   
                            else:
                                if not lead['rent'].isdigit():lead['rent'] = None                 
                else:
                    lead['address'] = soup.find('h1', {'class', 'FullDetail_street__zq-XK'}).text.split(u'\xa0')[0]
                    lead['rooms'] = soup.find('div', {'class': 'SummaryTable_summaryTable__3zCmu'}).ul.find_all('li')[1].div.span.text[0]
                    if not lead['rooms'].isdigit(): lead['rooms'] = None
                    lead['rent'] = soup.find('div', {'class': 'SummaryTable_summaryTable__3zCmu'}).ul.find_all('li')[0].div.text.replace('$', '').replace(',', '')
                    if lead['rent'] != None: 
                        lead['rent'] = lead['rent'].replace(b'\xe2\x80\x94'.decode('utf-8'), ' ')
                        if ' ' in lead['rent']:
                            rents = lead['rent'].split(' ')
                            lead['rent'] = math.ceil((int(rents[0])+int(rents[1]))/2)
                        else:
                            if not lead['rent'].isdigit():lead['rent'] = None
                    lead['baths'] = soup.find('div', {'class': 'SummaryTable_summaryTable__3zCmu'}).ul.find_all('li')[2].div.text[0]
                    if not lead['baths'].isdigit(): lead['baths'] = None
                    lead['square_feet'] = soup.find('div', {'class': 'SummaryTable_summaryTable__3zCmu'}).ul.find_all('li')[4].div.text.split(' ')[0].replace(',', '').replace('.', '')
                    if not lead['square_feet'].isdigit(): lead['square_feet'] = None
                lead['buildingType'] = 'Apartment'
                lead['inserted_at'] = datetime.datetime.utcnow()
                lead['numbers'] = ''
                if(city[0].isupper()):
                    if city[0] == 'T': lead['city'] = 'city-of-toronto'
                    elif city[0] == 'E': lead['city'] = 'etobicoke'
                    elif city[0] == 'S': lead['city'] = 'scarborough'
                    elif city[0] == 'N': lead['city'] = 'north-york'
                else:
                    lead['city'] = city.split('?')[0].split('/')[-1]
                leads.append(lead)
            except Exception as e:
                print("Error: ", e)
                print(lead['url'])
    csv_detailed_leads = create_csv(
        ['city', 'Address', 'Url', 'Rooms', 'Price', 'Building Type', 'Square Feet', 'Inserted at'],
        [[i['city'], i.get('address'), i['url'], i['rooms'], i['rent'], i['buildingType'], i['square_feet'], i['inserted_at']] for i in leads if i['rooms'] and i['rent'] and i['buildingType']]
    )
    todays_date = date.today().strftime("%d/%m/%Y")
    with app.app.app_context():
        msg = Message(
                f"Singlekey Kijiji Sales Leads for {todays_date}",
                sender=os.environ['GMAIL_ACCOUNT'],
                recipients=['seb7wake@gmail.com'],
            )
        msg.attach(
                f"detailed_leads_for_{todays_date}.csv", "text/csv", csv_detailed_leads.getvalue()
            )
        app.mail.send(msg)
    print('email to sk dev team')
get_kijiji_leads()
get_padmapper_leads()