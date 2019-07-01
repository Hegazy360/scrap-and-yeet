import requests
import firebase_admin
from bs4 import BeautifulSoup
from firebase_admin import firestore
from firebase_admin import credentials

cred = credentials.Certificate('./doomsday-244617-7c2e2ed9100f.json')
firebase_admin.initialize_app(cred)

db = firestore.client()

doc_ref = db.collection(u'animals')

for animal in doc_ref.get():
    print(animal.to_dict()['status'])
    response = requests.get("https://api.unsplash.com/search/photos?query=" + animal.to_dict()['name']+"&limit=1&order_by=popular&client_id=dd21c5e89a5ad3e3584f7dfac9f2a0a4ce8714a9d1c2cbe9183eb12cafa7e744")
    if(len(response.json()['results']) > 0):
      animal = doc_ref.document(animal.id)
      animal.set({
          u'image': response.json()['results'][0]
      });

    print('---------')



for animal in doc_ref.get():
    print(animal.to_dict()['status'])
    level = 0;
    status = animal.to_dict()['status'];
    if( status == 'Critically Endangered'):
      level = 5
    elif(status == 'Endangered'):
      level = 4
    elif(status == 'Vulnerable'):
      level = 3
    elif(status == 'Near Threatened'):
      level = 2
    elif(status == 'Least Concern'):
      level = 1
    animal = doc_ref.document(animal.id)
    animal.set({
        u'level': level,
    }, merge=True)

    print('---------')


url = 'https://www.worldwildlife.org/species/directory?direction=desc&page=2&sort=extinction_status'

response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

for row in soup.select('table tr'):
    td = row.findAll('td')
    if(len(td)):
        name = td[0].find(text=True)
        status = td[2].find(text=True)
        print(name)
        print(status)
        animal = doc_ref.document()
        animal.set({
            u'name': name,
            u'status': status,
        })
    print('----')
