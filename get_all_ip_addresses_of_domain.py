#!/usr/bin/python3
# Program to reverse lookup all possible IPv4 addresses for given domain names using nslookup and gethostbyname API.
# Inputs domains should be specified in 'input_domains.txt' file
# Output will be generated in 'output_list.txt'


import os
import re
import socket


class IPAddressNSLookup:
    def __init__(self):
        self.input_file_name = 'input_domains.txt'
        self.output_file_name = 'output_list.txt'
        self.domain_name_pattern = "(?:https?://)?(?:www\.)?(.+)"
        self.ip_regex_pattern = "Name:\s+[\w\.]+\nAddress:\s+(\d{1,3}\.\d{1,3}.\d{1,3}.\d{1,3})"

        self.values_list = []
        self.output_file = open(self.output_file_name, 'w')
        self.existing_ip_addresses = None

    def write_to_output_file(self, domain_name, ip_address):
        self.output_file.write(domain_name.strip() + ',' + ip_address.strip() + "\n")

    def extract_domain_name_from_url(self, input_line):
        return re.findall(self.domain_name_pattern, input_line)[0]

    @staticmethod
    def get_nslookup_results(domain_name):
        return os.popen('nslookup %s' % domain_name.strip()).read()

    def extract_ip_address_from_nslookup_result(self, nslookup_results):
        return re.findall(self.ip_regex_pattern, nslookup_results)

    def process_result(self, ip_address_list, domain_name):
        for each_ip in ip_address_list:
            self.write_to_output_file(domain_name, each_ip)

    def get_ip_addresses(self):
        with open(self.input_file_name, 'r') as input_file:
            for each_line in input_file:
                domain_name = self.extract_domain_name_from_url(each_line)

                print("Collecting IP addresses for %s" % domain_name)

                print("Getting NSLookup results...")

                nslookup_results = self.get_nslookup_results(domain_name)

                nslookup_ip_address_list = self.extract_ip_address_from_nslookup_result(nslookup_results)
                
                print("Getting Socket results...")

                try:
                    socket_ip_address_list = socket.gethostbyname_ex(domain_name)[2]
                except socket.gaierror:
                    socket_ip_address_list = []

                final_ip_address_list = list(set(nslookup_ip_address_list) | set(socket_ip_address_list))

                print("Combined IP addresses:")
                print(final_ip_address_list)

                print("Processing results")

                if final_ip_address_list:
                    self.process_result(final_ip_address_list, domain_name)

    def close_connections(self):
        self.output_file.close()


if __name__ == "__main__":
    ip_address_obj = IPAddressNSLookup()
    ip_address_obj.get_ip_addresses()
    ip_address_obj.close_connections()
