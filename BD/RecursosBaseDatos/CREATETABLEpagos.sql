CREATE TABLE pagos(

    id_pago UUID
        DEFAULT gen_random_uuid()
        PRIMARY KEY,

    id_pedido UUID
        NOT NULL
        REFERENCES pedidos(id_pedido),

    metodo_pago VARCHAR(20)
        NOT NULL
        CHECK (
            metodo_pago IN (
                'saldo_ficticio',
                'tarjeta_demo',
                'efectivo_demo'
            )
        ),

    monto NUMERIC(10,2)
        NOT NULL
        CHECK (monto >= 0),

    estado_pago VARCHAR(20)
        NOT NULL
        DEFAULT 'pendiente'
        CHECK (
            estado_pago IN (
                'pendiente',
                'aprobado',
                'rechazado'
            )
        ),

    fecha_pago TIMESTAMP
        DEFAULT CURRENT_TIMESTAMP
);