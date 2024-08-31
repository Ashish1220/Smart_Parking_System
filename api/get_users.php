<?php
// db.php - Connect to the database
header("Access-Control-Allow-Origin: *"); // Allow requests from any origin
header("Access-Control-Allow-Methods: GET, POST, OPTIONS"); // Allow specific HTTP methods
header("Access-Control-Allow-Headers: Content-Type"); // Allow specific headers

header("Content-Type: application/json");
$conn = new mysqli("localhost", "root", "", "smart parking system");

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Fetch data
$result = $conn->query("SELECT * FROM traffic");
$data = array();

while($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode($data);

$conn->close();
?>
