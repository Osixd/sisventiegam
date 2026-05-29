CREATE TABLE productos(

    id_producto UUID
		DEFAULT gen_random_uuid() 
		PRIMARY KEY,
		
    nombre_producto VARCHAR(50) 
		NOT NULL,
		
	id_categoria UUID
		REFERENCES categorias(id_categoria),

    plataforma VARCHAR(50),
	
    descripcion_producto TEXT,
	
    precio NUMERIC(10,2) 
		NOT NULL
		CHECK(precio >= 0),
		
    stock INT
	NOT NULL 
	DEFAULT 0 
	CHECK(stock >= 0)
);