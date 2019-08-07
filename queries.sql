SELECT "kyo_song"."id", "kyo_song"."name", "kyo_song"."album_id" FROM "kyo_song" LEFT OUTER JOIN "kyo_word" ON ("kyo_song"."id" = "kyo_word"."song_id") WHERE "kyo_word"."id" IS NULL
-- Time: 1.858 ms

-- to be transformed to
SELECT "kyo_song"."id", "kyo_song"."name", "kyo_song"."album_id" FROM "kyo_song" WHERE  NOT EXISTS (SELECT 1 FROM "kyo_word" WHERE song_id=kyo_song.id);
-- Time: 0.702 ms


-- DASHBOARD SONG

-- top 10 words in the song


-- Top 10 group of two words (lateral)


-- words that only appear in this song (exists/not exists)


-- group of two words appearing more than once

SELECT first_word.value, second_word.value, COUNT(*) FROM kyo_word first_word INNER JOIN LATERAL (SELECT value, position FROM kyo_word next_word WHERE next_word.song_id=first_word.song_id AND next_word.position > first_word.position ORDER BY position ASC LIMIT 1) second_word on true  WHERE song_id=992  GROUP BY 1,2 HAVING COUNT(*) > 1 ORDER BY 3 DESC;



SELECT 1 as id, first_word.value as value, second_word.value as following_word, COUNT(*) as nb_of_occurences
        FROM kyo_word first_word
        INNER JOIN LATERAL (
          SELECT value, position FROM kyo_word next_word
          WHERE next_word.song_id=first_word.song_id
          AND next_word.position > first_word.position
          ORDER BY position ASC LIMIT 1) second_word on true
        WHERE song_id=342  GROUP BY 1,2,3 HAVING COUNT(*) > 2 ORDER BY 4 DESC;


-- max value 8

-- detect chorus



WITH words AS (SELECT first_word.value, first_word.position, array_agg(second_word.value) as next FROM kyo_word first_word INNER JOIN LATERAL (SELECT value, position FROM kyo_word next_word WHERE next_word.song_id=first_word.song_id AND next_word.position > first_word.position ORDER BY position ASC LIMIT 7) second_word on true  WHERE song_id=342 GROUP BY 1,2)
SELECT array_prepend(words.value, words.next), COUNT(*) FROM words GROUP BY 1 ORDER BY 2 DESC;




-- DASHBOARD ALBUM


-- use a grouping sets






-- DASHBOARD ARTISTS

-- number of single words per album

-- in how many songs do the words appear

WITH distinct_song AS (SELECT DISTINCT value, song_id FROM kyo_word WHERE artist_id=6)
SELECT value, COUNT(*) FROM distinct_song GROUP BY value;


-- top 10 words per album


SELECT value, a.name, frequency, rank FROM (

SELECT value,
       album.name,
       count(*) as frequency,
       rank() OVER (PARTITION BY album.id
       ORDER BY COUNT(*)
       DESC
       ) rank
FROM kyo_word INNER JOIN kyo_album album ON album.id = kyo_word.album_id WHERE artist_id = 6  GROUP BY value, album.id ORDER BY album.id) a

WHERE a.rank < 10;



-- with a grouping sets on value, album

WITH distinct_words_song AS (SELECT DISTINCT value, song_id, kyo_album.name as album_name FROM kyo_word INNER JOIN kyo_album ON kyo_album.id=kyo_word.album_id WHERE kyo_album.artist_id = 6 AND value <> 'refrain' ORDER BY song_id)

SELECT value, album_name, count(*) FROM distinct_words_song WHERE album_name IS NOT NULL AND album_name <> '' GROUP BY GROUPING SETS ((value, album_name), (album_name), (value)) HAVING count(*) > 3 ORDER BY album_name, count(*) DESC;

-- number words in total per album, evolution of vocabulary



--


SELECT value, a.name album_name, sum(frequency) FROM (

SELECT value,
       album.name,
       count(*) as frequency,
       rank() OVER (PARTITION BY album.id
       ORDER BY COUNT(*)
       DESC
       ) rank
FROM kyo_word INNER JOIN kyo_album album ON album.id = kyo_word.album_id WHERE artist_id = 6  GROUP BY value, album.id ORDER BY album.id) a

WHERE a.rank < 10
GROUP BY GROUPING SETS (1, 2);


-- top words, grouping sets


WITH top_words AS (SELECT value, a.name as album_name, frequency, ranking FROM (

        SELECT value,
        album.name,
        count(*) as frequency,
        dense_rank() OVER (PARTITION BY album.id
        ORDER BY COUNT(*)
        DESC
        ) ranking
        FROM kyo_word INNER JOIN kyo_album album ON album.id = kyo_word.album_id WHERE kyo_word.artist_id = 9   AND value <> 'refrain' GROUP BY value, album.id ORDER BY album.id) a

        WHERE a.ranking < 9 AND a.frequency > 5)


SELECT value, album_name, SUM(frequency) as total_rep
FROM top_words
GROUP BY GROUPING SETS ((1, 2), (1))
ORDER BY album_name, total_rep DESC;
