# Changelog

## v1.0.0

### Changed

- Initial Release
- Include security_base, futures and fixed_deposit
- Notes:
  - In Fixed Deposit "add_fixed_deposit_info", calling "add_counter_party" has not been implemented and will be included when OTC Counter Party is included.
  - When adding Security Basic, Futures and Fixed Deposit, all fields are required and non-empty
  - All API will close the sqlalchemy session after each call automatically to avoid db connection leak. So no need to explicitly call a function to close DB connection
  - Database creation SQL script added to folder `sql`
  - Database connection setting can be modified at the file database_config.ini
