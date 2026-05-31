CREATE TABLE detalle_carrito(

    id_detalle_carrito UUID
        DEFAULT gen_random_uuid()
        PRIMARY KEY,

    id_carrito UUID
        NOT NULL
        REFERENCES carrito(id_carrito),

    id_producto UUID
        NOT NULL
        REFERENCES productos(id_producto),

    cantidad INT
        NOT NULL
        DEFAULT 1
        CHECK (cantidad > 0),

    UNIQUE(id_carrito, id_producto)
);