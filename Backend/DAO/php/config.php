<?php 
class Database {
	private $host = "localhost";
	private $user = "hf7f07df09_QLDTCNCH";
	private $pass = "*********";
    private $dbname = "hf7f07df09_QLDTCNCH";
    private $conn;

    public function connect() {
    	$this->conn = new mysqli (
    		$this->host,
    		$this->user,
    		$this->pass,
    		$this->dbname
    	);
    	if ($this->conn->connect_error) {
    		die(json_encode(["error" => "Connection error: " .$this->conn->connect_error]));
    	}
    	$this->conn->set_charset("utf8mb4");
    	return $this->conn;
    }
}
?>