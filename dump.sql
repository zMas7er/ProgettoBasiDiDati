create table TechHub_azienda
(
    ID_azienda   integer      not null
        primary key autoincrement,
    nome_azienda varchar(100) not null,
    sede_legale  varchar(100) not null
);

create table TechHub_componenti
(
    ID_componente integer      not null
        primary key autoincrement,
    nome          varchar(100) not null,
    marca         varchar(50)  not null,
    tipologia     varchar(50)  not null,
    azienda_id    integer      not null
        references TechHub_azienda
            deferrable initially deferred
);

create index TechHub_componenti_azienda_id_f6719760
    on TechHub_componenti (azienda_id);

create table TechHub_utente
(
    ID_utente    integer      not null
        primary key autoincrement,
    email        varchar(254) not null
        unique,
    data_nascita date         not null
);

create table TechHub_ordine
(
    ID_ordine      integer     not null
        primary key autoincrement,
    data_creazione datetime    not null,
    stato          varchar(20) not null,
    utente_id      integer     not null
        references TechHub_utente
            deferrable initially deferred
);

create table TechHub_contiene
(
    id            integer not null
        primary key autoincrement,
    componente_id integer not null
        references TechHub_componenti
            deferrable initially deferred,
    ordine_id     integer not null
        references TechHub_ordine
            deferrable initially deferred
);

create index TechHub_contiene_componente_id_a81d3c4a
    on TechHub_contiene (componente_id);

create index TechHub_contiene_ordine_id_7ea80e7b
    on TechHub_contiene (ordine_id);

create index TechHub_ordine_utente_id_bf1bb8df
    on TechHub_ordine (utente_id);

create table TechHub_pagamento
(
    ID_pagamento integer     not null
        primary key autoincrement,
    metodo       varchar(20) not null,
    esito        varchar(20) not null,
    ordine_id    integer     not null
        unique
        references TechHub_ordine
            deferrable initially deferred
);

create table TechHub_recensione
(
    ID_recensione integer not null
        primary key autoincrement,
    voto          integer not null,
    testo         text    not null,
    componente_id integer not null
        references TechHub_componenti
            deferrable initially deferred,
    utente_id     integer not null
        references TechHub_utente
            deferrable initially deferred
);

create index TechHub_recensione_componente_id_a69364ab
    on TechHub_recensione (componente_id);

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


