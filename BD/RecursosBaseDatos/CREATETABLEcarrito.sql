CREATE TABLE carrito(
    id_carrito UUID
		DEFAULT gen_random_uuid() 
		PRIMARY KEY,
		
    id_usuario UUID 
	REFERENCES usuarios(id_usuario),
	
    fecha_creacion TIMESTAMP 
	DEFAULT CURRENT_TIMESTAMP,
	
    estado VARCHAR(50)
	NOT NULL
	DEFAULT 'activo'
	CHECK(estado IN('activo', 'comprado', 'cancelado'))
)