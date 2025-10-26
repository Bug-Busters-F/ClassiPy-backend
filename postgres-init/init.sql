create table tipi (
    tipi_id serial primary key not null,
    tipi_descricao text,
    tipi_aliquota numeric(5,2),
    tipi_ncm varchar(50)
);

create table fabricante (
    fab_id serial primary key not null,
    fab_nome varchar(100),
    fab_endereco varchar(150),
    fab_pais varchar(80)
);

create table produto (
    pro_id serial primary key not null,
    pro_descricao text,
    pro_part_number varchar(25) not null,
    pro_status varchar(20),
    fabricante_fab_id int,
--    historico_hist_id int,
    tipi_tipi_id int,
--    constraint fk_historico_hist_id foreign key (historico_hist_id) references historico (hist_id),
    constraint fk_tipi_tipi_id foreign key (tipi_tipi_id) references tipi(tipi_id),
    constraint fk_fabricante_fab_id foreign key (fabricante_fab_id) references fabricante(fab_id)
);

create table historico (
    hist_id serial primary key,
    hist_data_processamento timestamp,
    hist_hash varchar (255),
    produto_pro_id int,
    constraint fk_produto_pro_id foreign key (produto_pro_id) references produto (pro_id)

);