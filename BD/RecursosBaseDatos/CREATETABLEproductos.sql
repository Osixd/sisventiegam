Create Table productos(
	id SERIAL PRIMARY KEY,
	nombre_prod VARCHAR (255),
	tipo VARCHAR (255),
	plataforma VARCHAR (255),
	descripcion_prod TEXT,
	precio NUMERIC (10, 2)
);