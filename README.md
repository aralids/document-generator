# document-generator

## To run doc-gen on Linux:
- Enter `docker build -t doc-gen .`
- Enter `docker run -p 9000:9000 doc-gen`
- You can now generate PDF files by using the user interface at `http://localhost:9000/` or by making POST requests to `http://localhost:9000/pdf`

- An example: `curl -H "Content-Type: application/json" -d '{"id": "e6caeb37-1590-436d-ad06-5977c4d621ff","external_id": "573c36e1-7c0a-4e16-944b-a98db61189f4","origin": "Zeitschrift","print_group_name": "UBJCS ZB ZSS Spezial","data": [{"effectiveLocationId": "29e31115-b52d-483d-a692-3209f7f25fbe","effectiveLocationName": "Magazin Zeughaus","fulfillmentPreference": "Hold Shelf","instanceContributorName": "Rocznik, Karl","instanceTitle": "Wetter und Klima in Bayern : ein Beitrag zur bayerischen Heimatkunde / Karl Rocznik","itemBarcode": "85294156","itemCallNumber": "205 RF 10423 R684","itemLocationLibraryName": "Zweigbibliothek Zeughaus","itemMaterialTypeId": "24080190-7539-4520-bde1-762f57d006fc","itemMaterialTypeName": "Druckschrift","itemPermanentLoanTypeId": "ecfbf446-421a-4a46-8e06-3e1e36d5b317","itemPermanentLoanTypeName": "0 u Ausleihbar","pickupServicePointId": "dd10b2e9-7ad5-4ec3-89e1-e771664d76ed","pickupServicePointName": "ZB Ausleihe","requestDate": "2024-08-06T11:37:58.799","requestId": "573c36e1-7c0a-4e16-944b-a98db61189f4","requestStatus": "Open - Not yet filled","requestTypeName": "Page","requesterBarcode": "00099997","requesterFirstName": "Stefan","requesterLastName": "HRZ-Administrator","requesterPatronGroupDescription": "UB-Mitarbeiter","requesterPatronGroupId": "9e7a5f7d-bf8a-408f-a02e-f0f5576a8214","returnCounterFullName": "Superuser","returnCounterId": "1b1900a4-dd88-4d0d-b2f2-3a9d765fd628"}],"received_at": "2024-09-23T11:27:45.075139"}' 127.0.0.1:9000/ > file.pdf`
