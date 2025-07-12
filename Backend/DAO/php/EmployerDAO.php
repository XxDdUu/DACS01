<?php
require_once 'config.php';

$db = new Database();
$conn = $db->connect();

function insert_employer($conn, $data) {
    try {
        $username = $data["username"];
        $email = $data["email"];
        $phone_number = $data["phone_number"];
        $enterprise_id = $data["enterprise_id"];
        $enterprise_password_employer = $data["enterprise_password_employer"];
        $dateofbirth = $data["date_of_birth"];
        $password = $data["password"];
        $confirm_password = $data["confirm_password"];

        if ($password !== $confirm_password) {
            throw new Exception("Mật khẩu xác nhận không khớp.");
        }

        // Hash mật khẩu
        $hashed_password = password_hash($password, PASSWORD_DEFAULT);

        // Dùng prepared statement để tránh SQL injection
        $stmt = $conn->prepare("INSERT INTO EMPLOYER 
            (Employer_name, Employer_Phone_Number, Employer_Email, DOB, Employer_password, Enterprise_ID)
            VALUES (?, ?, ?, ?, ?, ?)");

        $stmt->bind_param("sssssi", $username, $phone_number, $email, $dateofbirth, $hashed_password, $enterprise_id);

        if ($stmt->execute()) {
            echo "Thêm người dùng thành công.";
        } else {
            throw new Exception("Lỗi khi thêm người dùng: " . $stmt->error);
        }

        $stmt->close();
    } catch (Exception $e) {
        echo json_encode(["error" => $e->getMessage()]);
    }
}

// Gọi hàm ví dụ (chỉ nên dùng khi test)
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    insert_employer($conn, $_POST);
}

$conn->close();
?>
