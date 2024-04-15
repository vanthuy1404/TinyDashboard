from flask import Flask, render_template, flash, redirect, url_for, request

import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kakaka'
url = 'http://127.0.0.1:5000/'


@app.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def home():
    response = requests.get(f'{url}/users')
    users = response.json()
    return render_template('admin_user.html', users=users)


@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    response = requests.delete(f'{url}/users/{id}')
    if response.status_code == 200:
        flash("Xoa nguoi dung thanh cong", 'success')
    else:
        flash('Khong tim thay ng dung', 'error')
    return redirect(url_for('home'))


@app.route('/add_user', methods=['POST'])
def add_user():
    full_name = request.form.get('full_name')  # Sử dụng 'request.form.get'
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    response = requests.post(f'{url}/users', json={
        'username': username,
        'email': email,
        'password': password,
        'full_name': full_name
    })
    if response.status_code == 201:
        flash('Da them', 'success')
    else:
        flash('Co loi xay ra khi them', 'error')
    return redirect(url_for('home'))
@app.route('/update_user', methods =['POST'])
def update_user():
    id = request.form.get('id')
    full_name = request.form.get('full_name')  # Sử dụng 'request.form.get'
    email = request.form.get('email')
    username = request.form.get('username')
    password = request.form.get('password')
    response = requests.put(f'{url}/users/{id}',json={
        'username': username,
        'email': email,
        'password': password,
        'full_name': full_name
    })
    if response.status_code == 200:
        flash('Cập nhật thành công', 'success')
    else:
        flash('Có lỗi xảy ra khi cập nhật', 'error')
    return redirect(url_for('home'))
@app.route('/products_management', methods = ['GET', 'POST'])
def display_products():
    response = requests.get(f'{url}/products')
    if response.status_code == 200:
        products = response.json()
        return render_template('products.html', products = products)
    else:
        return "Không tìm thấy sản phẩm, 404 "
@app.route('/delete_product',methods = ['POST'])
def delete_product():
    product_code = request.form.get('product_code')
    response = requests.delete(f'{url}/products', json={'product_code': product_code})
    if response.status_code == 200:
        flash('Xóa sản phẩm thành công','success')
        return redirect(url_for('display_products'))
    else:
        flash('Có lỗi xảy ra', 'error')
        return redirect(url_for('display_products'))
@app.route('/add_product', methods=['POST'])
def add_product():
    product_code = request.form.get('product_code')
    category = request.form.get('category')
    name = request.form.get('name')
    price = request.form.get('price')
    image_path = request.form.get('image_path')
    description = request.form.get('description')

    # Gửi yêu cầu POST để thêm sản phẩm mới
    response = requests.post(f'{url}/products', json={
        'product_code': product_code,
        'category': category,
        'name': name,
        'price': price,
        'image_path': image_path,
        'description': description
    })

    if response.status_code == 201:
        flash('Thêm sản phẩm thành công', 'success')
    else:
        flash('Có lỗi xảy ra', 'error')

    return redirect(url_for('display_products'))
@app.route('/orders_management', methods =['POST','GET'])
def orders_management():
    response = requests.get(f'{url}/orders')
    if response.status_code == 200:
        orders = response.json()
        return render_template('orders.html', orders= orders)
    else:
        return "Không có sản phẩm"
if __name__ == "__main__":
    app.run(port=5001, debug=True)
