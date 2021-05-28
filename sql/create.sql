-- drop table security_base;
-- drop table futures;
-- drop table fixed_deposits;
-- drop table fx_forwards;
-- drop table otc_counter_parties;
-- drop table security_attributes;

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

CREATE TABLE `fx_forwards` (
	`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
	`factset_id` varchar(100) NOT NULL,
	`geneva_fx_forward_name` varchar(100) NOT NULL,
	`geneva_counter_party` varchar(100) NOT NULL,
	`starting_date` datetime NOT NULL,
	`maturity_date` datetime NOT NULL,
	`base_currency` varchar(5) NOT NULL,
	`base_currency_quantity` decimal(18,6) NOT NULL,
	`term_currency`varchar(5) NOT NULL,
	`term_currency_quantity` decimal(18,6) NOT NULL,
	`forward_rate` decimal(18,6) NOT NULL,
	`created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`created_by` int(11) unsigned DEFAULT NULL,
	`updated_by` int(11) unsigned DEFAULT NULL,
	PRIMARY KEY (`id`),
	UNIQUE KEY `udx_fx_forwards__factset_id` (`factset_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `otc_counter_parties` (
	`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
	`geneva_counter_party` varchar(100) NOT NULL,
	`geneva_party_type` varchar(100) NOT NULL,
	`geneva_party_name` varchar(100) default NULL,
	`bloomberg_ticker` varchar(50) default NULL,
	`created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`created_by` int(11) unsigned DEFAULT NULL,
	`updated_by` int(11) unsigned DEFAULT NULL,
	PRIMARY KEY (`id`),
	UNIQUE KEY `udx_otc_counter_parties__geneva_counter_party_geneva_party_type` (`geneva_counter_party`, `geneva_party_type`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `security_attributes` (
	`id` int(11) unsigned NOT NULL AUTO_INCREMENT,
	`security_id_type` varchar(50) NOT NULL,
	`security_id` varchar(100) NOT NULL,
	`gics_sector` varchar(100) DEFAULT NULL,
	`gics_industry_group` varchar(100) DEFAULT NULL,
	`industry_sector` varchar(100) DEFAULT NULL,
	`industry_group` varchar(100) DEFAULT NULL,
	`bics_sector_level_1` varchar(100) DEFAULT NULL,
	`bics_industry_group_level_2` varchar(100) DEFAULT NULL,
	`bics_industry_name_level_3` varchar(100) DEFAULT NULL,
	`bics_sub_industry_name_level_4` varchar(100) DEFAULT NULL,
	`parent_symbol` varchar(100) DEFAULT NULL,
	`parent_symbol_chinese_name` varchar(100) DEFAULT NULL,
	`parent_symbol_industry_group` varchar(100) DEFAULT NULL,
	`cast_parent_company_name` varchar(100) DEFAULT NULL,
	`country_of_risk` varchar(100) DEFAULT NULL,
	`country_of_issuance` varchar(100) DEFAULT NULL,
	`sfc_region` varchar(100) DEFAULT NULL,
	`s_p_issuer_rating` varchar(100) DEFAULT NULL,
	`moody_s_issuer_rating` varchar(100) DEFAULT NULL,
	`fitch_s_issuer_rating` varchar(100) DEFAULT NULL,
	`bond_or_equity_ticker` varchar(100) DEFAULT NULL,
	`s_p_rating` varchar(100) DEFAULT NULL,
	`moody_s_rating` varchar(100) DEFAULT NULL,
	`fitch_rating` varchar(100) DEFAULT NULL,
	`payment_rank` varchar(100) DEFAULT NULL,
	`payment_rank_mbs` varchar(100) DEFAULT NULL,
	`bond_classification` varchar(100) DEFAULT NULL,
	`local_government_lgfv` varchar(100) DEFAULT NULL,
	`first_year_default_probability` decimal(18,9) DEFAULT NULL,
	`contingent_capital` varchar(100) DEFAULT NULL,
	`co_co_bond_trigger` varchar(100) DEFAULT NULL,
	`capit_type_conti_conv_tri_lvl` varchar(100) DEFAULT NULL,
	`tier_1_common_equity_ratio` decimal(18,6) DEFAULT NULL,
	`bail_in_capital_indicator` varchar(100) DEFAULT NULL,
	`tlac_mrel_designation` varchar(100) DEFAULT NULL,
	`classif_on_chi_state_owned_enterp` varchar(100) DEFAULT NULL,
	`private_placement_indicator` varchar(100) DEFAULT NULL,
	`trading_volume_90_days` decimal(18,6) DEFAULT NULL,
	`created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
	`created_by` int(11) unsigned DEFAULT NULL,
	`updated_by` int(11) unsigned DEFAULT NULL,
	PRIMARY KEY (`id`),
	UNIQUE KEY `udx_security_attributes__security_id_type_security_id` (`security_id_type`, `security_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
