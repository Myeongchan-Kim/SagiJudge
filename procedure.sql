
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

DROP PROCEDURE IF EXISTS `getRateOfPageByUrl`;
--
CREATE PROCEDURE `getRateOfPageByUrl`(IN url VARCHAR(180))
BEGIN
    SELECT a.page_id as page_id, a.opt as opt, a.bad as bad, b.good as good
    FROM
    (SELECT p._id as page_id, u.opt as opt, count(r.rate) AS bad
        FROM rates AS r
        JOIN pages AS p
        ON r.page_id = p._id
        JOIN users as u
        ON r.user_id = u._id
        WHERE p.url = url
        AND r.rate = 0
        GROUP BY u.opt
    ) as a
    JOIN
    (SELECT p._id as page_id, u.opt as opt, count(r.rate) AS good
        FROM rates AS r
        JOIN pages AS p
        ON r.page_id = p._id
        JOIN users as u
        ON r.user_id = u._id
        WHERE p.url = url
        AND r.rate = 1
        GROUP BY u.opt
    ) AS b
    ON a.page_id = b.page_id AND a.opt = b.opt;
END
--

DROP PROCEDURE IF EXISTS `getRateOfPage`;
--
CREATE PROCEDURE `getRateOfPage`(IN id INT)
BEGIN
    SELECT a.page_id as page_id, a.opt as opt, a.bad as bad, b.good as good
    FROM
    (SELECT r.page_id as page_id, u.opt as opt, count(r.rate) AS bad
        FROM rates AS r
        JOIN users as u
        ON r.user_id = u._id
        WHERE r.rate = 0
        AND r.page_id = id
        GROUP BY u.opt
    ) as a
    JOIN
    (SELECT r.page_id as page_id, u.opt as opt, count(r.rate) AS good
        FROM rates AS r
        JOIN users as u
        ON r.user_id = u._id
        WHERE r.rate = 1
        AND r.page_id = id
        GROUP BY u.opt
    ) AS b
    ON a.page_id = b.page_id AND a.opt = b.opt;
END
--
DROP PROCEDURE IF EXISTS `getComputerRate`;
--
CREATE PROCEDURE `getComputerRate`(IN id INT)
BEGIN
    SELECT p._id as page_id, r.rate as score
    FROM rates as r
    JOIN pages as p
    ON p._id = r.page_id
    WHERE r.user_id = -1
    and p._id = id;
END
--

DROP PROCEDURE IF EXISTS `getDangerousPages`;
--
CREATE PROCEDURE `getDangerousPages`()
BEGIN
    SELECT a.page_id, (a.ratio - b.ratio) as gap
    FROM
    (SELECT t.page_id as page_id, t.ratio as ratio FROM
        (SELECT a.page_id as page_id,
            a.opt as opt,
            (b.good / (a.bad + b.good)) as ratio
            FROM
            (SELECT r.page_id as page_id, u.opt as opt, count(r.rate) AS bad
                FROM rates AS r
                JOIN users as u
                ON r.user_id = u._id
                WHERE r.rate = 0
                GROUP BY r.page_id, u.opt
            ) as a
            JOIN
            (SELECT r.page_id as page_id, u.opt as opt, count(r.rate) AS good
                FROM rates AS r
                JOIN users as u
                ON r.user_id = u._id
                WHERE r.rate = 1
                GROUP BY r.page_id, u.opt
            ) AS b
            ON a.page_id = b.page_id AND a.opt = b.opt) AS t WHERE t.opt = 1) AS a
    JOIN
    (SELECT t.page_id as page_id, t.ratio as ratio
        FROM (SELECT a.page_id as page_id,
            a.opt as opt,
            (b.good / (a.bad + b.good)) as ratio
            FROM
            (SELECT r.page_id as page_id, u.opt as opt, count(r.rate) AS bad
                FROM rates AS r
                JOIN users as u
                ON r.user_id = u._id
                WHERE r.rate = 0
                GROUP BY r.page_id, u.opt
            ) as a
            JOIN
            (SELECT r.page_id as page_id, u.opt as opt, count(r.rate) AS good
                FROM rates AS r
                JOIN users as u
                ON r.user_id = u._id
                WHERE r.rate = 1
                GROUP BY r.page_id, u.opt
            ) AS b
            ON a.page_id = b.page_id AND a.opt = b.opt) AS t WHERE t.opt = 2) AS b
    ON a.page_id = b.page_id
    ORDER BY gap;
END
--

DROP PROCEDURE IF EXISTS `getDangerousPages`;
--
CREATE PROCEDURE `getDangerousPages`()
BEGIN
    select *, norm.pid, norm.ratio - doc.ratio as wrongValue 
    from 
       (select page_id as pid, sum(rate) as sum ,count(*) as cnt, sum(rate)/count(*) as ratio 
        from 
          (rates 
          join users 
            on rates.user_id = users._id and users.opt = 1)
       group by page_id) as norm
    join
       (select page_id as pid, sum(rate) as sum, count(*) as cnt, sum(rate)/count(*) as ratio 
        from 
          (rates 
            join users 
            on rates.user_id = users._id and users.opt = 2)
       group by page_id) as doc
    on norm.pid = doc.pid
    ORDER BY wrongValue DESC
    LIMIT 4;
END
--

DROP PROCEDURE IF EXISTS `getWatingPages`;
--
CREATE PROCEDURE `getWatingPages`()
BEGIN
    select page_id, count(user_id) as userCount
    from rates
    group by page_id
    order by userCount DESC
    limit 4;
END
--

DROP PROCEDURE IF EXISTS `getHotPages`;
--
CREATE PROCEDURE `getHotPages`()
BEGIN
    select page_id, count(user_id) as userCount
    from rates
    group by page_id
    order by userCount
    limit 4;
END
--

DROP PROCEDURE IF EXISTS `getNewPages`;
--
CREATE PROCEDURE `getNewPages`()
BEGIN
    SELECT p._id AS page_id, p.content
    FROM pages as p
    LEFT JOIN page_tag_rels as r
    ON p._id = r.page_id
    WHERE r.page_id IS NULL;
END
--

