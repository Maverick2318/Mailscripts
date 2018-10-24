from argparse import ArgumentParser
import imapfetch
def main():
	'''Main control section.'''
	if args.type == 'imap_fetch':
		imapfetch.imapread()
	elif args.type == 'pop_fetch':
		imapfetch.pop_fetch()
	elif args.type == 'send_mail':
		imapfetch.send_mail()
	pass


if __name__ == '__main__':
	parser = ArgumentParser(description='Just a basic email handler!')
	parser.add_argument('-t', '--type', required=True, type=str, choices=['send_mail', 'imap_fetch', 'pop_fetch'], help='Action to be performed by script.')
	args = parser.parse_args()
	main()
