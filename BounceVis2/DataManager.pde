
class DataManager {
  Table table = new Table();  
  
  DataManager() {
  }
  
  void createCsvFile(String[] columns) {
    // Add columns to the table
    for (int i = 0; i < columns.length; i++) {
      table.addColumn(columns[i]);
    }
  }
  
  void addRow(String[] values) {
    // Add some sample rows (you can modify this as needed)
    TableRow newRow = table.addRow();
    for (int i = 0; i < values.length; i++) {
      newRow.setString(i, values[i]);
    }
  }
  
  void saveFile(String filename) {
    // Save the table to a CSV file
    saveTable(table, filename);
    println("CSV file saved as " + filename);
  }
}
