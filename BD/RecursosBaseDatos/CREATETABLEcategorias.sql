CREATE TABLE categorias(

    id_categoria UUID
        DEFAULT gen_random_uuid()
        PRIMARY KEY,

    nombre_categoria VARCHAR(50)
        UNIQUE NOT NULL
);