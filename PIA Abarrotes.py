import sys
import mysql.connector
from PyQt5 import uic, QtGui
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


user = []
class Login(QMainWindow):
    def __init__(self, parent = None):
        super(Login, self).__init__(parent)
        uic.loadUi('login.ui', self)
        
        global user
        self.user = user
        self.UiLogin()

    def UiLogin(self):
        self.btnIniciar.clicked.connect(self.fnAcceso)
    
    def fnAcceso(self):
        empleado = self.txtUsuario.text()
        contrasena = self.txtContrasena.text()
        t_empleado = self.cmbUsuario.currentIndex() + 1

        conexion = fnConexionBD()
        cursor = conexion.cursor()
        sql = 'SELECT * FROM usuarios WHERE nombre_usuario = %s AND contrasenia = %s AND tipo_usuario = %s'
        valores = (empleado, contrasena, t_empleado)
        cursor.execute(sql, valores)
        data = cursor.fetchall()

        if data:
            conexion = fnConexionBD()
            cursor = conexion.cursor()
            sql = '''
            SELECT nombre, apellido_paterno, apellido_materno FROM empleados WHERE idEmpleado = %s;'''
            valores = (data[0][1],)
            cursor.execute(sql, valores)
            data_usuario = cursor.fetchall()

            if data_usuario:
                self.user.append(data_usuario[0][0])
                self.user.append(data_usuario[0][1])
                self.user.append(data_usuario[0][2])
            
            if self.cmbUsuario.currentIndex() + 1 == 1:
                self.fnPanelControl()
            else:
                self.fnPuntoVenta()

        
    def fnPanelControl(self):
        self.hide()
        vModulos = PanelControl(self)
        vModulos.show()
    
    def fnPuntoVenta(self):
        self.hide()
        vModulos = PuntoVenta(self)
        vModulos.show()
            

class PanelControl(QMainWindow):
    def __init__(self, parent = None):
        super(PanelControl, self).__init__(parent)
        uic.loadUi('modulos.ui', self)
        self.UiPanel()
    
    def UiPanel(self):
        self.btnPuntoVenta.clicked.connect(self.fnPuntoVenta)
        self.btnEmpleados.clicked.connect(self.fnEmpleados)
        self.btnClientes.clicked.connect(self.fnClientes)
        self.btnProductos.clicked.connect(self.fnProductos)
    
    def fnPuntoVenta(self):
        self.hide()
        vModulo = PuntoVenta(self)
        vModulo.show()

    def fnEmpleados(self):
        self.hide()
        vModulo = Empleados(self)
        vModulo.show()

    def fnProductos(self):
        self.hide()
        vModulo = Productos(self)
        vModulo.show()

    def fnClientes(self):
        self.hide()
        vModulo = Clientes(self)
        vModulo.show()
    

        
class PuntoVenta(QMainWindow):
    def __init__(self, parent = None):
        super(PuntoVenta, self).__init__(parent)
        uic.loadUi('ventas.ui', self)
        self.UiPuntoVenta()

    def UiPuntoVenta(self):
        self.btnAgregar.clicked.connect(self.Agregar)
        self.btnPagar.clicked.connect(self.Pagar)
    
    def Agregar(self):
        codigo = (self.txtCodigo.text(),)

        conexion = fnConexionBD()
        cursor = conexion.cursor()
        sql = '''
            SELECT codigo_producto, producto, precio
            FROM productos
            WHERE codigo_producto = %s
        '''
        cursor.execute(sql, codigo)
        producto = cursor.fetchall()

        if producto:
            i = self.lsCantidad.count()
            importe = self.spCantidad.value() * producto[0][2]

            self.lsCantidad.insertItem(i, f'{self.spCantidad.value()}')
            self.lsProducto.insertItem(i, f'{producto[0][1]}')
            self.lsPrecio.insertItem(i, f'{producto[0][2]:.2f}')
            self.lsImporte.insertItem(i, f'{importe:.2f}')
            self.Total()

            self.txtCodigo.clear()
            self.spCantidad.setValue(1)
    
    def Pagar(self):
        conexion = fnConexionBD()

        cursor = conexion.cursor()
        sql = '''
            SELECT nombre, apellido_paterno, saldo
            FROM clientes
            WHERE idCliente = %s
        '''
        value = (self.txtCliente.text(),)
        cursor.execute(sql, value)
        cliente = cursor.fetchall()

        total = float(self.lblTotal.text())
        importe = float(self.txtImporte.text())
        
        title = f'{"ABARROTES - EL VECINDARIO":^45}\n'
        datos = f'Cliente: {cliente[0][0]} {cliente[0][1]}\n'
        ticket = self.Ticket()
        
        pie = f'{"--- GRACIAS POR SU COMPRA ---":^45}'

        
        if self.rdbEfectivo.isChecked():
            if importe < total:
                self.lblMensaje.setText('Importe insuficiente')
            else:
                cambio = importe - total


                pagos = f'{"-"*45}\n{"Total: $":>35}{total:>10}\n{"-" * 10:>45}\n{"Importe: $":>35}{importe:>10}\n{"Cambio: $":>35}{cambio:>10}\n'

                formato = f'{title}{datos}{ticket}{pagos}{pie}'
                self.txtDisplay.append(formato)
        else:
            self.txtImporte.setEnabled(False)
            if total > cliente[0][2]:
                self.lblMensaje.setText('Cliente con saldo insuficiente')
            else:
                saldo = float(cliente[0][2]) - total
                pagos = f'{"-"*45}\n{"Total: $":>35}{total:>10}\n{"-" * 10:>45}\n{"Crédito: $":>35}{total:>10}\n{"Nuevo Saldo: $":>35}{saldo:>10}\n'

                formato = f'{title}{datos}{ticket}{pagos}{pie}'
                self.txtDisplay.append(formato)

    
    def Total(self):
        total = 0
        for p in range(self.lsCantidad.count()):
            importe = float(self.lsImporte.item(p).text())
            total += importe
        
        self.lblTotal.setText(f'{total:.2f}')

    def Ticket(self):
        header = f'{"Cant":<5}{"Producto":20}{"Precio":>10}{"Total":>10}\n{"-" * 45}\n'
        ticket = ''

        for i in range(self.lsProducto.count()):
            ticket += f'{self.lsCantidad.item(i).text():<5}{self.lsProducto.item(i).text():20}{self.lsPrecio.item(i).text():>10}{self.lsImporte.item(i).text():>10}\n'
        
        return(header + ticket)


class Empleados(QMainWindow):
    def __init__(self, parent = None):
        super(Empleados, self).__init__(parent)
        uic.loadUi('empleados.ui', self)
        self.UiEmpleados()
    
    def UiEmpleados(self):
        self.Carga()
        self.btnBuscar.clicked.connect(self.busquedaE)
        self.btnLimpiar.clicked.connect(self.limpiar)
        self.btnRegistrar.clicked.connect(self.registroE)
        self.btnLimpiar2.clicked.connect(self.limpiar)
    
    def Carga(self):
        conexion = fnConexionBD()
        reg = fnCarga(conexion, 'empleados')

        numero = self.tbwEmpleados.rowCount()
        for fila in range(numero):
            self.tbwEmpleados.removeRow(0)
        
        for registro in reg:
            fila = self.tbwEmpleados.rowCount()
            self.tbwEmpleados.insertRow(fila)
            for d in range(len(registro)):
                dato = registro[d]
                self.tbwEmpleados.setItem(fila, d, QTableWidgetItem(str(dato)))
        
        puestos = fnCarga(conexion, 'puestos')
        for puesto in puestos:
            self.cmbPuesto.addItem(puesto[1])


    def busquedaE(self):
        empleado = (self.txtIdUsuario.text(),)
        conexion = fnConexionBD()
        cursor = conexion.cursor()
        sql = '''
            SELECT * FROM empleados
            WHERE idEmpleado = %s
        '''
        cursor.execute(sql, empleado)
        data = cursor.fetchall()

        print(data)
        if data:
            puestos = ['Administrador','Cajero','Inventarista','Gerente','Contador','Basurero']
            for puesto in range(len(puestos)):
                if data[0][5] == puesto + 1:
                    p = puesto + 1
                    break
        
            resultado = f'''--- RESULTADO DE BÚSQUEDA ---\nEmpleado:\n{data[0][1]} {data[0][2]} {data[0][3]}\nFecha de nacimiento: {data[0][4]}\nPuesto: {p}\nCorreo: {data[0][6]}\nTeléfono: {data[0][7]}\nCelular: {data[0][8]}'''
        else:
            resultado = 'Empleado no encontrado'
        
        self.txtDatos.clear()
        self.txtDatos.append(resultado)


    def registroE(self):
        nombre = self.txtNombre.text()
        paterno = self.txtPaterno.text()
        materno = self.txtMaterno.text()

        dia = self.dateNacimiento.date().day()
        mes = self.dateNacimiento.date().month()
        anio = self.dateNacimiento.date().year()
        fecha = f'{anio}-{mes}-{dia}'

        idEmpleado = f'{dia}{mes}{anio}'
        email = self.txtEmail.text()
        telefono = self.txtTelefono.text()
        celular = self.txtCelular.text()
        puesto = self.cmbPuesto.currentIndex() + 1

        usuario = self.txtUsuario.text()
        contra = self.txtContrasenia.text()

        conexion = fnConexionBD()
        cursor = conexion.cursor()
        sql = '''
            INSERT INTO empleados (idEmpleado, nombre, apellido_paterno, apellido_materno, fecha_nacimeinto, puesto, correo, telefono, celular, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        '''
        valores = (idEmpleado, nombre, paterno, materno, fecha, puesto, email, telefono, celular, 1)
        cursor.execute(sql, valores)
        conexion.commit()
        self.txtRegistro.append('Empleado registrado correctamente.')
        
        
        try:
            conexion = fnConexionBD()
            cursor = conexion.cursor()
            sql = '''
                INSERT INTO usuarios (noUsuario, idEmpleado, nombre_usuario, contrasenia, tipo_usuario)
                VALUES (%s, %s, %s, %s, %s)
            '''
            values = (dia, idEmpleado, usuario, contra, puesto)
            cursor.execute(sql, values)
            conexion.commit()
        except:
            self.txtRegistro.append('Error al realizar el registro')
        else:
            self.txtRegistro.append('Empleado registrado correctamente.')

            self.txtNombre.clear()
            self.txtPaterno.clear()
            self.txtMaterno.clear()
            self.txtEmail.clear()
            self.txtTelefono.clear()
            self.txtCelular.clear()
            self.puesto.setCurrentText(-1)
            self.txtUsuario.clear()
            self.txtContrasenia.clear()

    def limpiar(self):
        self.txtDatos.clear()
        self.txtRegistro.clear()


class Productos(QMainWindow):
    def __init__(self, parent = None):
        super(Productos, self).__init__(parent)
        uic.loadUi('productos.ui', self)
        self.UiProductos()

    def UiProductos(self):
        self.CargaP()
        self.btnRegistrar.clicked.connect(self.RegistroP)
        self.btnCancelar.clicked.connect(self.Limpiar)
        self.btnBuscar.clicked.connect(self.BuscarP)

    def CargaP(self):
        conexion = fnConexionBD()
        registros = fnCarga(conexion, 'productos')

        numero = self.tbwProductos.rowCount()
        for fila in range(numero):
            self.tbwProductos.removeRow(0)

        for registro in registros:
            f = self.tbwProductos.rowCount()
            self.tbwProductos.insertRow(f)
            for r in range(len(registro)):
                dato = registro[r]
                self.tbwProductos.setItem(f, r, QTableWidgetItem(str(dato)))
        
        for categoria in range(self.cmbCategoria.count()):
            self.cmbCategoria.removeItem(0)

        categorias = fnCarga(conexion, 'categorias')
        for categoria in categorias:
            self.cmbCategoria.addItem(categoria[1])
        
    def RegistroP(self):
        codigo = self.txtCodigo.text()
        producto = self.txtProducto.text()
        descripcion = self.txtDescripcion.toPlainText()
        costo = self.txtCosto.text()
        precio = self.txtPrecio.text()
        categoria = self.cmbCategoria.currentIndex() + 1
        proveedor = self.txtProveedor.text()

        conexion = fnConexionBD()
        cursor = conexion.cursor()
        sql = '''
            INSERT INTO productos
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        '''
        valores = (codigo, producto, categoria, descripcion, costo, precio, proveedor)
        cursor.execute(sql, valores)
        conexion.commit()
        self.CargaP()
        self.Limpiar()

    def BuscarP(self):
        codigo = self.txtCodigoB.text()
        conexion = fnConexionBD()
        cursor = conexion.cursor()
        sql = '''
            SELECT * FROM productos
            WHERE codigo_producto = %s
        '''
        cursor.execute(sql, (codigo,))
        producto = cursor.fetchall()

        resultado = f'''
        Producto encontrado:
        {producto[0][0]} - {producto[0][1]}
        "{producto[0][3]}"
        Precio: ${producto[0][5]}
        '''
        self.txtDisplay.setPlainText(resultado)
        
    def Limpiar(self):
        self.txtCodigo.clear()
        self.txtProducto.clear()
        self.txtDescripcion.clear()
        self.txtCosto.clear()
        self.txtPrecio.clear()
        self.cmbCategoria.setCurrentIndex(-1)
        self.txtProveedor.clear()


class Clientes(QMainWindow):
    def __init__(self, parent = None):
        super(Clientes, self).__init__(parent)
        uic.loadUi('clientes.ui', self)
        self.UiClientes()
    
    def UiClientes(self):
        self.Carga()
        self.btnRegistrar.clicked.connect(self.AgregarC)
        self.btnBuscar.clicked.connect(self.BuscarC)
        self.btnLimpiar.clicked.connect(self.Limpiar)
        self.btnLimpiar2.clicked.connect(self.Limpiar)

    def Carga(self):
        conexion = fnConexionBD()
        registros = fnCarga(conexion, 'clientes')

        numero = self.tbwClientes.rowCount()
        for fila in range(numero):
            self.tbwClientes.removeRow(0)

        for registro in registros:
            f = self.tbwClientes.rowCount()
            self.tbwClientes.insertRow(f)
            for r in range(len(registro)):
                dato = registro[r]
                self.tbwClientes.setItem(f, r, QTableWidgetItem(str(dato)))
        
    def AgregarC(self):
        conexion = fnConexionBD()
        cursor = conexion.cursor()
        sql = '''
            SELECT MAX(idCliente) FROM clientes
        '''
        cursor.execute(sql)
        cliente = cursor.fetchall()

        idCliente = cliente[0][0] + 1
        nombre = self.txtNombre.text()
        paterno = self.txtPaterno.text()
        materno = self.txtMaterno.text()
        direccion = self.txtDireccion.text()
        email = self.txtEmail.text()
        credito = self.txtCredito.text()
        estado = 1

        cursor = conexion.cursor()
        sql = '''
            INSERT INTO clientes
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        values = (idCliente, nombre, paterno, materno, direccion, email, estado, credito, credito)
        cursor.execute(sql, values)
        conexion.commit()
        self.Carga()
        self.Limpiar()


    def BuscarC(self):
        idCliente = self.txtIdCliente.text()
        conexion = fnConexionBD()
        cursor = conexion.cursor()
        sql = '''
            SELECT * FROM clientes
            WHERE idCliente = %s;
        '''
        values = (idCliente,)
        cursor.execute(sql,values)
        cliente = cursor.fetchall()

        resultado = f'''
        Cliente: {cliente[0][0]} - {'ACTIVO' if cliente[0][6] else 'INACTIVO' }

        Nombre: {cliente[0][1]} {cliente[0][2]} {cliente[0][3]}
        Dirección: {cliente[0][4]}
        Correo: {cliente[0][5]}
        Límite de crédito: {cliente[0][7]}
        Saldo disponible: {cliente[0][8]}
        '''
        self.txtDisplay.append(resultado)

    def Limpiar(self):
        self.txtNombre.clear()
        self.txtPaterno.clear()
        self.txtMaterno.clear()
        self.txtDireccion.clear()
        self.txtEmail.clear()
        self.txtCredito.clear()
        self.txtIdCliente.clear()
        self.txtDisplay.clear()


def fnConexionBD():
    conexion = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = 'roblox',
        database = 'abarrotes'
    )
    return conexion

def fnCarga(conexion, tabla):
    cursor = conexion.cursor()
    sql = f'SELECT * FROM {tabla}'
    cursor.execute(sql)
    data = cursor.fetchall()
    return data


app = QApplication(sys.argv)
UiWindow = Login()
UiWindow.show()
sys.exit(app.exec_())