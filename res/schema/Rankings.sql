USE primus;

CREATE TABLE IF NOT EXISTS ranks
(
    id                  INT UNSIGNED        NOT NULL AUTO_INCREMENT PRIMARY KEY,
    code                VARCHAR(10)         NOT NULL UNIQUE,
    title               VARCHAR(64)         NOT NULL,
    abbreviation        VARCHAR(10)         NOT NULL UNIQUE,
    points              INT UNSIGNED        NOT NULL DEFAULT 0,
    required_events     INT UNSIGNED        NOT NULL DEFAULT 0,
    held_events         INT UNSIGNED        NOT NULL DEFAULT 0,
    auto_barr           BOOLEAN             NOT NULL DEFAULT FALSE,
    thumbnail_path      VARCHAR(512)        NULL,
    role_name           VARCHAR(255)        NOT NULL,
    role_id             BIGINT UNSIGNED     NOT NULL UNIQUE,
    sort_order          SMALLINT UNSIGNED   NOT NULL UNIQUE
);

-- One to Many (1:Many)
CREATE TABLE IF NOT EXISTS training
(
    id                  INT UNSIGNED        NOT NULL AUTO_INCREMENT PRIMARY KEY,
    code                VARCHAR(10)         NOT NULL UNIQUE,
    name                VARCHAR(100)        NOT NULL UNIQUE,
    role_id             BIGINT UNSIGNED     NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS rank_required_training
(
    rank_id             INT UNSIGNED        NOT NULL,
    training_id         INT UNSIGNED        NOT NULL,

    PRIMARY KEY (rank_id, training_id),

    FOREIGN KEY (rank_id)     REFERENCES ranks(id)    ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (training_id) REFERENCES training(id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS locked_ranks
(
    role_id             BIGINT UNSIGNED     NOT NULL PRIMARY KEY,
    role_name           VARCHAR(255)        NOT NULL UNIQUE,

    FOREIGN KEY (role_id) REFERENCES ranks(role_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

--- INSERT ---

USE primus;
SET NAMES utf8mb4;  -- role names contain the "│" character

-- ============================================================
-- TRAINING
-- ============================================================
INSERT INTO training (code, name, role_id) VALUES
    ('BCT',  'Basic Combat Training',                  1239677485613056001),
    ('NCO',  'Sergeant & Corporal School',             1239677748486864917),
    ('SNCO', 'Staff Non Commissioned Officer Academy', 1285650796054319218);

-- ============================================================
-- RANKS  (sort_order follows the order in your JSON, so N/A sits before O-11)
-- ============================================================
INSERT INTO ranks
    (code, title, abbreviation, points, required_events, held_events, auto_barr, thumbnail_path, role_name, role_id, sort_order)
VALUES
    ('E-1',  'Private',                                'PVT',  0,   0, 0, FALSE, 'https://i.ibb.co/M5ynD7sq/E-1-PVT-moshed-10-29-18-05-13-493.gif',     'E-1 [PVT]│Private',                                    944111663370633236,  1),
    ('E-2',  'Private First Class',                    'PFC',  200, 1, 0, FALSE, 'https://i.ibb.co/67xJvkbD/E-2-PFC-moshed-10-29-18-05-37-694.gif',     'E-2 [PFC]│Private 1''st Class',                         1003755866673135656, 2),
    ('E-3',  'Lance Corporal',                         'LCPL', 225, 1, 0, FALSE, 'https://i.ibb.co/GQ5rvrpj/E-3-LCPL-moshed-10-29-18-05-52-285.gif',    'E-3 [LCPL]│Lance Corporal',                             1003754869024379020, 3),
    ('E-4',  'Corporal',                               'CPL',  250, 1, 0, TRUE,  'https://i.ibb.co/4wp4Vmp2/E-4-CPL-moshed-10-29-18-06-19-602.gif',     'E-4 [CPL]│Corporal',                                    944111931667664988,  4),
    ('E-5',  'Sergeant',                               'SGT',  300, 0, 1, TRUE,  'https://i.ibb.co/fYZynMSN/E-5-SGT-moshed-10-29-18-06-36-015.gif',     'E-5 [SGT]│Sergeant',                                    944112079927934986,  5),
    ('E-6',  'Staff Sergeant',                         'SSG',  325, 0, 1, TRUE,  'https://i.ibb.co/vCy7mVf6/E-6-SSG-moshed-10-29-18-06-53-812.gif',     'E-6 [SSG]│Staff Sergeant',                              1003756148589072394, 6),
    ('E-7',  'Gunnery Sergeant',                       'GSG',  350, 0, 1, FALSE, 'https://i.ibb.co/hFmdkCfj/E-7-GSG-moshed-10-29-18-07-14-123.gif',     'E-7 [GSG]│Gunnery Sergeant',                            1003756514156224512, 7),
    ('E-8',  'Master Sergeant',                        'MSG',  375, 0, 1, FALSE, 'https://i.ibb.co/6kQTg1G/E-8-MSG-moshed-10-29-18-07-44-049.gif',      'E-8 [MSG]│Master Sergeant',                             1003756755211276419, 8),
    ('E-9',  'First Sergeant',                         '1SG',  400, 0, 1, FALSE, 'https://i.ibb.co/twbWL19Q/E-9-1-SG-moshed-10-29-18-08-04-251.gif',    'E-9 [1SG]│1''st Sergeant',                              1003756936287768608, 9),
    ('E-10', 'Master Gunnery Sergeant',                'MGS',  425, 0, 1, FALSE, 'https://i.ibb.co/9C8HTd9/E-10-MGS-moshed-10-29-18-08-24-566.gif',     'E-10 [MGS]│Master Gunnery Sergeant',                    1003757331110174782, 10),
    ('E-11', 'Sergeant Major',                         'SGM',  0,   0, 0, FALSE, 'https://i.ibb.co/gMmRC6YD/E-11-SGM-moshed-10-29-18-08-45-153.gif',    'E-11 [SGM]│Sergeant Major',                            1003757801430073350, 11),
    ('E-12', 'Sergeant Major of the Marine Corps',     'SMMC', 0,   0, 1, FALSE, 'https://i.ibb.co/vCK084R1/E-12-SMMC-moshed-10-29-18-09-01-343.gif',   'E-12 [SMMC]│Sergeant Major of The Marine Corps',        1003758029205934184, 12),
    ('E-13', 'Senior Enlisted Advisor to The Chairman','SEAC', 0,   0, 1, TRUE,  'https://i.ibb.co/sJzt5bwV/E-13-SEAC-moshed-10-29-18-09-16-865.gif',   'E-13 [SEAC]│Senior Enlisted Advisor to The Chairman',   1245068747669115046, 13),
    ('W-1',  'Warrant Officer 1',                      'WO1',  0,   0, 0, TRUE,  'https://i.ibb.co/zh50gMmk/W-1-WO1-moshed-10-29-18-10-26-597.gif',     'W-1 [WO1]│Warrant Officer 1''st Grade',                 1003758284781662433, 14),
    ('W-2',  'Chief Warrant Officer 2',                'CWO2', 0,   0, 0, TRUE,  'https://i.ibb.co/RGWfXPtg/W-2-CWO2-moshed-10-29-18-10-41-886.gif',    'W-2 [CWO2]│Chief Warrant Officer 2''nd Grade',           1003758628278382592, 15),
    ('W-3',  'Chief Warrant Officer 3',                'CWO3', 0,   0, 0, TRUE,  'https://i.ibb.co/1YBq1GGt/W-3-CWO3-moshed-10-29-18-10-55-943.gif',    'W-3 [CWO3]│Chief Warrant Officer 3''rd Grade',           1003758961331294349, 16),
    ('W-4',  'Chief Warrant Officer 4',                'CWO4', 0,   0, 0, TRUE,  'https://i.ibb.co/1J4ZJbDb/W-4-CWO4-moshed-10-29-18-11-13-142.gif',    'W-4 [CWO4]│Chief Warrant Officer 4''th Grade',           1003759195918696528, 17),
    ('W-5',  'Chief Warrant Officer of the Marine Corps','CWMC',0,  0, 0, TRUE,  'https://i.ibb.co/k2vxBhFK/W-5-CWO5-moshed-10-29-18-11-27-730.gif',    'W-5 [CWMC]│Chief Warrant Officer of the Marine Corps',  1003759844332933272, 18),
    ('O-1',  'Second Lieutenant',                      '2LT',  400, 0, 0, FALSE, 'https://i.ibb.co/S7B6gGfG/O-1-2-LT-moshed-10-28-19-58-08-937.gif',    'O-1 [2LT]│2''nd Lieutenant',                            1003760362388201682, 19),
    ('O-2',  'First Lieutenant',                       '1LT',  400, 0, 1, FALSE, 'https://i.ibb.co/vCXrVnhp/O-2-1-LT-moshed-10-28-19-58-55-396.gif',    'O-2 [1LT]│1''st Lieutenant',                            1003760682254204948, 20),
    ('O-3',  'Captain',                                'CPT',  425, 0, 1, FALSE, 'https://i.ibb.co/ymZr4Byg/O-3-CPT-moshed-10-28-19-59-23-500.gif',     'O-3 [CPT]│Captain',                                     944111922024968213,  21),
    ('O-4',  'Major',                                  'MAJ',  450, 0, 1, FALSE, 'https://i.ibb.co/tw2btXqN/O-4-MAJ-moshed-10-28-19-59-57-268.gif',     'O-4 [MAJ]│Major',                                       944112419452641290,  22),
    ('O-5',  'Lieutenant Colonel',                     'LTC',  475, 0, 1, FALSE, 'https://i.ibb.co/Wpff3rJM/O-5-LTC-moshed-10-28-20-00-28-638.gif',     'O-5 [LTC]│Lieutenant Colonel',                          1003761010399784970, 23),
    ('O-6',  'Colonel',                                'COL',  500, 0, 1, TRUE,  'https://i.ibb.co/5ggWnZ0w/O-6-COL-moshed-10-28-20-00-52-532.gif',     'O-6 [COL]│Colonel',                                     944112823749988383,  24),
    ('O-7',  'Brigadier General',                      'BGE',  0,   0, 1, FALSE, 'https://i.ibb.co/MxKMt92b/O-7-BGE-moshed-10-28-20-01-36-710.gif',     'O-7 [BGE]│Brigadier General',                           944113144681332756,  25),
    ('O-8',  'Major General',                          'MGE',  0,   0, 1, FALSE, 'https://i.ibb.co/bMQ2pc7J/O-8-MAG-moshed-10-28-20-02-06-480.gif',     'O-8 [MAG]│Major General',                              963796891550773309,  26),
    ('O-9',  'Lieutenant General',                     'LTG',  0,   0, 1, FALSE, 'https://i.ibb.co/TMfsTL4r/O-9-LTG-moshed-10-28-20-02-31-148.gif',     'O-9 [LTG]│Lieutenant General',                          944113263791198228,  27),
    ('O-10', 'General',                                'GEN',  0,   0, 1, FALSE, 'https://i.ibb.co/Vc2wsdWc/O-10-GEN-moshed-10-28-20-02-50-239.gif',    'O-10 [GEN]│General',                                   944113428631547944,  28),
    ('N/A',  'Senior Executive Service',               'SES',  0,   0, 1, FALSE, 'https://i.ibb.co/nNCt77vZ/N-A-SES-moshed-12-16-17-27-24-805.gif',     'N/A [SES]│Senior Executive Service',                    1317934288246804480, 29),
    ('O-11', 'Fleet Admiral',                          'FADM', 0,   0, 1, FALSE, 'https://i.ibb.co/qLVytHnY/O-11-FADM-moshed-10-28-20-03-06-383.gif',   'O-11 [FADM]│Fleet Admiral',                             1195415351350018059, 30);

-- ============================================================
-- RANK REQUIRED TRAINING
-- Derived from your JSON, which follows a clean pattern:
--   BCT  : every rank except E-1 and N/A
--   NCO  : E-4 and above (everything except E-1..E-3 and N/A)
--   SNCO : E-6 and above (everything except E-1..E-5 and N/A)
-- ============================================================
INSERT INTO rank_required_training (rank_id, training_id)
SELECT r.id, t.id
FROM ranks r
JOIN training t ON t.code = 'BCT'
WHERE r.code NOT IN ('E-1', 'N/A');

INSERT INTO rank_required_training (rank_id, training_id)
SELECT r.id, t.id
FROM ranks r
JOIN training t ON t.code = 'NCO'
WHERE r.code NOT IN ('E-1', 'E-2', 'E-3', 'N/A');

INSERT INTO rank_required_training (rank_id, training_id)
SELECT r.id, t.id
FROM ranks r
JOIN training t ON t.code = 'SNCO'
WHERE r.code NOT IN ('E-1', 'E-2', 'E-3', 'E-4', 'E-5', 'N/A');

-- ============================================================
-- LOCKED RANKS
-- Cleaned: dropped the ",O-7" typo, the duplicate O-8/O-9 entries,
-- and "O-12" (no such rank in your data).
-- ============================================================
INSERT INTO locked_ranks (role_id, role_name)
SELECT role_id, role_name
FROM ranks
WHERE code IN (
    'E-11', 'E-12', 'E-13',
    'W-1', 'W-2', 'W-3', 'W-4', 'W-5',
    'O-1', 'O-7', 'O-8', 'O-9', 'O-10', 'O-11',
    'N/A'
);
