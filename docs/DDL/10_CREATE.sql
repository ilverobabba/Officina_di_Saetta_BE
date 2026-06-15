-- -- ============================================================
-- --  car_config_refactored – DDL
-- --  Prerequisiti: CREATE DATABASE car_config;
-- --  Poi: psql -U postgres -d car_config -f 10_CREATE.sql
-- -- ============================================================

-- -- ── Utenti ────────────────────────────────────────────────────────────────

-- CREATE TABLE IF NOT EXISTS app_user (
--     user_id       SERIAL       PRIMARY KEY,
--     tipo          VARCHAR(20)  NOT NULL,          -- 'client' | 'admin'
--     email         VARCHAR(150) NOT NULL UNIQUE,
--     password_hash VARCHAR(200) NOT NULL
-- );

-- CREATE TABLE IF NOT EXISTS client (
--     client_id  INTEGER      PRIMARY KEY REFERENCES app_user(user_id) ON DELETE CASCADE,
--     first_name VARCHAR(100) NOT NULL,
--     last_name  VARCHAR(100) NOT NULL,
--     phone      VARCHAR(30)
-- );

-- CREATE TABLE IF NOT EXISTS admin (
--     admin_id INTEGER PRIMARY KEY REFERENCES app_user(user_id) ON DELETE CASCADE
-- );

-- -- ── Motorizzazioni ────────────────────────────────────────────────────────

-- CREATE TABLE IF NOT EXISTS engine (
--     engine_id   SERIAL        PRIMARY KEY,
--     fuel_type   VARCHAR(50)   NOT NULL,
--     power_hp    INTEGER       NOT NULL CHECK (power_hp > 0),
--     extra_price NUMERIC(10,2) NOT NULL DEFAULT 0 CHECK (extra_price >= 0)
-- );

-- -- ── Modelli auto ──────────────────────────────────────────────────────────

-- CREATE TABLE IF NOT EXISTS model (
--     model_id   SERIAL        PRIMARY KEY,
--     name       VARCHAR(100)  NOT NULL,
--     brand      VARCHAR(100)  NOT NULL,
--     base_price NUMERIC(10,2) NOT NULL CHECK (base_price >= 0),
--     category   VARCHAR(50),
--     engine_id  INTEGER       NOT NULL REFERENCES engine(engine_id)
-- );

-- -- ── Optional ──────────────────────────────────────────────────────────────

-- CREATE TABLE IF NOT EXISTS optional (
--     optional_id SERIAL        PRIMARY KEY,
--     name        VARCHAR(100)  NOT NULL,
--     category    VARCHAR(50),
--     price       NUMERIC(10,2) NOT NULL DEFAULT 0 CHECK (price >= 0)
-- );

-- -- ── Catalogo optional per modello (N:M) ───────────────────────────────────

-- CREATE TABLE IF NOT EXISTS model_optional (
--     model_id    INTEGER NOT NULL REFERENCES model(model_id)       ON DELETE CASCADE,
--     optional_id INTEGER NOT NULL REFERENCES optional(optional_id) ON DELETE CASCADE,
--     PRIMARY KEY (model_id, optional_id)
-- );

-- -- ── Regole di compatibilità ───────────────────────────────────────────────

-- CREATE TABLE IF NOT EXISTS compatibility_rule (
--     rule_id   SERIAL      PRIMARY KEY,
--     rule_type VARCHAR(50) NOT NULL    -- 'incompatible' | 'requires'
-- );

-- CREATE TABLE IF NOT EXISTS compatibility (
--     compatibility_id SERIAL  PRIMARY KEY,
--     optional_id      INTEGER NOT NULL REFERENCES optional(optional_id) ON DELETE CASCADE,
--     optional_with_id INTEGER NOT NULL REFERENCES optional(optional_id) ON DELETE CASCADE,
--     rule_id          INTEGER NOT NULL REFERENCES compatibility_rule(rule_id) ON DELETE CASCADE,
--     CHECK (optional_id <> optional_with_id)
-- );

-- -- ── Configurazioni ────────────────────────────────────────────────────────

-- CREATE TABLE IF NOT EXISTS configuration (
--     configuration_id SERIAL        PRIMARY KEY,
--     name             VARCHAR(100)  NOT NULL,
--     status           VARCHAR(20)   NOT NULL DEFAULT 'draft',  -- 'draft' | 'saved' | 'quoted'
--     total_price      NUMERIC(10,2) NOT NULL DEFAULT 0,
--     client_id        INTEGER       NOT NULL REFERENCES client(client_id)   ON DELETE CASCADE,
--     model_id         INTEGER       NOT NULL REFERENCES model(model_id),
--     engine_id        INTEGER       NOT NULL REFERENCES engine(engine_id)
-- );

-- CREATE TABLE IF NOT EXISTS configuration_optional (
--     configuration_id INTEGER NOT NULL REFERENCES configuration(configuration_id) ON DELETE CASCADE,
--     optional_id      INTEGER NOT NULL REFERENCES optional(optional_id)           ON DELETE CASCADE,
--     PRIMARY KEY (configuration_id, optional_id)
-- );

-- -- ── Preventivi ────────────────────────────────────────────────────────────

-- CREATE TABLE IF NOT EXISTS quote (
--     quote_id         SERIAL        PRIMARY KEY,
--     quote_number     VARCHAR(30)   NOT NULL UNIQUE,
--     issued_at        TIMESTAMPTZ   NOT NULL DEFAULT NOW(),
--     status           VARCHAR(20)   NOT NULL DEFAULT 'pending',  -- 'pending' | 'accepted' | 'rejected' | 'expired'
--     final_price      NUMERIC(10,2) NOT NULL,
--     discount_pct     NUMERIC(5,2)  NOT NULL DEFAULT 0
--                          CHECK (discount_pct >= 0 AND discount_pct <= 100),
--     configuration_id INTEGER       NOT NULL UNIQUE REFERENCES configuration(configuration_id) ON DELETE CASCADE
-- );