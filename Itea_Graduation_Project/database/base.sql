create table if not exists color
(
	id serial not null
		constraint color_pk
			primary key,
	name varchar(20)
);

alter table color owner to postgres;

create unique index if not exists color_id_uindex
	on color (id);

create table if not exists goods
(
	id serial not null
		constraint goods_pk
			primary key,
	name varchar(35),
	color integer
		constraint goods_color_id_fk
			references color,
	density double precision,
	width integer
);

alter table goods owner to postgres;

create unique index if not exists goods_id_uindex
	on goods (id);

create table if not exists attributes
(
	id serial not null
		constraint attributes_pk
			primary key,
	name varchar(20),
	value integer,
	goods integer
		constraint attributes_goods_id_fk
			references goods
				on update cascade on delete cascade
				deferrable
);

alter table attributes owner to postgres;

create unique index if not exists attributes_id_uindex
	on attributes (id);



CREATE ROLE  "SuperAdmin" WITH SUPERUSER CREATEROLE CREATEDB INHERIT;
CREATE ROLE  "Admin" WITH NOSUPERUSER INHERIT NOCREATEROLE;
CREATE ROLE  "User" WITH NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION INHERIT;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO GROUP "SuperAdmin";
GRANT ALL PRIVILEGES ON DATABASE "things" to GROUP "SuperAdmin";
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO GROUP "SuperAdmin";
GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO GROUP "Admin";
GRANT ALL PRIVILEGES ON DATABASE "things" to GROUP "Admin";
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO GROUP "Admin";
GRANT SELECT ON ALL TABLES IN SCHEMA public TO GROUP "User";
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO GROUP "User";
CREATE USER root WITH PASSWORD 'root' SUPERUSER CREATEROLE CREATEDB INHERIT;
GRANT "SuperAdmin" TO root ;
GRANT ALL PRIVILEGES ON DATABASE things TO root;
