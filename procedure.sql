
DROP PROCEDURE IF EXISTS `getIdByUrl`;
--
CREATE PROCEDURE `getIdByUrl`(IN url_str VARCHAR(180), content_text TEXT)
BEGIN
    INSERT INTO pages (url, content)
    SELECT * from (SELECT url_str, content_text) as tmp
    WHERE NOT EXISTS(
        SELECT _id FROM pages as p WHERE p.url = tmp.url_str
    );
    SELECT _id FROM pages where url = url_str;
END
--


DROP PROCEDURE IF EXISTS `getBadOfPage`;
--
CREATE PROCEDURE `getBadOfPage`(IN url VARCHAR(180))
BEGIN
    SELECT count(*) AS bad
        FROM rates AS r JOIN pages AS p
        ON r.page_id = p._id
        WHERE p.url = url
        AND r.rate = 0;
END
--

DROP PROCEDURE IF EXISTS `getRateByPage`;
--
CREATE PROCEDURE `getRateByPage`(IN url VARCHAR(180))
BEGIN
    SELECT
    (SELECT count(*) AS bad
        FROM rates AS r JOIN pages AS p
        ON r.page_id = p._id
        WHERE p.url = url
        AND r.rate = 0) as bad,
    (SELECT count(*) AS good
        FROM rates AS r
        JOIN pages AS p
        ON r.page_id = p._id
        WHERE p.url = url
        AND r.rate = 1) AS good;
END
--

DROP PROCEDURE IF EXISTS `getRateOfPageByType`;
--
CREATE PROCEDURE `getRateOfPageByType`(IN url VARCHAR(180))
BEGIN
    SELECT
    (SELECT p.page_id, u.opt, count(*) AS bad
        FROM rates AS r
        JOIN pages AS p
        ON r.page_id = p._id
        JOIN users as u
        ON r.user_id = u._id
        WHERE p.url = url
        AND r.rate = 0
    ) as bad,
    (SELECT p.page_id, u.opt, count(*) AS good
        FROM rates AS r
        JOIN pages AS p
        ON r.page_id = p._id
        JOIN users as u
        ON r.user_id = u._id
        WHERE p.url = url
        AND r.rate = 1
    ) AS good;
END
--
