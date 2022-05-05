DROP TABLE IF EXISTS `archive_task`;
DROP TABLE IF EXISTS `archive_split_type`;
DROP TABLE IF EXISTS `archive_interval_type`;
DROP TABLE IF EXISTS `archive_compression_type`;
DROP TABLE IF EXISTS `archive_item`;
DROP TABLE IF EXISTS `archive_group`;

CREATE TABLE `archive_group` (
	`archive_group_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`archive_group_created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`archive_group_modified` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`archive_group_flags` TINYINT(3) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'Flags: 1=enabled/disabled.',
	`archive_group_name` VARCHAR(64) NOT NULL COMMENT 'I am the name of the archiving group. I am unique.' COLLATE 'utf8_general_ci',
	`archive_group_table` VARCHAR(64) NOT NULL COMMENT 'I am the mysql table the archived data will be stored into.' COLLATE 'utf8_general_ci',
	`archive_group_type` ENUM('I','E') NOT NULL COMMENT 'I am the group archiving type. (E=Event based, I=Intervall based)' COLLATE 'utf8_general_ci',
	`archive_group_interval` INT(10) UNSIGNED NULL DEFAULT NULL COMMENT 'I am the amount of seconds to wait between archive entries.',
	PRIMARY KEY (`archive_group_id`) USING BTREE,
	UNIQUE INDEX `archivegroup_name` (`archive_group_name`) USING BTREE,
	UNIQUE INDEX `archivegroup_table` (`archive_group_table`) USING BTREE
) COLLATE='utf8_general_ci' ENGINE=INNODB;

CREATE TABLE `archive_item` (
	`archive_item_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`archive_item_created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`archive_item_modified` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`archive_item_flags` TINYINT(4) NOT NULL DEFAULT '0',
	`archive_group_id` INT(10) UNSIGNED NOT NULL COMMENT 'I am the archive group that the archive item is mapped to.',
	`opc_item_id` INT(10) UNSIGNED NOT NULL COMMENT 'I am the OPC item which value will be used to archive it based on the group setup.',
	PRIMARY KEY (`archive_item_id`) USING BTREE,
	UNIQUE INDEX `archive_group_archive_item_unique` (`archive_group_id`, `opc_item_id`) USING BTREE,
	INDEX `archive_item_to_opc_item` (`opc_item_id`) USING BTREE,
	CONSTRAINT `archive_item_to_archive_group` FOREIGN KEY (`archive_group_id`) REFERENCES `archive_group` (`archive_group_id`) ON UPDATE NO ACTION ON DELETE NO ACTION,
	CONSTRAINT `archive_item_to_opc_item` FOREIGN KEY (`opc_item_id`) REFERENCES `opc_item` (`opc_item_id`) ON UPDATE NO ACTION ON DELETE NO ACTION
) COLLATE='utf8_general_ci' ENGINE=INNODB;

CREATE TABLE `archive_compression_type` (
	`archive_compression_type_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`archive_compression_type_created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`archive_compression_type_modified` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`archive_compression_type_flags` TINYINT(5) UNSIGNED ZEROFILL NOT NULL,
	`archive_compression_type_name` VARCHAR(32) NOT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`archive_compression_type_id`) USING BTREE,
	UNIQUE INDEX `Index 2` (`archive_compression_type_name`) USING BTREE
) COLLATE='utf8_general_ci' ENGINE=INNODB;

CREATE TABLE `archive_interval_type` (
	`archive_interval_type_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`archive_interval_type_created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`archive_interval_type_modified` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`archive_interval_type_flags` TINYINT(5) UNSIGNED ZEROFILL NOT NULL,
	`archive_interval_type_name` VARCHAR(32) NOT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`archive_interval_type_id`) USING BTREE,
	UNIQUE INDEX `Index 2` (`archive_interval_type_name`) USING BTREE
) COLLATE='utf8_general_ci' ENGINE=INNODB;

CREATE TABLE `archive_split_type` (
	`archive_split_type_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`archive_split_type_created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`archive_split_type_modified` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`archive_split_type_flags` TINYINT(5) UNSIGNED ZEROFILL NOT NULL,
	`archive_split_type_name` VARCHAR(32) NOT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`archive_split_type_id`) USING BTREE,
	UNIQUE INDEX `Index 2` (`archive_split_type_name`) USING BTREE
) COLLATE='utf8_general_ci' ENGINE=INNODB;

CREATE TABLE `archive_task` (
	`archive_task_id` INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
	`archive_task_created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`archive_task_modified` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`archive_task_flags` TINYINT(3) UNSIGNED NOT NULL DEFAULT '0',
	`archive_interval_type_id` INT(10) UNSIGNED NOT NULL,
	`archive_compression_type_id` INT(10) UNSIGNED NOT NULL,
	`archive_split_type_id` INT(10) UNSIGNED NULL DEFAULT NULL,
	`archive_group_id` INT(10) UNSIGNED NOT NULL,
	`archive_task_interval` INT(10) UNSIGNED NOT NULL,
	`archive_task_name` VARCHAR(64) NOT NULL COLLATE 'utf8_general_ci',
	PRIMARY KEY (`archive_task_id`) USING BTREE,
	UNIQUE INDEX `Index 2` (`archive_task_name`) USING BTREE,
	UNIQUE INDEX `CompressionTypeAndArchiveGroupUnique` (`archive_group_id`, `archive_interval_type_id`, `archive_task_interval`, `archive_compression_type_id`, `archive_split_type_id`) USING BTREE,
	INDEX `archive_interval_type_id` (`archive_interval_type_id`) USING BTREE,
	INDEX `archive_compression_type_id` (`archive_compression_type_id`) USING BTREE,
	INDEX `archive_split_type_id` (`archive_split_type_id`) USING BTREE,
	CONSTRAINT `archive_group_id` FOREIGN KEY (`archive_group_id`) REFERENCES `archive_group` (`archive_group_id`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `archive_compression_type_id` FOREIGN KEY (`archive_compression_type_id`) REFERENCES `archive_compression_type` (`archive_compression_type_id`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `archive_interval_type_id` FOREIGN KEY (`archive_interval_type_id`) REFERENCES `archive_interval_type` (`archive_interval_type_id`) ON UPDATE RESTRICT ON DELETE RESTRICT,
	CONSTRAINT `archive_split_type_id` FOREIGN KEY (`archive_split_type_id`) REFERENCES `archive_split_type` (`archive_split_type_id`) ON UPDATE RESTRICT ON DELETE RESTRICT
) COLLATE='utf8_general_ci' ENGINE=INNODB;


DROP PROCEDURE `prepareColumn`;
DELIMITER $$;
CREATE PROCEDURE `prepareColumn`(`pDatabase` VARCHAR(32), `pTable` VARCHAR(32), `pColumn` VARCHAR(32), `pType` VARCHAR(32))
BEGIN

	SET @createStatement = CONCAT('
	CREATE TABLE IF NOT EXISTS `', `pTable` , '` (
	  `', `pTable`, '_created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
	) ENGINE=INNODB DEFAULT CHARSET=utf8mb3;');

	PREPARE createStatement FROM @createStatement;
	EXECUTE createStatement;
	DEALLOCATE PREPARE createStatement;


	SET @preparedStatement = (SELECT IF(
	  (
	    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
	    WHERE
	      (TABLE_NAME = `pTable`)
	      AND (table_schema = `pDatabase`)
	      AND (COLUMN_NAME = `pColumn`)
	  ) > 0,
	  "SELECT 1",
	  CONCAT('ALTER TABLE ', `pTable`, ' ADD `', `pColumn`, '` ', `pType`)
	));
	PREPARE alterIfNotExists FROM @preparedStatement;
	EXECUTE alterIfNotExists;
	DEALLOCATE PREPARE alterIfNotExists;

END $$;

DELIMITER ;

