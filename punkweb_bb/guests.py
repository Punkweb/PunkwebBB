from expiringdict import ExpiringDict


class GuestList:
    def __init__(self):
        self.__guests = ExpiringDict(max_len=2048, max_age_seconds=60 * 5)

    def length(self):
        return len(self.__guests)

    def add(self, ip):
        if not self.__guests.get(ip, None):
            self.__guests[ip] = True

    def clear_expired(self):
        for key in list(self.__guests.keys()):
            _ = self.__guests.get(key, None)


guest_list = GuestList()
