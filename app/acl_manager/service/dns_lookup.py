import dns.resolver


class DNSLookupService:
    _NAMESERVERS = ['1.1.1.1', '8.8.8.8', '8.8.4.4']

    def __init__(self):
        dns_resolver = dns.resolver.Resolver()
        dns_resolver.nameservers = self._NAMESERVERS
        self._dns_resolver = dns_resolver

    def look_up(self, domain: str):
        dns_info = self._dns_resolver.resolve(domain)
        for ip, _ in dns_info.rrset.items.items():
            return str(ip)
        return None
