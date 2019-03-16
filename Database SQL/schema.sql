/* phase 2 team 009 postgresql schema */
CREATE SCHEMA public009;

/* STRONG ENTITIES */
CREATE TABLE regularuser (
    username VARCHAR(50) PRIMARY KEY NOT NULL,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL
);

CREATE TABLE item (
    itemid BIGSERIAL PRIMARY KEY NOT NULL,
    description VARCHAR(500) NOT NULL,
    name VARCHAR(50) NOT NULL,
    condition INTEGER NOT NULL,
    winner VARCHAR(50) DEFAULT NULL,
    endingtime TIMESTAMP WITH TIME ZONE NOT NULL,
    getitnowprice NUMERIC(30, 2),
    returnable BOOLEAN NOT NULL,
    startingprice NUMERIC(30, 2) NOT NULL,
    minimumsaleprice NUMERIC(30, 2) NOT NULL 
);

CREATE TABLE category (
    name VARCHAR(50) PRIMARY KEY NOT NULL
);

/* WEAK ENTITIES */
CREATE TABLE bid (
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    price NUMERIC(30, 2) NOT NULL
);

CREATE TABLE RATE (
    comments VARCHAR(500),
    time TIMESTAMP WITH TIME ZONE NOT NULL,
    stars INTEGER NOT NULL
);

/* SUPER/SUBTYPES */
CREATE TABLE adminuser (
    position VARCHAR(50)
);

/*ADD FOREIGN KEYS */
ALTER TABLE item 
      ADD COLUMN username VARCHAR(50), 
      ADD CONSTRAINT fk_item_username_regularuser_username 
      FOREIGN KEY (username) 
      REFERENCES regularuser (username);

ALTER TABLE item 
      ADD COLUMN categoryname VARCHAR(50), 
      ADD CONSTRAINT fk_item_categoryname_category_name
      FOREIGN KEY (categoryname) 
      REFERENCES category (name);

ALTER TABLE item  
      ADD CONSTRAINT fk_item_winner_regularuser_username 
      FOREIGN KEY (winner) 
      REFERENCES regularuser (username);

ALTER TABLE rate
      ADD COLUMN username VARCHAR(50), 
      ADD CONSTRAINT fk_rate_username_regularuser_username 
      FOREIGN KEY (username) 
      REFERENCES regularuser (username);

ALTER TABLE rate
      ADD COLUMN itemid BIGSERIAL, 
      ADD CONSTRAINT fk_rate_itemid_item_itemid
      FOREIGN KEY (itemid) 
      REFERENCES item (itemid);

ALTER TABLE bid
      ADD COLUMN username VARCHAR(50), 
      ADD CONSTRAINT fk_bid_username_regularuser_username 
      FOREIGN KEY (username) 
      REFERENCES regularuser (username);

ALTER TABLE bid
      ADD COLUMN itemid BIGINT,
      ADD CONSTRAINT fk_bid_itemid_item_itemid
      FOREIGN KEY (itemid) 
      REFERENCES item (itemid);

ALTER TABLE adminuser
      ADD COLUMN username VARCHAR(50), 
      ADD CONSTRAINT fk_adminuser_username_regularuser_username 
      FOREIGN KEY (username) 
      REFERENCES regularuser (username);

/* ADD COMPOSITE PRIMARY KEYS*/
ALTER TABLE bid
  ADD PRIMARY KEY (itemid, username, time);

ALTER TABLE rate
  ADD PRIMARY KEY (itemid, username);

/* ADD PRIMARY KEY FOR SUBTYPE */
ALTER TABLE adminuser
  ADD PRIMARY KEY (username);