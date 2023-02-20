Source: https://oersi.org/resources/pages/de/docs/api/data/

1) activate wsl in the terminal. 
2) Then the curl commands from above links can be run one by one.
3) Make sure to set the time of the "keep_alive" to be more than 15 mins as it will be the same pit id for that amount of minutes.
4) Entity provider names can be changed to gather the data from a particular source. 
5) Refer to comments posted in "loadFiles.ipynb" or "loadFilesPythonScript.py" for in-depth functioning of the code.

Locally saved Json files can be stored in drive directory:  \BE O365 MS-Cloud\BG365 - E365 Maverick - General\Daten\Oersi Json Files


How to find out the correct Entityprovider Name to implement in the script : 

1) Go to oersi.org. Select the particular provider on the left side of the "Quelle" tab. 
2) select one of the shown results and copy the title name.
3) Paste the name in the query section of the curl command mentioned below  and run the curl command in wsl.
4) curl -X 'POST' 'https://oersi.org/resources/api/search/oer_data/_search?pretty' \
-H 'Content-Type: application/json' -H 'accept: application/json' \
-d '{"query": {"query_string": {"query": "(Mittelwertbildung verringert Varianz)"}}}'
5) search the title name in the results from the curl command.
6) look for "entityprovider" and  there you will find the entity provider name which can be used in the script. 


