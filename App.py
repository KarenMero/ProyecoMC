#Actualizar el app.py
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from wsgiref.simple_server import make_server

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Anibal22062000'  # Cambia si es necesario
app.config['MYSQL_DB'] = 'TiendaMC'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/products')  # Lista de todos los productos
def products():
   cur = mysql.connection.cursor()
   cur.execute('SELECT * FROM producto')  # Obtiene todos los productos
   data = cur.fetchall()
   cur.close()
   return render_template('products.html', products=data)

@app.route('/product/<int:id>')  # Detalles de un producto específico
def product(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM producto WHERE idProducto = %s', [id])
    data = cur.fetchone()
    cur.close()
    if data:
        return render_template('product.html', producto=data, edit=False)
    else:
        flash('Producto no encontrado')
        return redirect(url_for('products'))  # Redirigir a la lista de productos



@app.route('/venta')
def venta():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM venta_factura')  
    data = cur.fetchall()
    cur.close()
    return render_template('venta.html', venta=data)


@app.route('/clientes')
def clientes():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cliente')  
    data = cur.fetchall()
    cur.close()
    return render_template('clientes.html' , clientes=data)

@app.route('/add_cliente', methods=['POST'])
def add_cliente():
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correoElectronico = request.form['correoElectronico']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO cliente (nombres, apellidos, direccion, telefono, correoElectronico) VALUES (%s, %s, %s, %s, %s)', 
                    (nombres, apellidos, direccion, telefono, correoElectronico))
        mysql.connection.commit()
        cur.close()
        flash('Cliente agregado satisfactoriamente')
        return redirect(url_for('index'))



@app.route('/edit_cliente/<id>')
def edit_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cliente WHERE idCliente = {0}'.format(id))
    data = cur.fetchall()
    cur.close()
    return render_template('edit_cliente.html', cliente=data[0])


@app.route('/update_cliente/<id>', methods=['POST'])
def update_cliente(id):
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correoElectronico = request.form['correoElectronico']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE cliente SET nombres = %s, apellidos = %s, direccion = %s, telefono = %s, correoElectronico = %s WHERE idCliente = {0}'.format(id), 
                    (nombres, apellidos, direccion, telefono, correoElectronico))
        mysql.connection.commit()
        cur.close()
        flash('Cliente actualizado satisfactoriamente')
        return redirect(url_for('index'))


@app.route('/delete_cliente/<string:id>')
def delete_cliente(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM cliente WHERE idCliente = {0}'.format(id))
    mysql.connection.commit()
    cur.close()
    flash('Cliente eliminado satisfactoriamente')
    return redirect(url_for('index'))



@app.route('/product/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        nombre_serie = request.form['nombreSerie']
        precio = request.form['precio']
        stock = request.form['stock']
        id_proveedor = request.form['idProveedor']
        
        cur.execute('UPDATE producto SET nombreSerie = %s, precio = %s, stock = %s, idProveedor = %s WHERE idProducto = %s',
                    (nombre_serie, precio, stock, id_proveedor, id))
        mysql.connection.commit()
        cur.close()
        flash('Producto actualizado exitosamente.')
        return redirect(url_for('product', id=id))
    
    cur.execute('SELECT * FROM producto WHERE idProducto = %s', [id])
    producto = cur.fetchone()
    cur.close()
    if producto:
        return render_template('product.html', producto=producto, edit=True)
    else:
        flash('Producto no encontrado.')
        return redirect(url_for('product'))

@app.route('/product/delete/<int:id>', methods=['GET'])
def delete_product(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM producto WHERE idProducto = %s', [id])
    mysql.connection.commit()
    cur.close()
    flash('Producto eliminado exitosamente.')
    return redirect(url_for('productos'))  # Redirigir a la lista de productos


@app.route('/edit_venta/<int:id>')
def edit_venta(id):
    # Lógica para editar la venta
    pass

@app.route('/delete_venta/<int:id>', methods=['POST'])
def delete_venta(id):
    # Lógica para eliminar la venta
    pass


if __name__ == '__main__':
    app.run(port=3000, debug=True)
