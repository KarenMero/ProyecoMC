from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
from wsgiref.simple_server import make_server

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Cambia si es necesario
app.config['MYSQL_DB'] = 'TiendaMC'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'


@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM cliente')  # Cambiar a cliente para obtener los datos
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', clientes=data)


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


@app.route('/productos')
def productos():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM producto')  # Obtiene los productos
    data = cur.fetchall()
    cur.close()
    return render_template('productos.html', productos=data)


@app.route('/add_producto', methods=['POST'])
def add_producto():
    if request.method == 'POST':
        nombreSerie = request.form['nombreSerie']
        precio = request.form['precio']
        stock = request.form['stock']
        idProveedor = request.form['idProveedor']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO producto (nombreSerie, precio, stock, idProveedor) VALUES (%s, %s, %s, %s)', 
                    (nombreSerie, precio, stock, idProveedor))
        mysql.connection.commit()
        cur.close()
        flash('Producto agregado satisfactoriamente')
        return redirect(url_for('productos'))


@app.route('/edit_producto/<id>')
def edit_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM producto WHERE idProducto = {0}'.format(id))
    data = cur.fetchall()
    cur.close()
    return render_template('edit_producto.html', producto=data[0])


@app.route('/update_producto/<id>', methods=['POST'])
def update_producto(id):
    if request.method == 'POST':
        nombreSerie = request.form['nombreSerie']
        precio = request.form['precio']
        stock = request.form['stock']
        idProveedor = request.form['idProveedor']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE producto SET nombreSerie = %s, precio = %s, stock = %s, idProveedor = %s WHERE idProducto = {0}'.format(id), 
                    (nombreSerie, precio, stock, idProveedor))
        mysql.connection.commit()
        cur.close()
        flash('Producto actualizado satisfactoriamente')
        return redirect(url_for('productos'))


@app.route('/delete_producto/<string:id>')
def delete_producto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM producto WHERE idProducto = {0}'.format(id))
    mysql.connection.commit()
    cur.close()
    flash('Producto eliminado satisfactoriamente')
    return redirect(url_for('productos'))


if __name__ == '__main__':
    app.run(port=3000, debug=True)
