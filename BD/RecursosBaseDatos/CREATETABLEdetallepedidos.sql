CREATE TABLE detalle_pedido(

    id_detalle_pedido UUID
        DEFAULT gen_random_uuid()
        PRIMARY KEY,

    id_pedido UUID
        NOT NULL
        REFERENCES pedidos(id_pedido),

    id_producto UUID
        NOT NULL
        REFERENCES productos(id_producto),

    nombre_producto VARCHAR(50)
        NOT NULL,

    cantidad INT
        NOT NULL
        CHECK(cantidad > 0),

    precio_unitario NUMERIC(10,2)
        NOT NULL
        CHECK(precio_unitario >= 0)
);