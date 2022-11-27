import os
from time import sleep
import requests
from bs4 import BeautifulSoup
import sqlite3


headers = {
        "accept": "*/*",
        "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36"
    }

def connect_db():
    with sqlite3.connect("db.sqlite3") as connector:
        cursor = connector.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shop_category (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category_name TEXT,
                    category_slug TEXT
            );
        """)
        cursor.executescript("""
            CREATE TABLE IF NOT EXISTS shop_product (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                slug TEXT,
                image TEXT,
                description TEXT,
                price TEXT,
                stock INTEGER,
                available TEXT DEFAULT (True),
                created timestamp,
                updated timestamp,
                category_id INTEGER NOT NULL,
                FOREIGN KEY (category_id) REFERENCES category(id)
            );
        """)
        connector.commit()
    connector.close()


def insert_db(category_name, category_slug, name, slug, image, description, price, available):
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT category_name, category_slug FROM shop_category WHERE category_name = '{category_name}' AND category_slug = '{category_slug}'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO shop_category VALUES (NULL,?,?)", (category_name, category_slug))
        print(cursor.execute(f"SELECT rowid FROM shop_category WHERE category_name = '{category_name}'"))
        cursor.execute(f"SELECT id FROM shop_category")
        nr_category_id = cursor.fetchone()[0]
        print(f'dodano kategorię {category_name} o numerze {nr_category_id}')
        cursor.execute("INSERT INTO shop_product VALUES (NULL,?,?,?,?,?,NULL,?,NULL,NULL,?)", (
            name,
            slug,
            image,
            description,
            price,
            available,
            nr_category_id
        ))
        conn.commit()
    else:
        cursor.execute(f"SELECT id FROM shop_category")
        nr_category_id = cursor.fetchone()[0]
        print(f"taka kategoria już jest! nr id: {nr_category_id}")
        cursor.execute("INSERT INTO shop_product VALUES (NULL,?,?,?,?,?,NULL,?,NULL,NULL,?)", (
            name,
            slug,
            image,
            description,
            price,
            available,
            nr_category_id
        ))
        conn.commit()
    conn.close()


def get_links():
    for p in range(1, 2):
        print(f'strona nr: {p}')

        url = f"https://modelnet.pl/modele-drewniane-statkow/?page={p}"
        # url = f"https://modelnet.pl/modele-drewniane-statkow/"
        response = requests.get(url, headers=headers)
        html = response.text
        sleep(1)
        soup = BeautifulSoup(html, "lxml")
        products = soup.find_all('article', class_='product-miniature js-product-miniature')

        urls = []
        count = 0
        for product in products:
            url = product.find('a', href_='').get('href')
            product_name = product.find('h2', class_='h3 product-title').find('a').text
            urls.append(url)
        get_products(urls)


def get_products(urls):
    print(urls)
    rep = [";", " ", "/"]
    for url in urls:
        req = requests.get(url=url, headers=headers)
        src = req.text
        soup = BeautifulSoup(src, "lxml")
        category_name = url.split('/')[3]
        category_slug = category_name
        for item in rep:
            if item in category_slug:
                category_slug = category_slug.replace(item, "-")
        name = soup.find('h1', class_='h1').get_text(strip=True)
        slug = soup.find('h1', class_='h1').get_text(strip=True)
        for item in rep:
            if item in slug:
                slug = slug.replace(item, "-")
        description = soup.find('div', class_='product-description-short').find_next('p').text
        print(description)
        price = soup.find('div', class_='current-price').find('span').get_text(strip=True)
        available = True
        image_link = soup.find('li', class_='thumb-container').find('img', src_='').get('data-image-large-src')
        if (image_link != '0' and image_link != 'image_link'):
            subdir = name
            for item in rep:
                if item in subdir:
                    subdir = subdir.replace(item, "_")
            filename = image_link.split('/')[-1]
            print(f'{subdir} : {filename}')
            if not os.path.exists('media/' + subdir):
                os.mkdir('media/' + subdir)
            img_data = requests.get(image_link, verify=False).content
            with open('media/' + subdir + '/' + filename, 'wb') as handler:
                handler.write(img_data)

            print(f'{subdir} : {filename}')
            image = f'{subdir}/{filename}'


        insert_db(category_name, category_slug, name, slug, image, description, price, available)





def main():
    connect_db()
    get_links()


if __name__ == '__main__':
    main()
