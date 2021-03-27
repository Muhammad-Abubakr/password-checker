import requests
import hashlib
# import sys
import os

## sending requests to api for data exchange
def request_data_api(querystring):
	url = 'https://api.pwnedpasswords.com/range/' + querystring  ## first five characters of SHA1 encryption for k-anonymity used by api
	res = requests.get(url)
	# if status_Code == 400 $client_error or 500 == server_error ~ req not found on server
	if res.status_code != 200:
		raise RuntimeError(f'server responded with errorcode {res.status_code}')
	return res

def check_api_response(hashes, hash_to_check):
	hashes = (line.split(':') for line in hashes.text.splitlines())

	for h, count in hashes:
		if h == hash_to_check:
			return count
	return 0

def pwned_api_check(password):
	## converting the string to SHA1 encryption for anonymity and as a requirement from api
	sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	head, tail = sha1password[:5], sha1password[5:]
	response = request_data_api(head)
	return check_api_response(response, tail)

## for use with command line

# def main(args):
# 	for password in args:
# 		count = pwned_api_check(password)
# 		if count:
# 			print(f'your {password} was found {count} times ... you should consider changing it!')
# 		else:
# 			print(f'your {password} was NOT found. Carry on!')

# main(sys.argv[1:])

## use with a text file
## recommended (procedure below)

def main():
	for file in os.listdir('./'):
		if file.endswith('.txt'):
			pass_file = open(file)
			pass_list = (password.replace('\n', '') for password in pass_file.readlines())
			for password in pass_list:
				count = pwned_api_check(password)
				if count:
					print(f'your {password} was found {count} times ... you should consider changing it!')
				else:
					print(f'your {password} was NOT found. Carry on!')

		return 'NO FILE FOUND'

main()
			
