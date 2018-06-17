BEGIN TRANSACTION;
CREATE TABLE "users" (
	`id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`username`	TEXT,
	`password`	TEXT,
	`role`	INTEGER DEFAULT 0
);
CREATE TABLE "sessions" (
	`user_id`	INTEGER,
	`removal_time`	INTEGER,
	`session`	TEXT
);
COMMIT;
