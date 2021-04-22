CREATE DATABASE sheet;
use sheet;

CREATE TABLE IF NOT EXISTS sheet (
    `lname` VARCHAR(50) CHARACTER SET utf8,
    `fname` VARCHAR(50) CHARACTER SET utf8,
    `ssn` VARCHAR(50) CHARACTER SET utf8,
    `test1` INT,
    `test2` INT,
    `test3` INT,
    `test4` INT,
    `final` INT,
    `grade` VARCHAR(50) CHARACTER SET utf8
);
INSERT INTO sheet VALUES
    ('Alfalfa','   "Aloysius"','   "123-45-6789"',40,90,100,83,49,'   "D-"'),
    ('Alfred','    "University"',' "123-12-1234"',41,97,96,97,48,'   "D+"'),
    ('Gerty','     "Gramma"','     "567-89-0123"',41,80,60,40,44,'   "C"'),
    ('Android','   "Electric"','   "087-65-4321"',42,23,36,45,47,'   "B-"'),
    ('Bumpkin','   "Fred"','       "456-78-9012"',43,78,88,77,45,'   "A-"'),
    ('Rubble','    "Betty"','      "234-56-7890"',44,90,80,90,46,'   "C-"'),
    ('Noshow','    "Cecil"','      "345-67-8901"',45,11,-1,4,43,'   "F"'),
    ('Buff','      "Bif"','        "632-79-9939"',46,20,30,40,50,'   "B+"'),
    ('Airpump','   "Andrew"','     "223-45-6789"',49,1,90,100,83,'   "A"'),
    ('Backus','    "Jim"','        "143-12-1234"',48,1,97,96,97,'   "A+"'),
    ('Carnivore',' "Art"','        "565-89-0123"',44,1,80,60,40,'   "D+"'),
    ('Dandy','     "Jim"','        "087-75-4321"',47,1,23,36,45,'   "C+"'),
    ('Elephant','  "Ima"','        "456-71-9012"',45,1,78,88,77,'   "B-"'),
    ('Franklin','  "Benny"','      "234-56-2890"',50,1,90,80,90,'   "B-"'),
    ('George','    "Boy"','        "345-67-3901"',40,1,11,-1,4,'   "B"'),
    ('Heffalump',' "Harvey"','     "632-79-9439"',30,1,20,30,40,'   "C"');
