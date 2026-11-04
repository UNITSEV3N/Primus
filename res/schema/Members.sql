-- Create and use the default database
CREATE DATABASE IF NOT EXISTS primus;
USE primus;

-- REGISTRY -------------------------------------------------------------------------

-- Holds all server members
CREATE TABLE IF NOT EXISTS members
(
    id              BIGINT PRIMARY KEY,
    username        VARCHAR(100) NOT NULL,
    platform        VARCHAR(25) NOT NULL,
    joined          TIMESTAMP NOT NULL,
    registry        ENUM('RECRUIT', 'REGISTERED') NOT NULL DEFAULT 'RECRUIT'
);

-- Member registry
CREATE TABLE IF NOT EXISTS registry
(
    id              BIGINT PRIMARY KEY,
    char_name       VARCHAR(25) NOT NULL DEFAULT 'NONE',
    rank_name       VARCHAR(100) NOT NULL DEFAULT 'NONE',
    rank_abbr       VARCHAR(25) NOT NULL DEFAULT 'NONE',
    thumbnail       TEXT,

    FOREIGN KEY (id) REFERENCES members(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Member progression
CREATE TABLE IF NOT EXISTS progression
(
    id              BIGINT PRIMARY KEY,
    hierarchy       INTEGER NULL,
    current_point   INTEGER NOT NULL DEFAULT 0,
    current_events  INTEGER NOT NULL DEFAULT 0,
    held_events     INTEGER NOT NULL DEFAULT 0,

    FOREIGN KEY (id) REFERENCES members(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Member ribbons (one-to-many)
CREATE TABLE IF NOT EXISTS ribbons
(
    id              BIGINT PRIMARY KEY AUTO_INCREMENT,
    member_id       BIGINT NOT NULL,
    ribbon_name     VARCHAR(60) NOT NULL,
    role_id         BIGINT NOT NULL,

    UNIQUE (member_id, role_id),

    FOREIGN KEY (member_id) REFERENCES members(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Member activity
CREATE TABLE IF NOT EXISTS activity
(
    id              BIGINT PRIMARY KEY,
    barred          BOOLEAN NOT NULL DEFAULT FALSE,
    barr_reason     VARCHAR(255),
    activity        ENUM('ACTIVE', 'LEAVE', 'NONE') NOT NULL DEFAULT 'NONE',

    FOREIGN KEY (id) REFERENCES members(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Member leave status
CREATE TABLE IF NOT EXISTS member_leave
(
    id              BIGINT PRIMARY KEY AUTO_INCREMENT,
    member_id       BIGINT NOT NULL,
    start_date      TIMESTAMP NULL,
    end_date        TIMESTAMP NULL,
    reason          TEXT,

    FOREIGN KEY (member_id) REFERENCES members(id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

