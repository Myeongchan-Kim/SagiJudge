drop table if exists rates;
drop table if exists page_tag_rels;
drop table if exists tags;
drop table if exists pages;
drop table if exists doctors;
drop table if exists users;

CREATE TABLE users(
    _id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE doctors(
    user_id INT,
    license VARCHAR(255) NOT NULL,
    name VARCHAR(255) CHARACTER SET UTF8MB4 NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(_id),
    UNIQUE (license)
);

CREATE TABLE pages(
    _id INT PRIMARY KEY AUTO_INCREMENT,
    url VARCHAR(255) NOT NULL,
    content TEXT CHARACTER SET UTF8MB4,
    UNIQUE (url)
);

CREATE TABLE tags(
    _id INT PRIMARY KEY AUTO_INCREMENT,
    tag VARCHAR(128) CHARACTER SET UTF8MB4,
    UNIQUE KEY `idx_tag` (`tag`) USING HASH
);

CREATE TABLE page_tag_rels(
    page_id INT,
    tag_id INT,
    PRIMARY KEY (page_id, tag_id),
    FOREIGN KEY (page_id) REFERENCES pages(_id),
    FOREIGN KEY (tag_id) REFERENCES tags(_id)
);

CREATE TABLE rates(
    user_id INT,
    page_id INT,
    rate INT NOT NULL,
    content TEXT CHARACTER SET UTF8MB4,
    PRIMARY KEY (user_id, page_id),
    FOREIGN KEY (user_id) REFERENCES users(_id),
    FOREIGN KEY (page_id) REFERENCES pages(_id)
);
