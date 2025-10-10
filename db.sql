create table asset_types
(
    id         bigint unsigned auto_increment
        primary key,
    type_name  varchar(100) not null,
    created_at timestamp    null,
    updated_at timestamp    null
);

create table trackers
(
    id           bigint unsigned auto_increment primary key,
    tracker_code varchar(50) not null,
    created_at   timestamp   null,
    updated_at   timestamp   null,
    constraint trackers_tracker_code_unique
        unique (tracker_code)
);

create table assets
(
    id                     bigint unsigned auto_increment primary key,
    asset_code             varchar(50)                                                  not null,
    asset_type_id          bigint unsigned                                              null,
    ownership              enum ('Owned', 'Third-Party')                                not null,
    status                 enum ('empty', 'full')                                       not null,
    size                   enum ('20ft', '40ft', '45ft')                                not null,
    `condition`            enum ('operational', 'non_operational', 'under_maintenance') not null,
    category               enum ('excellent', 'good', 'bad', 'very_bad')                not null,
    manufactured_at        date                                                         not null,
    last_maintenance_at    date                                                         null,
    last_inspection_at     date                                                         null,
    next_inspection_due_at date                                                         null,
    max_payload_kg         int unsigned                                                 not null,
    created_at             timestamp                                                    null,
    updated_at             timestamp                                                    null,
    constraint assets_asset_code_unique
        unique (asset_code),
    constraint assets_asset_type_id_foreign
        foreign key (asset_type_id) references asset_types (id)
            on delete set null
);

create table customers
(
    id                    bigint unsigned auto_increment
        primary key,
    full_name             varchar(255) not null,
    identification_number varchar(50)  not null,
    email                 varchar(255) null,
    phone_number          varchar(50)  null,
    created_at            timestamp    null,
    updated_at            timestamp    null,
    constraint customers_email_unique
        unique (email),
    constraint customers_identification_number_unique
        unique (identification_number)
);

create table locations
(
    id            bigint unsigned auto_increment
        primary key,
    location_name varchar(255)                                    not null,
    address       varchar(255)                                    null,
    city          varchar(100)                                    null,
    country       varchar(100)                                    null,
    location_type enum ('port', 'warehouse', 'customer_facility') not null,
    created_at    timestamp                                       null,
    updated_at    timestamp                                       null
);

create table routes
(
    id                      bigint unsigned auto_increment
        primary key,
    origin_location_id      bigint unsigned not null,
    destination_location_id bigint unsigned not null,
    created_at              timestamp       null,
    updated_at              timestamp       null,
    constraint routes_destination_location_id_foreign
        foreign key (destination_location_id) references locations (id)
            on delete cascade,
    constraint routes_origin_location_id_foreign
        foreign key (origin_location_id) references locations (id)
            on delete cascade
);

create table users
(
    id                bigint unsigned auto_increment
        primary key,
    name              varchar(255) not null,
    email             varchar(255) not null,
    email_verified_at timestamp    null,
    password          varchar(255) not null,
    remember_token    varchar(100) null,
    created_at        timestamp    null,
    updated_at        timestamp    null,
    constraint users_email_unique
        unique (email)
);

create table vessels
(
    id                    bigint unsigned auto_increment
        primary key,
    vessel_name           varchar(255) not null,
    imo_number            varchar(20)  not null,
    mmsi_number           varchar(20)  null,
    call_sign             varchar(20)  null,
    ais_transponder_class varchar(50)  null,
    general_vessel_type   varchar(100) null,
    detailed_vessel_type  varchar(100) null,
    service_status        varchar(100) null,
    port_of_registry      varchar(100) null,
    year_built            smallint     null,
    dimensions            varchar(100) null,
    design_description    text         null,
    last_dry_dock_survey  date         null,
    tonnage_info          varchar(255) null,
    engine_info           varchar(255) null,
    capacity_info         varchar(255) null,
    created_at            timestamp    null,
    updated_at            timestamp    null,
    constraint vessels_imo_number_unique
        unique (imo_number),
    constraint vessels_mmsi_number_unique
        unique (mmsi_number)
);

create table voyages
(
    id                 bigint unsigned auto_increment
        primary key,
    route_id           bigint unsigned               not null,
    vessel_id          bigint unsigned               not null,
    departure_datetime datetime                      null,
    arrival_datetime   datetime                      null,
    status             varchar(50) default 'planned' not null,
    created_at         timestamp                     null,
    updated_at         timestamp                     null,
    constraint voyages_route_id_foreign
        foreign key (route_id) references routes (id)
            on delete cascade,
    constraint voyages_vessel_id_foreign
        foreign key (vessel_id) references vessels (id)
            on delete cascade
);

create table shipments
(
    id                      bigint unsigned auto_increment
        primary key,
    tracking_code           varchar(50)                    not null,
    customer_id             bigint unsigned                not null,
    voyage_id               bigint unsigned                null,
    origin_location_id      bigint unsigned                not null,
    destination_location_id bigint unsigned                not null,
    creation_datetime       datetime                       not null,
    declared_value          decimal(12, 2)                 null,
    current_status          varchar(100) default 'created' not null,
    created_at              timestamp                      null,
    updated_at              timestamp                      null,
    constraint shipments_tracking_code_unique
        unique (tracking_code),
    constraint shipments_customer_id_foreign
        foreign key (customer_id) references customers (id)
            on delete cascade,
    constraint shipments_destination_location_id_foreign
        foreign key (destination_location_id) references locations (id)
            on delete cascade,
    constraint shipments_origin_location_id_foreign
        foreign key (origin_location_id) references locations (id)
            on delete cascade,
    constraint shipments_voyage_id_foreign
        foreign key (voyage_id) references voyages (id)
            on delete set null
);

create table bills_of_lading
(
    id                   bigint unsigned auto_increment
        primary key,
    shipment_id          bigint unsigned      not null,
    bol_number           varchar(100)         not null,
    issue_date           date                 not null,
    terms_and_conditions text                 null,
    shipper_details      text                 null,
    consignee_details    text                 null,
    is_hazardous         tinyint(1) default 0 not null,
    created_at           timestamp            null,
    updated_at           timestamp            null,
    constraint bills_of_lading_bol_number_unique
        unique (bol_number),
    constraint bills_of_lading_shipment_id_unique
        unique (shipment_id),
    constraint bills_of_lading_shipment_id_foreign
        foreign key (shipment_id) references shipments (id)
            on delete cascade
);

create table shipment_items
(
    id          bigint unsigned auto_increment
        primary key,
    shipment_id bigint unsigned not null,
    asset_id    bigint unsigned not null,
    description text            null,
    weight_kg   decimal(10, 2)  null,
    dimensions  varchar(100)    null,
    created_at  timestamp       null,
    updated_at  timestamp       null,
    constraint shipment_items_asset_id_foreign
        foreign key (asset_id) references assets (id)
            on delete cascade,
    constraint shipment_items_shipment_id_foreign
        foreign key (shipment_id) references shipments (id)
            on delete cascade
);

create table tracking_events
(
    id             bigint unsigned auto_increment
        primary key,
    shipment_id    bigint unsigned not null,
    location_id    bigint unsigned null,
    event_datetime datetime        not null,
    event_type     varchar(100)    not null,
    notes          text            null,
    created_at     timestamp       null,
    updated_at     timestamp       null,
    constraint tracking_events_location_id_foreign
        foreign key (location_id) references locations (id)
            on delete set null,
    constraint tracking_events_shipment_id_foreign
        foreign key (shipment_id) references shipments (id)
            on delete cascade
);

