import gspread

sa = gspread.service_account(filename="service_account.json")
sh = sa.open("EpiFinderAutomattedAnnotations")

#wks = sh.worksheet("Sheet1")

def listOfSheets():
    worksheet_list = sh.worksheets()
    worksheetTitles = []
    for i in range(len(worksheet_list)):
        worksheetTitles.append(parseSheetsTitle(str(sh.get_worksheet(i))))
    return worksheetTitles

def parseSheetsTitle(str1):
    title = str1[str1.find(' \'')+2:str1.find('\' ')]
    return title

def currentWorksheet(str1):
    sheet_list = listOfSheets()
    wks = ''
    if str1 in sheet_list:
        wks = sh.worksheet(str1)
    elif str1 not in sheet_list:
        wks = sh.add_worksheet(title=str1, rows='2000', cols='20')
        wks = sh.worksheet(str1)
    return wks
            
# Get a single or multiple cells
#print(wks.acell('C1').value)
#print(wks.cell(3,4))
#print(wks.get('A1:E3'))

# Get all cells
#print(wks.get_all_records())
#print(wks.get_all_values())

# Update a cell
#wks.update('A3', 'Anthony')
#print(wks.acell('A3'))

# Update multiple cells
#wks.update('D2:E3', [['Brethern', 'Tenis'], ['major business', 'pottery']])
#print(wks.get('D2:E3'))

# Delete a row
#wks.delete_rows(2)

def _batch(self, requests):
    body = {
        'requests': requests
    }
    return self._service.spreadsheets().batchUpdate(spreadsheetId=self.spreadsheetId, body=body).execute()

def renameSheet(self, sheetId, newName):
    return self._batch({
        "updateSheetProperties": {
            "properties": {
                "sheetId": sheetId,
                "title": newName,
            },
            "fields": "title",
        }
    })

print("Sheets API Loading...")