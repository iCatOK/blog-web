-- добавление записей дневника
CREATE TABLE diary_records (
   id integer PRIMARY KEY,
   user_id integer NOT NULL,
   record_text text NOT NULL,
   record_date timestamp not null default current_timestamp
);