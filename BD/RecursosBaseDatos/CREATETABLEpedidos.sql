CREATE TABLE pedidos(

    id_pedido UUID
        DEFAULT gen_random_uuid()
        PRIMARY KEY,

    id_usuario UUID
        NOT NULL
        REFERENCES usuarios(id_usuario),

    fecha_pedido TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP,

    estado VARCHAR(20)
        NOT NULL
        DEFAULT 'pendiente'
        CHECK (
            estado IN (
                'pendiente',
                'pagado',
                'enviado',
                'entregado',
                'cancelado'
            )
        ),

    total NUMERIC(10,2)
        NOT NULL
        CHECK(total >= 0)
);