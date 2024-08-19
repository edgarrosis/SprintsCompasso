-- Criação da tabela CLIENTE
CREATE TABLE CLIENTE (
    idCliente INTEGER PRIMARY KEY,
    nomeCliente TEXT NOT NULL,
    cidadeCliente TEXT NOT NULL,
    estadoCliente TEXT NOT NULL,
    paisCliente TEXT NOT NULL
);

-- Criação da tabela COMBUSTIVEL
CREATE TABLE COMBUSTIVEL (
    idcombustivel INTEGER PRIMARY KEY,
    tipoCombustivel TEXT NOT NULL
);

-- Criação da tabela CARRO
CREATE TABLE CARRO (
    idCarro INTEGER PRIMARY KEY,
    classiCarro TEXT NOT NULL,
    marcaCarro TEXT NOT NULL,
    modeloCarro TEXT NOT NULL,
    anoCarro INTEGER NOT NULL,
    id_combustivelfk INTEGER,
    FOREIGN KEY (id_combustivelfk) REFERENCES COMBUSTIVEL(idcombustivel)
);

-- Criação da tabela QUILOMETRAGEM
CREATE TABLE QUILOMETRAGEM(
    id_km INTEGER PRIMARY KEY,
    kmCarro INTEGER NOT NULL,
    id_carrokm_fk INTEGER NOT NULL,
    FOREIGN KEY (id_carrokm_fk) REFERENCES CARRO(idCarro)
);

-- Criação da tabela VENDEDOR
CREATE TABLE VENDEDOR (
    idVendedor INTEGER PRIMARY KEY,
    nomeVendedor TEXT NOT NULL,
    sexoVendedor TEXT NOT NULL,
    estadoVendedor TEXT NOT NULL
);

-- Criação da tabela LOCACAO
CREATE TABLE LOCACAO (
    idLocacao INTEGER PRIMARY KEY,
    dataLocacao DATE NOT NULL,
    horaLocacao TIME NOT NULL,
    qtdDiaria INTEGER NOT NULL,
    vlrDiaria REAL NOT NULL,
    dataEntrega DATE NOT NULL,
    horaEntrega TIME NOT NULL,
    id_clientefk INTEGER,
    id_vendedorfk INTEGER,
    id_carrofk INTEGER,
    FOREIGN KEY (id_clientefk) REFERENCES CLIENTE(idCliente),
    FOREIGN KEY (id_vendedorfk) REFERENCES VENDEDOR(idVendedor),
    FOREIGN KEY (id_carrofk) REFERENCES CARRO(idCarro)
);

-- Inserindo dados na tabela COMBUSTIVEL
INSERT INTO COMBUSTIVEL (idcombustivel, tipoCombustivel) VALUES
(1, 'Gasolina'),
(2, 'Etanol'),
(3, 'Flex'),
(4, 'Diesel');

-- Inserindo dados na tabela CLIENTE
INSERT INTO CLIENTE (idCliente, nomeCliente, cidadeCliente, estadoCliente, paisCliente) VALUES
(2, 'Cliente dois', 'São Paulo', 'São Paulo', 'Brasil'),
(3, 'Cliente tres', 'Rio de Janeiro', 'Rio de Janeiro', 'Brasil'),
(4, 'Cliente quatro', 'Rio de Janeiro', 'Rio de Janeiro', 'Brasil'),
(5, 'Cliente cinco', 'Manaus', 'Amazonas', 'Brasil'),
(6, 'Cliente seis', 'Belo Horizonte', 'Minas Gerais', 'Brasil'),
(10, 'Cliente dez', 'Rio Branco', 'Acre', 'Brasil'),
(20, 'Cliente vinte', 'Macapá', 'Amapá', 'Brasil'),
(22, 'Cliente vinte e dois', 'Porto Alegre', 'Rio Grande do Sul', 'Brasil'),
(23, 'Cliente vinte e tres', 'Eusébio', 'Ceará', 'Brasil'),
(26, 'Cliente vinte e seis', 'Campo Grande', 'Mato Grosso do Sul', 'Brasil');

-- Inserindo dados na tabela CARRO
INSERT INTO CARRO (idCarro, classiCarro, marcaCarro, modeloCarro, anoCarro, id_combustivelfk) VALUES
(98, 'AKJHKN98JY76539', 'Fiat', 'Fiat Uno', 2000, 1),
(99, 'IKJHKN98JY76539', 'Fiat', 'Fiat Palio', 2010, 1),
(3, 'DKSHKNS8JS76S39', 'VW', 'Fusca 78', 1978, 1),
(10, 'LKIUNS8JS76S39', 'Fiat', 'Fiat 147', 1996, 1),
(7, 'SSIUNS8JS76S39', 'Fiat', 'Fiat 147', 1996, 1),
(6, 'SKIUNS8JS76S39', 'Nissan', 'Versa', 2019, 1),
(2, 'AKIUNS1JS76S39', 'Nissan', 'Versa', 2019, 2),
(4, 'LLLUNS1JS76S39', 'Nissan', 'Versa', 2020, 2),
(1, 'AAAKNS8JS76S39', 'Toyota', 'Corolla XEI', 2023, 3),
(5, 'MSLUNS1JS76S39', 'Nissan', 'Frontier', 2022, 4);

INSERT INTO QUILOMETRAGEM(id_km, kmCarro, id_carrokm_fk) VALUES
(1, 1800, 1),
(2, 8500, 1),
(3, 10000, 2),
(4, 20000, 2),
(5, 30000, 2),
(6, 121700, 3),
(7, 131800, 3),
(8, 151700, 3),
(9, 152700, 3),
(10, 55000, 4),
(11, 56000, 4),
(12, 58000, 4),
(13, 28000, 5),
(14, 38000, 5),
(15, 48000, 5),
(16, 68000, 5),
(17, 78000, 5),
(18, 21800, 6),
(19, 212800, 7),
(20, 211800, 10),
(21, 25412, 98),
(22, 29450, 98),
(23, 20000, 99),
(24, 21000, 99),
(25, 21700, 99);

-- Inserindo dados na tabela VENDEDOR
INSERT INTO VENDEDOR (idVendedor, nomeVendedor, sexoVendedor, estadoVendedor) VALUES
(5, 'Vendedor cinco', '0', 'São Paulo'),
(6, 'Vendedora seis', '1', 'São Paulo'),
(7, 'Vendedora sete', '1', 'Rio de Janeiro'),
(8, 'Vendedora oito', '1', 'Minas Gerais'),
(16, 'Vendedor dezesseis', '0', 'Amazonas'),
(30, 'Vendedor trinta', '0', 'Rio Grande do Sul'),
(31, 'Vendedor trinta e um', '0', 'Ceará'),
(32, 'Vendedora trinta e dois', '1', 'Mato Grosso do Sul');

-- Inserindo dados na tabela LOCACAO
INSERT INTO LOCACAO (idLocacao, dataLocacao, horaLocacao, qtdDiaria, vlrDiaria, dataEntrega, horaEntrega, id_clientefk, id_vendedorfk, id_carrofk) VALUES
(1, '2015-01-10', '10:00', 2, 100, '2015-01-12', '10:00', 2, 5, 98),
(2, '2015-02-10', '12:00', 2, 100, '2015-02-12', '12:00', 2, 5, 98),
(3, '2015-02-13', '12:00', 2, 150, '2015-02-15', '12:00', 3, 6, 99),
(4, '2015-02-15', '13:00', 5, 150, '2015-02-20', '13:00', 4, 6, 99),
(5, '2015-03-02', '14:00', 5, 150, '2015-03-07', '14:00', 4, 7, 99),
(6, '2016-03-02', '14:00', 10, 250, '2016-03-12', '14:00', 6, 8, 3),
(7, '2016-08-02', '14:00', 10, 250, '2016-08-12', '14:00', 6, 8, 3),
(8, '2017-01-02', '18:00', 10, 250, '2017-01-12', '18:00', 4, 6, 3),
(9, '2018-01-02', '18:00', 10, 280, '2018-01-12', '18:00', 4, 6, 3),
(10, '2018-03-02', '18:00', 10, 50, '2018-03-12', '18:00', 10, 16, 10),
(11, '2018-04-01', '11:00', 10, 50, '2018-04-11', '11:00', 20, 16, 7),
(12, '2020-04-01', '11:00', 10, 150, '2020-04-11', '11:00', 20, 16, 6),
(13, '2022-05-01', '08:00', 20, 150, '2022-05-21', '18:00', 22, 30, 2),
(14, '2022-06-01', '08:00', 20, 150, '2022-06-21', '18:00', 22, 30, 2),
(15, '2022-07-01', '08:00', 20, 150, '2022-07-21', '18:00', 22, 30, 2),
(16, '2022-08-01', '08:00', 20, 150, '2022-07-21', '18:00', 22, 30, 2),
(17, '2022-09-01', '08:00', 20, 150, '2022-09-21', '18:00', 23, 31, 4),
(18, '2022-10-01', '08:00', 20, 150, '2022-10-21', '18:00', 23, 31, 4),
(19, '2022-11-01', '08:00', 20, 150, '2022-11-21', '18:00', 23, 31, 4),
(20, '2023-01-02', '18:00', 10, 880, '2023-01-12', '18:00', 5, 16, 1),
(21, '2023-01-15', '18:00', 10, 880, '2023-01-25', '18:00', 5, 16, 1),
(22, '2023-01-25', '08:00', 5, 600, '2023-01-30', '18:00', 26, 32, 5),
(23, '2023-01-31', '08:00', 5, 600, '2023-02-05', '18:00', 26, 32, 5),
(24, '2023-02-06', '08:00', 5, 600, '2023-02-11', '18:00', 26, 32, 5),
(25, '2023-02-12', '08:00', 5, 600, '2023-02-17', '18:00', 26, 32, 5),
(26, '2023-02-18', '08:00', 1, 600, '2023-02-19', '18:00', 26, 32, 5);