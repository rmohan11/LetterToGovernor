1. Create a file with the following json object
{
    "name":"Rakesh Mohan",
    "address_line1":"1701, East 8th Street",
    "address_line2":"",
    "address_city":"Tempe",
    "address_state":"Az",
    "address_country":"US",
    "address_zip":"85281",
    "message": "Hello Governor, This is a sample letter sent using LOB endpoints"
}. The json object contains the address of the sender along with the message that needs to be sent. This file is expected to be in the current working directory.

2. The letter is created for the Governor of the state.

3. The google-api-python-client library is required for using civic APIs. Please run pip install --upgrade google-api-python-client to get this library.

4. The config.txt file has all the configuration settings. This file is expected to be in the current working directory.

5. Steps to run the script.

	Step a) Run the script from command line like shown below
			Rakeshs-MacBook-Air:Lob_Legislator rakesh$ python3.5 lob_letter.py

	Step b) Enter the file name(default:MyFile.txt): <<Give the newly created file name present in the same working directory or Just press enter to take the default file for processing>>


		Message generated as the file is being processed:
		Reading the from address and message from the input file
		Retrieving Governor's address from the Civic API
		Creating a HTML TEMPLATE
		Creating the Letter

	Step c) Use the resulting url in your browser to find the created 			letter.

		Output:
		Url for Letter: https://s3.us-west-2.amazonaws.com/assets.lob.com/ltr_b1fb0befafea5057_thumb_large_1.png?AWSAccessKeyId=AKIAIILJUBJGGIBQDPQQ&Expires=1515910095&Signature=V0vBhopIjXsn65neoYQWIxCb8RM%3D




