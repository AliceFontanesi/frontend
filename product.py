from dbmanager import DbManager
import mysql.connector
import json

class Product:

    @staticmethod
    def connector():
        try:
            db_manager = DbManager("192.168.2.200", 3306, "fontanesi_alice", "Sevastopol.immodesty.Floyd.", "fontanesi_alice_ecommerce")
            conn = db_manager.connect()
            return conn
        except mysql.connector.Error as e:
            print("Errore durante la connessione al database:", str(e))
            
    def __init__(self, id, nome, prezzo, marca):
        self._id = id
        self._nome = nome
        self._prezzo = prezzo
        self._marca = marca
    
    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    @property
    def prezzo(self):
        return self._prezzo

    @prezzo.setter
    def prezzo(self, value):
        self._prezzo = value

    @property
    def marca(self):
        return self._marca

    @marca.setter
    def marca(self, value):
        self._marca = value

    @staticmethod
    def fetchAll(): 
        try: 
            conn = Product.connector()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products")
            records = cursor.fetchall()
            cursor.close()
            products = []
            for row in records:
                product = Product(id=row[0], nome=row[1], prezzo=row[2], marca=row[3])
                products.append(product)
            return products
        except mysql.connector.Error as e:
            print("Errore durante la ricerca dei prodotti:", str(e))

    @staticmethod
    def find(id): 
        try:
            conn = Product.connector()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM products WHERE id = %s", (id,))
            row = cursor.fetchone()
            conn.close()
            if row:
                return Product(id=row[0], nome=row[1], prezzo=row[2], marca=row[3])
            else:
                return None
        except mysql.connector.Error as e:
            print("Errore durante la ricerca del prodotto:", str(e))
            

    @staticmethod
    def create(product_data): 
        try:
            conn = Product.connector()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO products (nome, prezzo, marca) VALUES (%s, %s, %s)", (product_data['nome'], product_data['prezzo'], product_data['marca']))
            conn.commit()
            product_id = cursor.lastrowid
            conn.close()
            return Product(id=product_id, nome=product_data["nome"], prezzo=product_data["prezzo"], marca=product_data["marca"])
        except mysql.connector.Error as e:
            print("Errore durante la creazione del prodotto:", str(e))

    def update(self, product_data): 
        try:
            conn = Product.connector()
            cursor = conn.cursor()
            cursor.execute("UPDATE products SET marca = %s, nome = %s, prezzo = %s WHERE id = %s", (product_data['marca'], product_data['nome'], product_data['prezzo'], self.id,))
            conn.commit()
            conn.close()
        except mysql.connector.Error as e:
            print("Errore durante l'aggiornamento del prodotto:", str(e))
            
    def delete(self): 
        try:
            conn = Product.connector()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = %s", (self.id,))
            conn.commit()
            conn.close()
        except mysql.connector.Error as e:
            print("Errore durante l'eliminazione del prodotto:", str(e))