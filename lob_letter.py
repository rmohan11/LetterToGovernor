import os, json
from apiclient.discovery import build
import requests, lob


# Sender and Receiver Attributes
ADDR_ATTR = ['name', 'address_line1', 'address_line2', 'address_city', 'address_state', 'address_country',
             'address_zip', 'message']

CIVIC_ATTR = ["name", "line1", "line2", "city", "zip", "country", "state"]

# Error Codes
NO_ERR = 0
TOADDR_ERR = 1

# Configuration File
CONFIG = "config.txt"


def get_sender_address_from_file(filename="MyFile.txt"):
    """
    Description: Returns the sender address

    Input: Input File name

    Output: Dictionary of from address
    """
    try:
        with open(filename, 'r') as f:

            # The address attributes in the text file should conform to
            # the expected format
            from_address = json.load(f)

            for key, value in from_address.items():
                try:
                    # Address line 2 is the only attribute that can be empty.
                    # Returns None if other values are empty.
                    if from_address[key] == "" and key != 'address_line2':
                        print("Required Value Missing: ", key)
                        return None
                except KeyError as e:
                    print(e)
                    return None

            from_address['string'] = ", ".join([from_address[key] for key in ADDR_ATTR[1:-1]])

            return from_address
    except Exception as e:
        print(e)
        return None


def get_to_address_from_civic(string_address, config, role="headOfGovernment", official="Governor" ):
    """
    Description: Returns the recipient address

    Input: From address read from the input file

    Output: Dictionary of to address details
    """
    try:
        service = build(config['civic_service'], config['civic_ver'], developerKey=config['civic_api_key'])

        required_role = service.representatives() \
            .representativeInfoByAddress(address=string_address,
                                         includeOffices=True,
                                         roles=role).execute()

        for office in required_role['offices']:
            # Pick the required official by name and then use the index
            # to retrieve the official's information
            if office['name'] == official:
                index = office['officialIndices'].pop()
                address = required_role['officials'][index]['address'].pop()
                address['name'] = required_role['officials'][index]['name']
                address['country'] = 'US'
                to_address = {}
                for attr in CIVIC_ATTR:
                    try:
                        to_address[attr] = address[attr]
                    except KeyError:
                        # Address line 2 is the only attribute that can be empty.
                        if attr == 'line2':
                            to_address[attr] = ""
                        else:
                            print("Required Value Missing: ", attr)
                            return TOADDR_ERR, {}

                return NO_ERR, to_address

    except Exception as e:
        print(e)
        return TOADDR_ERR, {}


def retrieve_html_tmpl(config):
    """
    Description: Returns html template of the letter

    Input: The Configuration Json

    Output: The html template ID
    """
    try:
        headers = config['headers']
        with open(config['html_file'], 'r') as f:
            html_text = f.read()
            payload = {'html': html_text}
            response = requests.post(config['lob_url'] + config['template_suffix'], headers=headers, data=payload)
            return response.json()['id']
    except Exception as e:
        print(e)
        return None


def create_letter(from_address, to_address, tmpl_Id, config):
    """
    Description: Generates the url for the letter

    Input: The sender & recipient address along with the letter template

    Output: URL of the letter generated.
    """
    try:
        lob.api_key = config['lob_key']
        response = lob.Letter.create(
            description='A letter to the Governor',
            to_address={
                'name': to_address['name'],
                'address_line1': to_address['line1'],
                'address_line2': to_address['line2'],
                'address_city': to_address['city'],
                'address_state': to_address['state'],
                'address_zip': to_address['zip'],
                'address_country': to_address['country']
            },
            from_address={
                'name': from_address['name'],
                'address_line1': from_address['address_line1'],
                'address_line2': from_address['address_line2'],
                'address_city': from_address['address_city'],
                'address_state': from_address['address_state'],
                'address_zip': from_address['address_zip'],
                'address_country': from_address['address_country']
            },
            file=tmpl_Id,
            merge_variables={
                'message': from_address['message']
            },
            color=True
        )
        return response["thumbnails"]
    except Exception as e:
        print(e)
        return None


def main():

    config = json.load(open(CONFIG, "r"))

    filename = input("Enter the file name(default:MyFile.txt): ")

    if len(str(filename)) is 0:
        filename = 'MyFile.txt'

    fullname = os.path.abspath(filename)

    print("Reading the from address and message from the input file")
    from_address = get_sender_address_from_file(fullname)

    if from_address is None:
        print("Unable to read sender's address from the file")
        exit(1)

    print("Retrieving Governor's address from the Civic API")
    result, to_address = get_to_address_from_civic(from_address['string'], config)
    if result is not NO_ERR:
        print("Error: %d in parsing address" % result)
        exit(1)

    print("Creating a HTML TEMPLATE")
    tmpl_Id = retrieve_html_tmpl(config)

    if tmpl_Id is None:
        print("Template couldn't be created ")
        exit(1)

    print("Creating the Letter")
    urldict = create_letter(from_address, to_address, tmpl_Id, config)

    if urldict is None:
        print("Letter was not created")
        exit(1)

    print("Url for Letter:", urldict.pop()["large"])


if __name__ == "__main__":
    main()
