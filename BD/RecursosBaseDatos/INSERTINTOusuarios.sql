CREATE TABLE usuarios(

	id_usuario UUID 
		DEFAULT gen_random_uuid() PRIMARY KEY,
		
	nombre_usuario VARCHAR (50) 
		UNIQUE NOT NULL,
		
	nombres VARCHAR (50),
	
	apellido_paterno VARCHAR (50),
	
	apellido_materno VARCHAR (50),
	
	permisos VARCHAR (10) 
		NOT NULL
		DEFAULT 'user'
		CHECK (permisos IN ('admin', 'user')),
		
	correo VARCHAR (150) 
		UNIQUE NOT NULL,
		
	contrasena VARCHAR (255) 
		NOT NULL,
	fecha_registro TIMESTAMP
		DEFAULT CURRENT_TIMESTAMP
);