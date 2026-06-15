-- -- ============================================================
-- --  car_config_refactored – DML (dati di esempio)
-- --  Da eseguire DOPO 10_CREATE.sql:
-- --  psql -U postgres -d car_config -f 20_INSERT.sql
-- -- ============================================================

-- -- ── Regole di compatibilità ───────────────────────────────────────────────
-- INSERT INTO compatibility_rule (rule_type) VALUES
--     ('incompatible'),
--     ('requires');

-- -- ── Motorizzazioni ────────────────────────────────────────────────────────
-- INSERT INTO engine (fuel_type, power_hp, extra_price) VALUES
--     ('Benzina',   100,     0),   -- 1
--     ('Ibrido',    130,  2500),   -- 2  (CityGo)
--     ('Diesel',    150,     0),   -- 3
--     ('Benzina',   190,  3200),   -- 4  (TerraX)
--     ('Benzina',   380,     0),   -- 5
--     ('Elettrico', 450, 12000),   -- 6  (Aero S)
--     ('Diesel',    163,     0),   -- 7
--     ('Benzina',   204,  2800);   -- 8  (Elegance)

-- -- ── Modelli ───────────────────────────────────────────────────────────────
-- INSERT INTO model (name, brand, base_price, category, engine_id) VALUES
--     ('CityGo',   'Saetta Motors', 18500, 'city',    1),  -- id=1, motore base: 1.0 100cv
--     ('TerraX',   'Saetta Motors', 32900, 'suv',     3),  -- id=2, motore base: 2.0 TDI
--     ('Aero S',   'Saetta Motors', 48900, 'sport',   5),  -- id=3, motore base: 3.0 V6
--     ('Elegance', 'Saetta Motors', 41500, 'berlina', 7);  -- id=4, motore base: 2.0 TDI

-- -- ── Optional ──────────────────────────────────────────────────────────────
-- INSERT INTO optional (name, category, price) VALUES
--     ('Tetto panoramico',       'comfort',   1800),  -- 1
--     ('Premium Audio 12 Speaker','tech',     1200),  -- 2
--     ('Sedili riscaldati',      'comfort',    900),  -- 3
--     ('Adaptive Cruise Control','sicurezza', 1100),  -- 4
--     ('Driver Assist Pack',     'sicurezza', 1500),  -- 5
--     ('Cerchi 20" Sport',       'estetica',  2200),  -- 6
--     ('Interni Pelle Nappa',    'comfort',   2800),  -- 7
--     ('Trazione integrale AWD', 'sicurezza', 3500),  -- 8
--     ('Head-Up Display',        'tech',       950),  -- 9
--     ('Vernice metallizzata',   'estetica',   750);  -- 10

-- -- ── Catalogo optional per modello ─────────────────────────────────────────
-- -- CityGo (1): optional leggeri, no AWD, no V6 accessories
-- INSERT INTO model_optional VALUES
--     (1,1),(1,2),(1,3),(1,4),(1,5),(1,9),(1,10);

-- -- TerraX (2): SUV → tutto disponibile
-- INSERT INTO model_optional VALUES
--     (2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(2,7),(2,8),(2,9),(2,10);

-- -- Aero S (3): sportiva → no AWD separato (già incluso), no sedili riscaldati base
-- INSERT INTO model_optional VALUES
--     (3,1),(3,2),(3,4),(3,5),(3,6),(3,7),(3,9),(3,10);

-- -- Elegance (4): berlina luxury → tutto tranne cerchi sport
-- INSERT INTO model_optional VALUES
--     (4,1),(4,2),(4,3),(4,4),(4,5),(4,7),(4,8),(4,9),(4,10);

-- -- ── Regole di compatibilità tra optional ──────────────────────────────────
-- -- Tetto panoramico (1) incompatibile con Trazione AWD (8)
-- INSERT INTO compatibility (optional_id, optional_with_id, rule_id) VALUES (1, 8, 1);

-- -- Adaptive Cruise Control (4) richiede Driver Assist Pack (5)
-- INSERT INTO compatibility (optional_id, optional_with_id, rule_id) VALUES (4, 5, 2);

-- -- Head-Up Display (9) richiede Adaptive Cruise Control (4)
-- INSERT INTO compatibility (optional_id, optional_with_id, rule_id) VALUES (9, 4, 2);

-- -- ── Utenti di esempio ─────────────────────────────────────────────────────
-- -- NOTA: le password hash qui sotto sono placeholder.
-- -- Per creare utenti funzionanti usa POST /api/auth/register dopo l'avvio.
-- INSERT INTO app_user (tipo, email, password_hash) VALUES
--     ('admin',  'admin@saetta.it',  '$2b$12$PLACEHOLDER_ADMIN'),
--     ('client', 'mario@email.it',   '$2b$12$PLACEHOLDER_CLIENT1'),
--     ('client', 'giulia@email.it',  '$2b$12$PLACEHOLDER_CLIENT2');

-- INSERT INTO admin  (admin_id)  VALUES (1);
-- INSERT INTO client (client_id, first_name, last_name, phone) VALUES
--     (2, 'Mario',  'Rossi',   '3331234567'),
--     (3, 'Giulia', 'Verdi',   '3479876543');