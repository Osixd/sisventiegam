CREATE TABLE usuarios(
	id SERIAL PRIMARY KEY,
	nombre_usuario VARCHAR (255) UNIQUE NOT NULL,
	nombres VARCHAR (255),
	apellido_paterno VARCHAR (255),
	apellido_materno VARCHAR (255),
	permisos VARCHAR (10) CHECK (permisos IN ('admin', 'user')),
	correo VARCHAR (255) UNIQUE NOT NULL,
	contrasena VARCHAR (255) NOT NULL,
	fecharegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);