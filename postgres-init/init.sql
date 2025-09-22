create table tipi(
id_tipi serial primary key,
descricao varchar(100),
aliquota numeric(5,2),
ncm char(8)
);

create table produto(
part_number varchar(25) primary key,
nome varchar(100),
fornecedor varchar(100),
pais_origem varchar(2),
id_tipi int,
constraint fk_id_tipi foreign key (id_tipi) references tipi(id_tipi)
);

create table historico(
hash_code varchar(256),
process_data date,
part_number varchar(25),
constraint fk_part_number foreign key (part_number) references produto(part_number)
);

