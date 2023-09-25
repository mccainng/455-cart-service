from flask import Flask, jsonify
import requests
app = Flask(__name__)

url = 'http://127.0.0.1:5000/'

cart = { 
     1: {"user_id": 1, "items": {}},
     2: {"user_id": 2, "items": {}},
}

# Function to retrieve product information
def retrieve_product_info(product_id):
    response = requests.get(f'{url}/products/{product_id}')
    if response.status_code == 200:
        return response.json()
    
# Endpoint to retrieve the contents of the cart
# Endpoint to retrieve the current contents of a user's shopping cart
@app.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    if user_id in cart:  # Change from 'carts' to 'cart'
        return jsonify(cart[user_id])
    else:
        return jsonify({"message": "Cart not found"}), 404


#Endpoint to add a specified quantity of a product
@app.route('/cart/<int:user_id>/add/<int:product_id>', methods=['POST'])
def add_quantity(user_id, product_id):
    data = requests.get_json()
    quantity = data.get('quantity', 1)

    product = retrieve_product_info(product_id)
    if product is None:
        return jsonify({"message": "n/a"}), 404
    
    if user_id in cart:
        carts = cart[user_id]
        current_cart = carts['items']
        if product_id in current_cart:
            current_cart[product_id]['quantity'] += quantity
        else:
            current_cart[product_id] = {
                'product_name': product['name'],
                'quantity': quantity,
                'new_price': product['price'] * quantity
            }
        return jsonify({"message": "added to cart"}),201
    else:
        return jsonify({"message:" "n/a"}),404
    


#Endpoint to remove a specified quantity of a product 
@app.route('/cart/<int:user_id>/remove/<int:product_id>', methods=['POST'])
def remove_quantity(user_id, product_id):
    data = requests.get_json()
    quantity = data.get('quantity', 1)

    product = retrieve_product_info(product_id)
    if product is None:
        return jsonify({"message": "n/a"}), 404
    
    if user_id in cart:
        carts = cart[user_id]
        current_cart = carts['items']
        if product_id in current_cart:
            current_cart = current_cart[product_id]
            if current_cart['quantity'] <= quantity:
                del current_cart[product_id]
            else:
                current_cart['quantity'] -= quantity
                current_cart['new_price'] -= retrieve_product_info(product_id)['price'] * quantity
            return jsonify({"message": "removed"}),200
        else:
            return jsonify({"message": "not in cart"}),404
    else:
        return jsonify({"message": "n/a"}),400
    
if __name__ == '__main__':
    app.run(debug=True)
