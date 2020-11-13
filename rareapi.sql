SELECT * FROM rareapi_postINSERT INTO rareapi_postreaction (id, post_id, reaction_id, user_id)
VALUES (
    id:integer,
    post_id:integer,
    reaction_id:integer,
    user_id:integer
  );
DELETE  FROM rareapi_postreaction