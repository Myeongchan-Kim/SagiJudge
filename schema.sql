drop table if exists rates;
drop table if exists page_tag_rels;
drop table if exists tags;
drop table if exists pages;
drop table if exists doctors;
drop table if exists users;

CREATE TABLE users(
    _id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    opt INT DEFAULT 1 NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE doctors(
    user_id INT,
    license VARCHAR(128) NOT NULL,
    name VARCHAR(255) CHARACTER SET UTF8MB4 NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(_id),
    UNIQUE (license)
);

CREATE TABLE pages(
    _id INT PRIMARY KEY AUTO_INCREMENT,
    url VARCHAR(180) NOT NULL,
    title VARCHAR(255) CHARACTER SET UTF8MB4,
    content TEXT CHARACTER SET UTF8MB4,
    UNIQUE (url)
);

CREATE TABLE tags(
    _id INT PRIMARY KEY AUTO_INCREMENT,
    page_id INT,
    tag VARCHAR(128) CHARACTER SET UTF8MB4,
    FOREIGN KEY (page_id) REFERENCES pages(_id)
);

CREATE TABLE rates(
    user_id INT,
    page_id INT,
    rate INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    content TEXT CHARACTER SET UTF8MB4,
    PRIMARY KEY (user_id, page_id),
    FOREIGN KEY (user_id) REFERENCES users(_id),
    FOREIGN KEY (page_id) REFERENCES pages(_id)
);

