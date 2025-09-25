-- Tabela de Tipi (classificação fiscal)
create table tipi (
    id_tipi serial primary key,
    descricao varchar(100) not null,
    aliquota numeric(5,2) not null,
    ncm char(8) not null
);

-- Tabela de Produto
create table produto (
    part_number varchar(25) primary key,
    nome varchar(100),
    fornecedor varchar(100),
    pais_origem char(2),
    id_tipi int,
    constraint fk_id_tipi foreign key (id_tipi) references tipi(id_tipi)
);

-- Histórico de classificações
create table historico (
    id_historico serial primary key,
    hash_code varchar(256) not null,
    process_data timestamp default current_timestamp, -- data/hora do salvamento
    part_number varchar(25) not null,
    constraint fk_part_number foreign key (part_number) references produto(part_number)
);
