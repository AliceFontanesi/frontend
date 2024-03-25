import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from product import Product

class RequestHandler(BaseHTTPRequestHandler):
    
    def _set_response(self, status_code=200, content_type='application/json'):
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')  # Consenti l'accesso da qualsiasi origine
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, PATCH')  # Specifica i metodi consentiti
        self.send_header('Access-Control-Allow-Headers', 'Content-type')  # Specifica gli header consentiti
        self.end_headers()
        
        
    @staticmethod
    def create_product_dict(product):
        product_dict = {
            "type": "products",
            "id": str(product.id),
            "attributes": {
                "marca": product.marca,
                "nome": product.nome,
                "prezzo": product.prezzo
            }
        }
        return product_dict
        

    def do_GET(self):
        if self.path == '/products':
            self.get_products()
        elif self.path.startswith('/products/'):
            parts = self.path.split('/')
            product_id = int(parts[2])
            self.get_product(product_id)
        else:
            self.send_error(404, 'Not Found')
            

    def get_products(self):
        records = Product.fetchAll()
        products_list = []
        for record in records:
            product_dict = self.create_product_dict(record)
            products_list.append(product_dict)

        self._set_response()
        response_data = {'data': products_list}
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
    

    def get_product(self, product_id):
        product = Product.find(product_id)
        if product is not None:
            product_dict = self.create_product_dict(product)
            
            self._set_response()
            response_data = {'data': product_dict}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            self.send_error(404, 'Product Not Found')
            
            
    def do_POST(self):
        if self.path == '/products':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            self.create_product(post_data)
        else:
            self.send_error(404, 'Not Found')
            

    def create_product(self, post_data):
        try:
            data = json.loads(post_data.decode('utf-8'))
            if 'data' not in data or 'attributes' not in data['data'] or 'nome' not in data['data']['attributes'] or 'prezzo' not in data['data']['attributes'] or 'marca' not in data['data']['attributes']:
                self.send_error(400, 'Bad Request - Incomplete Data Request')
                return
            
            product = Product.create(data['data']['attributes'])
            product_dict = self.create_product_dict(product)
            self._set_response(status_code=201)
            response_data = {'data': product_dict}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        except json.JSONDecodeError:
            self.send_error(400, 'Bad Request - Invalid JSON')
            
            
    def do_DELETE(self):
        if self.path.startswith('/products/'):
            parts = self.path.split('/')
            product_id = int(parts[2])
            product = Product.find(product_id)
            if product:
                self.delete_product(product)
            else:
                self.send_error(404, 'Product Not Found')
        else:
            self.send_error(404, 'Not Found')
            

    def delete_product(self, product):
        try:
            product.delete()
            self._set_response(status_code=204) 
        except Exception as e:
            self.send_error(500, f'Internal Server Error: {str(e)}')


    def do_PATCH(self):
        if self.path.startswith('/products/'):
            parts = self.path.split('/')
            product_id = int(parts[2])
            product = Product.find(product_id)
            if product:
                self.update_product(product)
            else:
                self.send_error(404, 'Product Not Found')
        else:
            self.send_error(404, 'Not Found')
        
            
    def update_product(self, product):
        try:
            content_length = int(self.headers['Content-Length'])
            patch_data = self.rfile.read(content_length)
            data = json.loads(patch_data.decode('utf-8'))
            
            if 'data' not in data or 'attributes' not in data['data'] or 'nome' not in data['data']['attributes'] or 'prezzo' not in data['data']['attributes'] or 'marca' not in data['data']['attributes']:
                self.send_error(400, 'Bad Request - Incomplete Data Request')
                return
                
            product.update(data['data']['attributes'])
            product_dict = self.create_product_dict(product)
            
            self._set_response()
            response_data = {'data': product_dict}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        except Exception as e:
            self.send_error(500, f'Internal Server Error: {str(e)}')
            

def run(server_class=HTTPServer, handler_class=RequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run()
