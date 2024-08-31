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
$result = $conn->query("SELECT
    DATE_FORMAT(time, '%Y-%m-%d %H:00:00') AS hour,
    COUNT(*) AS count,
    SUM(CAST(available_in_parking_1 AS UNSIGNED)) AS total_available_in_parking_1,
    SUM(CAST(available_in_parking_2 AS UNSIGNED)) AS total_available_in_parking_2,
    SUM(CAST(nearest_in_parking_1 AS UNSIGNED)) AS total_nearest_in_parking_1,
    SUM(CAST(nearest_in_parking_2 AS UNSIGNED)) AS total_nearest_in_parking_2
FROM
    traffic
GROUP BY
    hour
ORDER BY
    hour;");
$data = array();

while($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode($data);

$conn->close();
?>
