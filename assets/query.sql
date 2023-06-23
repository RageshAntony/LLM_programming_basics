CREATE TABLE `episode_info` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'Unique Id of the Episode ',
  `series` int DEFAULT NULL COMMENT 'Series Id of the episode',
  `season` int DEFAULT NULL COMMENT 'Season id of the episode ',
  `episode_index` int DEFAULT NULL COMMENT 'Episode number of the episode ',
  `title` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci COMMENT 'Title of the episode ',
  `description` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci COMMENT 'Description  of the episode ',
  `air_date` date DEFAULT NULL COMMENT 'Air date  of the episode ',
  `duration_mins` int DEFAULT NULL COMMENT 'Run time  of the episode ',
  `poster_url` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci COMMENT 'Image URL for the banner  of the episode ',
  `video_url` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci COMMENT 'Trailer Video URL  of the episode ',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `series_info_idx` (`series`),
  KEY `seasons_info_idx` (`season`),
  CONSTRAINT `seasons_info` FOREIGN KEY (`season`) REFERENCES `seasons` (`id`),
  CONSTRAINT `series_info` FOREIGN KEY (`series`) REFERENCES `series_info` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=155 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

CREATE TABLE `maturity` (
  `id` int NOT NULL AUTO_INCREMENT,
  `rating_value` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Rating value of Maturity rating ',
  `description` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Description of Maturity rating ',
  `age_start` int DEFAULT NULL COMMENT 'Starting age of Maturity rating ',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

CREATE TABLE `seasons` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT 'Id of the seasons',
  `season_index` int DEFAULT NULL COMMENT 'Season number',
  `info` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci COMMENT 'Info about the season',
  `release` date DEFAULT NULL COMMENT 'Release date of a season',
  `episode_count` int DEFAULT NULL COMMENT 'Number of episodes in a season',
  `series` int DEFAULT NULL COMMENT 'Series id which the season belongs to, refers ‘series_info’  table',
  `title` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci COMMENT 'Title of the season',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `series_rel_idx` (`series`),
  CONSTRAINT `series_rel` FOREIGN KEY (`series`) REFERENCES `series_info` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

CREATE TABLE `series_info` (
  `id` int NOT NULL AUTO_INCREMENT,
  `plot` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci COMMENT 'The plot line of the Series',
  `maturity` int DEFAULT NULL COMMENT 'The maturity rating of the Series, refers ‘maturity’ table',
  `release` date DEFAULT NULL COMMENT 'The release date of the Series',
  `seasons` int DEFAULT NULL COMMENT 'The number of seasons in the Series',
  `trailer_url` varchar(300) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'The trailer url of the Series',
  `studios` int DEFAULT NULL COMMENT 'The studio that produced the Series, refers ‘studios’ table',
  `title` mediumtext CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci COMMENT 'The title of the Series',
  `poster_url` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci COMMENT 'The poster url of the Series',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`),
  KEY `maturity_idx` (`maturity`),
  KEY `studios_idx` (`studios`),
  CONSTRAINT `maturity` FOREIGN KEY (`maturity`) REFERENCES `maturity` (`id`),
  CONSTRAINT `studios` FOREIGN KEY (`studios`) REFERENCES `studios` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;

CREATE TABLE `studios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci DEFAULT NULL COMMENT 'Name of the studio',
  `description` longtext CHARACTER SET utf8mb3 COLLATE utf8mb3_unicode_ci COMMENT 'Description of the studio',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_unicode_ci;
