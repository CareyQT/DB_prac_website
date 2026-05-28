/*
Tales From The Spiral

*/

DELIMITER $$

CREATE PROCEDURE ResetDatabase()
    
    Begin


    SET FOREIGN_KEY_CHECKS = 0;
    START TRANSACTION;

    DROP TABLE IF EXISTS NPC_Abilities;
    DROP TABLE IF EXISTS Enemy_Abilities;
    DROP TABLE IF EXISTS Area_Enemies;
    DROP TABLE IF EXISTS Area_Hazards;
    DROP TABLE IF EXISTS NPCs;
    DROP TABLE IF EXISTS Abilities;
    DROP TABLE IF EXISTS Enemies;
    DROP TABLE IF EXISTS Hazards;
    DROP TABLE IF EXISTS Areas;

    SET FOREIGN_KEY_CHECKS = 1;


    /*Main tables*/

    CREATE TABLE Areas (
        areaID VARCHAR(255) NOT NULL,
        areaLevel INT NOT NULL,
        PRIMARY KEY (areaID)
    );

    CREATE TABLE Hazards (
        hazardID VARCHAR(255) NOT NULL,
        damage INT NOT NULL,
        PRIMARY KEY (hazardID)
    );

    CREATE TABLE Enemies (
        enemyID VARCHAR(255) NOT NULL,
        hp INT NOT NULL,
        damage INT NOT NULL,
        PRIMARY KEY (enemyID)
    );

    CREATE TABLE Abilities (
        abilityID VARCHAR(255) NOT NULL,
        damage INT,
        PRIMARY KEY (abilityID)
    );

    CREATE TABLE NPCs (
        npcID VARCHAR(255) NOT NULL,
        hp INT NOT NULL,
        quest BOOLEAN NOT NULL,
        shopkeeper BOOLEAN NOT NULL,
        areaID VARCHAR(255) NOT NULL,
        enemyID VARCHAR(255),
        PRIMARY KEY (npcID),
        FOREIGN KEY (areaID) REFERENCES Areas(areaID)
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
        FOREIGN KEY (enemyID) REFERENCES Enemies(enemyID)
            ON UPDATE CASCADE
            ON DELETE SET NULL
    );


    /*Intersection tables*/

    CREATE TABLE Area_Hazards (
        areaID VARCHAR(255) NOT NULL,
        hazardID VARCHAR(255) NOT NULL,
        PRIMARY KEY (areaID, hazardID),
        FOREIGN KEY (areaID) REFERENCES Areas(areaID)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        FOREIGN KEY (hazardID) REFERENCES Hazards(hazardID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );

    CREATE TABLE Area_Enemies (
        areaID VARCHAR(255) NOT NULL,
        enemyID VARCHAR(255) NOT NULL,
        PRIMARY KEY (areaID, enemyID),
        FOREIGN KEY (areaID) REFERENCES Areas(areaID)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        FOREIGN KEY (enemyID) REFERENCES Enemies(enemyID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );

    CREATE TABLE Enemy_Abilities (
        enemyID VARCHAR(255) NOT NULL,
        abilityID VARCHAR(255) NOT NULL,
        PRIMARY KEY (enemyID, abilityID),
        FOREIGN KEY (enemyID) REFERENCES Enemies(enemyID)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        FOREIGN KEY (abilityID) REFERENCES Abilities(abilityID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );

    CREATE TABLE NPC_Abilities (
        npcID VARCHAR(255) NOT NULL,
        abilityID VARCHAR(255) NOT NULL,
        PRIMARY KEY (npcID, abilityID),
        FOREIGN KEY (npcID) REFERENCES NPCs(npcID)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
        FOREIGN KEY (abilityID) REFERENCES Abilities(abilityID)
            ON UPDATE CASCADE
            ON DELETE CASCADE
    );


    /*Sample data
    3-5 rows per table*/

    INSERT INTO Areas (areaID, areaLevel)
    VALUES
    ('Whispering_Woods', 3),
    ('Sunken_Ruins', 7),
    ('Ironkeep_Village', 2);

    INSERT INTO Hazards (hazardID, damage)
    VALUES
    ('Poison_Fog', 8),
    ('Spike_Trap', 12),
    ('Falling_Rocks', 15);

    INSERT INTO Enemies (enemyID, hp, damage)
    VALUES
    ('Goblin_Scout', 35, 6),
    ('Bone_Warden', 60, 12),
    ('Marsh_Wraith', 50, 10);

    INSERT INTO Abilities (abilityID, damage)
    VALUES
    ('Quick_Slash', 7),
    ('Fireball', 18),
    ('Heal', NULL),
    ('Shield_Bash', 10);

    INSERT INTO NPCs (npcID, hp, quest, shopkeeper, areaID, enemyID)
    VALUES
    ('Lena_the_Merchant', 40, FALSE, TRUE, 'Ironkeep_Village', NULL),
    ('Brother_Cale', 45, TRUE, FALSE, 'Whispering_Woods', NULL),
    ('Mira_the_Hunted', 38, TRUE, FALSE, 'Sunken_Ruins', 'Marsh_Wraith');


    /*Intersection data*/

    INSERT INTO Area_Hazards (areaID, hazardID)
    VALUES
    ('Whispering_Woods', 'Poison_Fog'),
    ('Sunken_Ruins', 'Spike_Trap'),
    ('Sunken_Ruins', 'Falling_Rocks'),
    ('Ironkeep_Village', 'Spike_Trap');

    INSERT INTO Area_Enemies (areaID, enemyID)
    VALUES
    ('Whispering_Woods', 'Goblin_Scout'),
    ('Sunken_Ruins', 'Bone_Warden'),
    ('Sunken_Ruins', 'Marsh_Wraith'),
    ('Ironkeep_Village', 'Goblin_Scout');

    INSERT INTO Enemy_Abilities (enemyID, abilityID)
    VALUES
    ('Goblin_Scout', 'Quick_Slash'),
    ('Bone_Warden', 'Shield_Bash'),
    ('Marsh_Wraith', 'Fireball'),
    ('Marsh_Wraith', 'Quick_Slash');

    INSERT INTO NPC_Abilities (npcID, abilityID)
    VALUES
    ('Lena_the_Merchant', 'Heal'),
    ('Brother_Cale', 'Shield_Bash'),
    ('Mira_the_Hunted', 'Fireball');

    COMMIT;
END$$

DELIMITER ;