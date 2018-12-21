Attribute VB_Name = "Module1"
Sub Fill_Product_Table()
'
' Macro1 Macro
'
' Keyboard Shortcut: Ctrl+Shift+Y

    MsgBox "Hello World - Excel VBA Begins here"
    Application.ScreenUpdating = False
    
' Call python function to fetch the latest prices from websites
    RunPython ("import trackProducts; trackProducts.tracking()")
    
' update the graphs after reading csv data from new_file
    Sheets("Sheet1").Select
    Columns("A:A").Select
    For i = 1 To 10
       Selection.Delete Shift:=xlToLeft
    Next i
    With ActiveSheet.ListObjects.Add(SourceType:=0, Source:= _
        "OLEDB;Provider=Microsoft.Mashup.OleDb.1;Data Source=$Workbook$;Location=""new_file"";Extended Properties=""""" _
        , Destination:=Range("$A$1")).QueryTable
        .CommandType = xlCmdSql
        .CommandText = Array("SELECT * FROM [new_file]")
        .RowNumbers = False
        .FillAdjacentFormulas = False
        .PreserveFormatting = True
        .RefreshOnFileOpen = False
        .BackgroundQuery = True
        .RefreshStyle = xlInsertDeleteCells
        .SavePassword = False
        .SaveData = True
        .AdjustColumnWidth = True
        .RefreshPeriod = 0
        .PreserveColumnInfo = True
        .ListObject.DisplayName = "product_table"
        .Refresh BackgroundQuery:=False
    End With
    Columns("I:I").Select
    Selection.NumberFormat = "[$-en-US]m/d/yy h:mm AM/PM;@"
    ActiveWorkbook.Save
    MsgBox "Hello World - Excel VBA Ends here"
    Application.ScreenUpdating = True
End Sub




