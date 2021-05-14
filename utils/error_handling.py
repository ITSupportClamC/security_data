# coding=utf-8
# 
class NoDataClearingInProuctionModeError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class DataStoreNotYetInitializeError(Exception):
	def __init__(self, msg):
		super().__init__(msg)

class SecurityBaseAlreadyExistError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class SecurityBaseNotExistError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class FuturesAlreadyExistError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class FuturesNotExistError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class FixedDepositAlreadyExistError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class FixedDepositNotExistError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class FxForwardAlreadyExistError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class FxForwardNotExistError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class OtcCounterPartyAlreadyExistError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class OtcCounterPartyNotExistError(Exception):
    def __init__(self, msg):
        super().__init__(msg)