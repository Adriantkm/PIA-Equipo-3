create database abarrotes;
use abarrotes;

create table clientes (
	idCliente integer not null,
    nombre varchar(45) not null,
    apellido_paterno varchar(45) not null,
    apellido_materno varchar(45) not null,
    direccion varchar(100),
    correo varchar(60),
    estado binary not null,
    credito decimal not null,
    saldo decimal not null,
    primary key (idCliente)
);

create table puestos (
	idPuesto integer not null,
    puesto varchar(45) not null,
    primary key (idPuesto)
);

create table empleados (
	idEmpleado integer not null,
    nombre varchar(45) not null,
    apellido_paterno varchar(45) not null,
    apellido_materno varchar(45) not null,
    fecha_nacimeinto date not null,
    puesto integer not null,
    correo varchar(60),
    telefono varchar(10),
    celular varchar(10),
    estado binary,
    primary key (idEmpleado),
    foreign key (puesto) references puestos(idPuesto)
);

create table usuarios (
	noUsuario integer not null,
    idEmpleado integer,
    nombre_usuario varchar(45) not null,
    contrasenia varchar(16) not null,
    tipo_usuario smallint not null,
    
    primary key (noUsuario),
    foreign key (idEmpleado) references empleados(idEmpleado)
);

create table categorias (
	idCategoria smallint not null,
    categoria varchar(45),
    primary key (idCategoria)
);

create table productos (
	codigo_producto varchar(16) not null,
    producto varchar(45) not null,
    idCategoria smallint not null,
    descripcion varchar(45),
    costo decimal not null,
    precio decimal not null,
    proveedor varchar(45),
    primary key (codigo_producto),
    foreign key (idCategoria) references categorias(idCategoria)
);

create table ventas (
	noVenta integer not null,
    fecha_venta date not null,
    total_venta decimal not null,
    cliente integer,
    empleado integer,
    primary key(noVenta),
    foreign key(cliente) references clientes(idCliente),
    foreign key(empleado) references empleados(idEmpleado)
);

create table venta_detalle(
	noDetalle integer auto_increment not null,
    noVenta integer not null,
    producto varchar(16) not null,
    cantidad decimal,
    primary key (noDetalle),
    foreign key (noVenta) references ventas(noVenta),
    foreign key (producto) references productos(codigo_producto)
);

insert into clientes
values (1, 'Melanie', 'Hernandez', 'Hernandez', 'San Nicolas', 'melanie.hernandez@uanl.edu.mx', 1, 5000, 3000);
insert into clientes
values (2, 'Marcela Araceli', 'Yañez', 'Escobedo', 'San Nicolas', 'marcela.yañez@uanl.edu.mx','1', 4000,1800);

insert into puestos
values (1, 'Administrador');
insert into puestos
values (2, 'Cajero');
insert into puestos
values (3, 'Invetarista');
insert into puestos
values (4, 'Gerente');
insert into puestos
values (5, 'Contador');
insert into puestos
values (6, 'Basurero');

insert into empleados
values (1, 'Adrián de Jesús', 'Rangel', 'Muñoz', '2003-08-03', 1, 'adrian.rangelmnz@uanl.edu.mx', '8120080918', '8120080918', 1);
insert into empleados
values (2, 'Kevin Misael', 'Diaz', 'Rios', '1998-10-24', 2, 'kevin.diazrz@uanl.edu.mx', '8129199203', '8129199203', 1);
insert into empleados
values (3, 'Karen Nallely', 'Sanchez', 'Martinez', '2003-11-08', 3, 'karen.sanchezmtz@uanl.edu.mx', '8137757567', '8137757567', 1);
insert into empleados
values (4, 'Melanie', 'Hernandez', 'Hernandez', '1999-06-05', 4, 'melanie.hernandezhdz@uanl.edu.mx', '8123644870', '8123644870', 2);
insert into empleados
values (6, 'Arturo Cesar', 'Dominguez', 'Gonzalez', '2002-09-06', 6, 'arturo.dominguezgz@uanl.edu.mx', '833329449', '833329449', 2);

insert into categorias
values (1, 'Papas');
insert into categorias
values (2, 'Galletas');
insert into categorias
values (3, 'Jugos');
insert into categorias
values (4, 'Dulces');
insert into categorias
values(5, 'Refrescos');
insert into categorias
values (6, 'Tortillas');
insert into categorias
values (7, 'Pan');
insert into categorias
values (8,'Azucar');
insert into categorias
values (9, 'Frijol');

insert into Productos
values ('1A', 'Takis', 1, 'Papas picantes',13 , 15, 'Barcel');
insert into Productos
values ('2A', 'Chokis', 2, 'Galletas con chispas de chocolate', 15, 17, 'Gamesa');
insert into Productos
values ('3A', 'Frutsi', 3, '355ml', 5, 7, 'Grupo Universalplast Mexico');
insert into Productos
values ('4A', 'Paletas', 4,  'Manita', 2, 3, 'Vero');
insert into Productos
values ('5A', 'CocaCola', 5, '600ml', 14.5, 16, 'CocaCola');
insert into Productos
values ('6A', 'Pepsi', 5, '600ml', 14.5, 16, 'Pepsi');
insert into Productos
values ('7A', 'Tortillas', 6, '1kg', 22, 24, 'Tortilleria');
insert into Productos
values ('8A', 'Conchita', 7, '1 pieza', 5, 7, 'Tia Rosa');
insert into Productos
values ('9A', 'Azucar', 8, '1kg', 25, 26, 'Zulka');
insert into Productos
values ('10A', 'Frijol', 9, '1kg', 30, 32, 'Verde Valle');

update clientes set saldo = 5000 where idCliente = 1;
update puestos set puesto = 'Administrador' where IdPuesto = 1;
delete from categorias where idCategoria = 9;
delete from empleados where idEmpleado = 1;
select * from clientes;
select * from empleados;
select * from categorias;
select * from productos;

