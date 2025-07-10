create table TechHub_azienda
(
    ID_azienda   integer      not null
        primary key autoincrement,
    nome_azienda varchar(100) not null
        unique,
    sede_legale  varchar(100) not null
);

create table TechHub_componenti
(
    id         integer      not null
        primary key autoincrement,
    nome       varchar(100) not null,
    marca      varchar(100) not null,
    tipologia  varchar(50)  not null,
    prezzo     decimal      not null,
    immagine   varchar(500),
    azienda_id integer      not null
        references TechHub_azienda
            deferrable initially deferred
);

create index TechHub_componenti_azienda_id_f6719760
    on TechHub_componenti (azienda_id);

create table TechHub_giveaway
(
    ID_giveaway integer      not null
        primary key autoincrement,
    titolo      varchar(100) not null,
    immagine    varchar(200) not null,
    data_inizio datetime     not null,
    data_fine   datetime     not null
);

create table TechHub_utente
(
    id                 integer      not null
        primary key autoincrement,
    ID_utente          varchar(50)  not null
        unique,
    password           varchar(100) not null,
    email              varchar(254),
    ruolo              varchar(10)  not null,
    data_nascita       date,
    telefono           varchar(20),
    nazionalita        varchar(50),
    partita_iva        varchar(50),
    telefono_aziendale varchar(20)
);

create table TechHub_ordine
(
    ID_ordine        integer      not null
        primary key autoincrement,
    data_creazione   datetime     not null,
    stato            varchar(20)  not null,
    sconto_applicato decimal      not null,
    nome             varchar(100) not null,
    marca            varchar(100) not null,
    tipologia        varchar(50)  not null,
    prezzo           decimal      not null,
    utente_id        bigint       not null
        references TechHub_utente
            deferrable initially deferred
);

create index TechHub_ordine_utente_id_bf1bb8df
    on TechHub_ordine (utente_id);

create table TechHub_ordine_componenti
(
    id            integer not null
        primary key autoincrement,
    ordine_id     integer not null
        references TechHub_ordine
            deferrable initially deferred,
    componenti_id bigint  not null
        references TechHub_componenti
            deferrable initially deferred
);

create index TechHub_ordine_componenti_componenti_id_0355759b
    on TechHub_ordine_componenti (componenti_id);

create index TechHub_ordine_componenti_ordine_id_98af604a
    on TechHub_ordine_componenti (ordine_id);

create unique index TechHub_ordine_componenti_ordine_id_componenti_id_310193ea_uniq
    on TechHub_ordine_componenti (ordine_id, componenti_id);

create table TechHub_partecipa
(
    id          integer      not null
        primary key autoincrement,
    email       varchar(254) not null,
    data        datetime     not null,
    giveaway_id integer      not null
        references TechHub_giveaway
            deferrable initially deferred,
    utente_id   bigint       not null
        references TechHub_utente
            deferrable initially deferred
);

create index TechHub_partecipa_giveaway_id_ae202609
    on TechHub_partecipa (giveaway_id);

create index TechHub_partecipa_utente_id_eac042e4
    on TechHub_partecipa (utente_id);

create unique index TechHub_partecipa_utente_id_giveaway_id_c381d13f_uniq
    on TechHub_partecipa (utente_id, giveaway_id);

create table TechHub_recensione
(
    ID_recensione integer      not null
        primary key autoincrement,
    titolo        varchar(100) not null,
    voto          integer      not null,
    testo         text         not null,
    utente_id     bigint       not null
        references TechHub_utente
            deferrable initially deferred
);

create index TechHub_recensione_utente_id_b992d930
    on TechHub_recensione (utente_id);

create table auth_group
(
    id   integer      not null
        primary key autoincrement,
    name varchar(150) not null
        unique
);

create table auth_user
(
    id           integer      not null
        primary key autoincrement,
    password     varchar(128) not null,
    last_login   datetime,
    is_superuser bool         not null,
    username     varchar(150) not null
        unique,
    last_name    varchar(150) not null,
    email        varchar(254) not null,
    is_staff     bool         not null,
    is_active    bool         not null,
    date_joined  datetime     not null,
    first_name   varchar(150) not null
);

create table auth_user_groups
(
    id       integer not null
        primary key autoincrement,
    user_id  integer not null
        references auth_user
            deferrable initially deferred,
    group_id integer not null
        references auth_group
            deferrable initially deferred
);

create index auth_user_groups_group_id_97559544
    on auth_user_groups (group_id);

create index auth_user_groups_user_id_6a12ed8b
    on auth_user_groups (user_id);

create unique index auth_user_groups_user_id_group_id_94350c0c_uniq
    on auth_user_groups (user_id, group_id);

create table django_content_type
(
    id        integer      not null
        primary key autoincrement,
    app_label varchar(100) not null,
    model     varchar(100) not null
);

create table auth_permission
(
    id              integer      not null
        primary key autoincrement,
    content_type_id integer      not null
        references django_content_type
            deferrable initially deferred,
    codename        varchar(100) not null,
    name            varchar(255) not null
);

create table auth_group_permissions
(
    id            integer not null
        primary key autoincrement,
    group_id      integer not null
        references auth_group
            deferrable initially deferred,
    permission_id integer not null
        references auth_permission
            deferrable initially deferred
);

create index auth_group_permissions_group_id_b120cbf9
    on auth_group_permissions (group_id);

create unique index auth_group_permissions_group_id_permission_id_0cd325b0_uniq
    on auth_group_permissions (group_id, permission_id);

create index auth_group_permissions_permission_id_84c5c92e
    on auth_group_permissions (permission_id);

create index auth_permission_content_type_id_2f476e4b
    on auth_permission (content_type_id);

create unique index auth_permission_content_type_id_codename_01ab375a_uniq
    on auth_permission (content_type_id, codename);

create table auth_user_user_permissions
(
    id            integer not null
        primary key autoincrement,
    user_id       integer not null
        references auth_user
            deferrable initially deferred,
    permission_id integer not null
        references auth_permission
            deferrable initially deferred
);

create index auth_user_user_permissions_permission_id_1fbb5f2c
    on auth_user_user_permissions (permission_id);

create index auth_user_user_permissions_user_id_a95ead1b
    on auth_user_user_permissions (user_id);

create unique index auth_user_user_permissions_user_id_permission_id_14a6b632_uniq
    on auth_user_user_permissions (user_id, permission_id);

create table django_admin_log
(
    id              integer           not null
        primary key autoincrement,
    object_id       text,
    object_repr     varchar(200)      not null,
    action_flag     smallint unsigned not null,
    change_message  text              not null,
    content_type_id integer
        references django_content_type
            deferrable initially deferred,
    user_id         integer           not null
        references auth_user
            deferrable initially deferred,
    action_time     datetime          not null,
    check ("action_flag" >= 0)
);

create index django_admin_log_content_type_id_c4bce8eb
    on django_admin_log (content_type_id);

create index django_admin_log_user_id_c564eba6
    on django_admin_log (user_id);

create unique index django_content_type_app_label_model_76bd3d3b_uniq
    on django_content_type (app_label, model);

create table django_migrations
(
    id      integer      not null
        primary key autoincrement,
    app     varchar(255) not null,
    name    varchar(255) not null,
    applied datetime     not null
);

create table django_session
(
    session_key  varchar(40) not null
        primary key,
    session_data text        not null,
    expire_date  datetime    not null
);

create index django_session_expire_date_a5c62663
    on django_session (expire_date);

create table sqlite_master
(
    type     TEXT,
    name     TEXT,
    tbl_name TEXT,
    rootpage INT,
    sql      TEXT
);

create table sqlite_sequence
(
    name,
    seq
);


