create table tipi (
    id_tipi serial primary key,
    descricao text,
    aliquota numeric(5,2),
    ncm char(8)
);

create table endereco (
    id_endereco serial primary key,
    pais_origem varchar(80),
    endereco_completo varchar(150)
);

create table produto (
    id serial primary key,
    part_number varchar(25) not null,
    descricao text,
    fornecedor varchar(100),
    status_produto boolean default false,
    id_tipi int,
    id_endereco int,
    constraint fk_produto_tipi foreign key (id_tipi) references tipi(id_tipi),
    constraint fk_produto_endereco foreign key (id_endereco) references endereco(id_endereco)
);

create table historico (
    id_historico serial primary key,
    hash_code varchar(256) not null,
    process_data timestamp default current_timestamp,
    produto_id int not null,
    constraint fk_historico_produto foreign key (produto_id) references produto(id)
);
