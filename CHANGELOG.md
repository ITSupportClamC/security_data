# Changelog

## v1.0.0

### Changed

- Initial Release
- Include security_base, futures and fixed_deposit
- Notes:
  - In Fixed Deposit `add_fixed_deposit_info`, calling `add_counter_party` has not been implemented and will be included when OTC Counter Party is included.
  - When adding Security Basic, Futures and Fixed Deposit, all fields are required and non-empty
  - All API will close the sqlalchemy session after each call automatically to avoid db connection leak. So no need to explicitly call a function to close DB connection
  - Database creation SQL script added to folder `sql`
  - Database connection setting can be modified at the file `database_config.ini`

## v1.1.0

### Changed

- Include FX Forward, OTC Counter Party
- Notes:
  - When calling `add_fixed_deposit_info` and `add_fx_forward_info`, the program will call `add_counter_party` now.
  - When adding FX Forward, all fields are required and non-empty
  - When adding OTC Counter Party, the fields `geneva_party_name` and `bloomberg_ticker` are optional fields
  - Update SQL add to the `create.sql` in the folder `sql`

## v1.2.0

### Changed

- Include Security Attribute
- Notes:
  - In the functions `add_security_attribute` and `update_security_attribute`, only `security_id_type` and `security_id` are required fields
  - Update SQL add to the `create.sql` in the folder `sql`
