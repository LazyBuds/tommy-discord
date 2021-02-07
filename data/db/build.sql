CREATE TABLE IF NOT EXISTS guilds (
	GuildID integer PRIMARY KEY,
	Prefix text DEFAULT "+",
	Wcmessage text DEFAULT NULL,
	Wcchannel BigInt,
	Leavechannel BigInt,
	Leavemessage text DEFAULT NULL,
	Logchannel BigInt
);


CREATE TABLE IF NOT EXISTS mutes(
	UserID integer PRIMARY KEY,
	RoleIDs text,
	EndTime text
);

CREATE TABLE IF NOT EXISTS afk(
	UserID BigInt not NULL,
	Guildid BigInt not NULL,
	afktype text DEFAULT NULL,
	afkreason text DEFAULT NULL,
	PRIMARY KEY (UserID)
);

CREATE TABLE IF NOT EXISTS command(
	channelid BigInt not NULL PRIMARY KEY,
	commandname text,
	commanduse text DEFAULT "True"
);

CREATE TABLE IF NOT EXISTS shoob(
	guildid BigInt not NULL,
	t1 BigInt DEFAULT NULL,
	t2 BigInt DEFAULT NULL,
	t3 BigInt DEFAULT NULL,
	t4 BigInt DEFAULT NULL,
	t5 BigInt DEFAULT NULL,
	t6 BigInt DEFAULT NULL,
	PRIMARY KEY (guildid)

);





CREATE TABLE IF NOT EXISTS permission (
	guildId integer PRIMARY KEY,
	Welcomecard text DEFAULT NULL,
	Customwelcome text DEFAULT NULL,
	Muterole BigInt DEFAULT NULL,
	Custombanner text DEFAULT NULL,
	Bannersetting text DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS captcha (
	guid BigInt PRIMARY KEY,
	chid BigInt,
	roleid BigInt
);

CREATE TABLE IF NOT EXISTS boost (
	gu_id BigInt PRIMARY KEY,
	ch_id BigInt DEFAULT NULL,
	embed_ch BigInt DEFAULT NULL,
	setting text DEFAULT 'off',
	boost_msg text
);

CREATE TABLE IF NOT EXISTS global_counters(
	command text PRIMARY KEY,
	amount Numeric DEFAULT 0

);

CREATE TABLE IF NOT EXISTS guild_counters(
	guilds BigInt PRIMARY KEY,
	amount Numeric DEFAULT 0
);

-- CREATE TABLE IF NOT EXISTS user_counters(
-- 	userid BigInt NOT NULL,
-- 	guild_id BigInt NOT NULL,
-- 	amount Numeric,
-- 	PRIMARY KEY (userid, guild_id)
	
-- );


CREATE TABLE IF NOT EXISTS todos(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	userid bigint NOT NULL,
	content TEXT NOT NULL

);
-- CREATE TABLE IF NOT EXISTS reminders(
--     id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
-- 	guild_id bigint, 
-- 	users bigint, 
-- 	channel_id bigint, 
-- 	type_ text, 
-- 	message_content text, 
-- 	time_ NUMERIC
-- );


CREATE TABLE IF NOT EXISTS monitor(
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	mentor bigint NOT NULL,
	target bigint NOT NULL,
	guild bigint NOT NULL,
	nick text, 
	before_nick text
);

CREATE TABLE IF NOT EXISTS horoscope(
  user_id BigInt,
  sunsign TEXT,
  PRIMARY KEY(user_id)
);