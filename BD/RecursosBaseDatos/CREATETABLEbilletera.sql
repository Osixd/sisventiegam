CREATE TABLE billeteras(

    id_billetera UUID
        DEFAULT gen_random_uuid()
        PRIMARY KEY,

    id_usuario UUID
        UNIQUE
        REFERENCES usuarios(id_usuario),

    saldo NUMERIC(10,2)
        NOT NULL
        DEFAULT 10000
        CHECK (saldo >= 0)
);