-- drop table security_base;
-- drop table futures;
-- drop table fixed_deposits;

CREATE TABLE `security_base` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `geneva_id` varchar(100) NOT NULL,
  `geneva_asset_type` varchar(100) NOT NULL,
  `geneva_investment_type` varchar(100) NOT NULL,
  `ticker` varchar(50) NOT NULL,
  `isin` varchar(50) NOT NULL,
  `bloomberg_id` varchar(50) NOT NULL,
  `sedol` varchar(50) NOT NULL,
  `currency` varchar(5) NOT NULL,
  `is_private` varchar(5) NOT NULL,
  `description` varchar(200) NOT NULL,
  `exchange_name` varchar(100) NOT NULL,
  `timestamp` datetime NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `created_by` int(11) unsigned DEFAULT NULL,
  `updated_by` int(11) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `udx_security_base__geneva_id` (`geneva_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE `futures` (
	`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
	`ticker` varchar(50) NOT NULL,
	`underlying_id` varchar(100) NOT NULL,
	`contract_size` decimal(18,6) NOT NULL,
	`value_of_1pt` decimal(18,6) NOT NULL,
	`timestamp` datetime NOT NULL,
	`created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`created_by` int(11) unsigned DEFAULT NULL,
	`updated_by` int(11) unsigned DEFAULT NULL,
	PRIMARY KEY (`id`),
	UNIQUE KEY `udx_futures__ticker` (`ticker`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `fixed_deposits` (
	`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
	`geneva_id` varchar(100) NOT NULL,
	`factset_id` varchar(100) NOT NULL,
	`geneva_counter_party` varchar(100) NOT NULL,
	`starting_date` datetime NOT NULL,
	`maturity_date` datetime NOT NULL,
	`interest_rate` decimal(18,6) NOT NULL,
	`created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`created_by` int(11) unsigned DEFAULT NULL,
	`updated_by` int(11) unsigned DEFAULT NULL,
	PRIMARY KEY (`id`),
	UNIQUE KEY `udx_fixed_deposits__geneva_id` (`geneva_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
