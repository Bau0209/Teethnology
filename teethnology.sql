-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: teethnology
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `account_activity`
--

DROP TABLE IF EXISTS `account_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_activity` (
  `activity_id` int NOT NULL AUTO_INCREMENT,
  `account_id` int NOT NULL,
  `action` varchar(255) NOT NULL,
  `date_and_time` datetime NOT NULL,
  `module` varchar(255) NOT NULL,
  `target` varchar(255) NOT NULL,
  `details` text,
  PRIMARY KEY (`activity_id`),
  KEY `account_id` (`account_id`),
  CONSTRAINT `account_activity_ibfk_1` FOREIGN KEY (`account_id`) REFERENCES `accounts` (`account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_activity`
--

LOCK TABLES `account_activity` WRITE;
/*!40000 ALTER TABLE `account_activity` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts`
--

DROP TABLE IF EXISTS `accounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accounts` (
  `account_id` int NOT NULL AUTO_INCREMENT,
  `employee_id` int NOT NULL,
  `email` varchar(255) NOT NULL,
  `account_password` varchar(255) NOT NULL,
  `access_level` enum('owner','staff') NOT NULL DEFAULT 'staff',
  `account_status` enum('active','inactive') NOT NULL DEFAULT 'active',
  PRIMARY KEY (`account_id`),
  UNIQUE KEY `email` (`email`),
  KEY `accounts_ibfk_1` (`employee_id`),
  CONSTRAINT `accounts_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (1,1,'john.doe@example.com','securepassword123','owner','active'),(2,2,'sam.versoza@gmail.com','securepassword123','staff','active');
/*!40000 ALTER TABLE `accounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `appointment_id` int NOT NULL AUTO_INCREMENT,
  `branch_id` int NOT NULL,
  `patient_id` int NOT NULL,
  `returning_patient` tinyint(1) NOT NULL DEFAULT '0',
  `appointment_sched` datetime NOT NULL,
  `alternative_sched` datetime DEFAULT NULL,
  `appointment_type` varchar(255) NOT NULL,
  `appointment_status` enum('pending','approved','cancelled') NOT NULL DEFAULT 'pending',
  `request_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `approval_date` datetime DEFAULT NULL,
  `approved_by` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`appointment_id`),
  KEY `branch_id` (`branch_id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`branch_id`) REFERENCES `branch` (`branch_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`patient_id`) REFERENCES `patient_info` (`patient_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=71 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (1,1,1,0,'2024-01-15 09:00:00',NULL,'Tooth Extraction','approved','2024-01-10 08:00:00','2024-01-12 14:00:00','Dr. Reyes'),(2,1,1,1,'2024-03-10 10:30:00',NULL,'Oral Prophylaxis','approved','2024-03-05 11:00:00','2024-03-07 09:00:00','Dr. Reyes'),(3,1,2,0,'2024-02-25 11:00:00',NULL,'Dental Filling','approved','2024-02-20 13:00:00','2024-02-22 10:00:00','Dr. Santos'),(4,2,3,0,'2024-04-12 14:00:00',NULL,'Root Canal Therapy (Session 1)','approved','2024-04-07 09:30:00','2024-04-10 16:00:00','Dr. Tan'),(5,2,3,1,'2024-05-05 10:00:00',NULL,'Temporary Crown Placement','approved','2024-05-01 12:00:00','2024-05-03 14:00:00','Dr. Tan'),(6,2,4,0,'2024-01-10 09:00:00',NULL,'Orthodontic Consultation','approved','2024-01-05 08:00:00','2024-01-08 12:00:00','Dr. Garcia'),(7,2,4,1,'2024-02-05 10:00:00',NULL,'Braces Installation','approved','2024-01-30 13:00:00','2024-02-02 15:00:00','Dr. Garcia'),(8,2,4,1,'2024-03-05 10:00:00',NULL,'Braces Adjustment (Month 1)','approved','2024-03-01 09:30:00','2024-03-03 16:00:00','Dr. Garcia'),(9,2,4,1,'2024-04-05 10:00:00',NULL,'Braces Adjustment (Month 2)','approved','2024-04-01 11:00:00','2024-04-03 13:00:00','Dr. Garcia'),(10,2,4,1,'2024-05-04 10:00:00',NULL,'Braces Adjustment (Month 3)','approved','2024-05-01 11:00:00','2024-05-03 13:00:00','Dr. Garcia'),(11,2,4,1,'2024-06-05 10:00:00',NULL,'Braces Adjustment (Month 4)','approved','2024-06-01 11:00:00','2024-06-03 13:00:00','Dr. Garcia'),(12,1,5,0,'2025-07-31 16:00:00','2025-07-30 18:00:00','Tooth Extraction','pending','2025-07-01 14:28:01',NULL,NULL),(24,1,2,1,'2025-07-23 16:30:00',NULL,'Consultation','approved','2025-07-02 06:26:05',NULL,NULL),(26,1,1,1,'2025-07-30 10:30:00',NULL,'Tooth Extraction','approved','2025-07-02 09:31:20',NULL,NULL),(29,2,3,1,'2025-07-10 16:00:00',NULL,'Tooth Extraction','approved','2025-07-03 02:09:44',NULL,NULL),(44,1,26,1,'2025-06-10 09:00:00','2025-06-11 11:00:00','Follow-up Cleaning','approved','2025-07-05 01:13:57','2025-07-05 01:13:57','Dr. Ortega'),(45,1,27,1,'2025-03-15 14:00:00','2025-03-16 10:00:00','Wisdom Tooth Removal','approved','2025-07-05 01:19:20','2025-07-05 01:19:20','Dr. Mendoza'),(46,1,28,1,'2025-05-22 13:30:00','2025-05-23 09:00:00','Filling Replacement','approved','2025-07-05 01:22:58','2025-07-05 01:22:58','Dr. Tan'),(47,1,29,0,'2025-04-12 15:00:00','2025-04-13 10:00:00','Tooth Bonding','approved','2025-07-05 01:24:43','2025-07-05 01:24:43','Dr. Cruz'),(48,1,30,1,'2025-07-01 10:00:00','2025-06-19 14:00:00','Filling Procedure','approved','2025-07-05 01:24:57','2025-07-05 01:24:57','Dr. Velasquez'),(49,1,31,1,'2025-08-08 11:00:00','2025-08-09 13:00:00','Internal Bleaching','pending','2025-07-05 01:26:51','2025-07-05 01:26:51','Dr. Carreon'),(50,1,32,1,'2025-09-12 10:30:00','2025-09-13 14:30:00','Root Canal Therapy','approved','2025-07-05 01:26:58','2025-07-05 01:26:58','Dr. Trinidad'),(51,1,33,1,'2025-10-02 15:00:00','2025-10-03 13:00:00','Wisdom Tooth Extraction','approved','2025-07-05 01:31:20','2025-07-05 01:31:20','Dr. Fabian'),(52,1,34,1,'2025-10-22 09:30:00','2025-10-23 10:30:00','Deep Cleaning','pending','2025-07-05 01:36:12','2025-07-05 01:36:12','Dr. Yulo'),(55,1,35,1,'2025-11-10 14:00:00','2025-11-11 10:00:00','Crown Preparation','approved','2025-07-05 01:39:18','2025-07-05 01:39:18','Dr. Valencia'),(56,1,36,1,'2025-09-28 10:30:00','2025-09-29 08:30:00','Desensitizing Treatment','pending','2025-07-05 01:40:14','2025-07-05 01:40:14','Dr. Santos'),(57,1,37,1,'2025-08-02 15:00:00','2025-08-03 13:00:00','Occlusal Adjustment','approved','2025-07-05 01:40:36','2025-07-05 01:40:36','Dr. Lim'),(58,1,39,0,'2025-01-18 13:30:00','2025-01-19 10:00:00','Tooth Filling','approved','2025-01-05 00:00:00','2025-01-06 00:00:00','Dr. Beltran'),(60,1,40,0,'2025-02-14 11:00:00','2025-02-15 09:00:00','Extraction Consultation','approved','2025-02-01 00:00:00','2025-02-03 00:00:00','Dr. Gomez'),(61,1,41,0,'2025-07-04 11:30:00','2025-07-03 15:00:00','Root Canal Therapy','approved','2025-07-05 10:29:57','2025-07-05 10:29:57','Dr. Lopez'),(62,2,44,0,'2025-07-05 10:00:00','2025-07-06 14:00:00','Cosmetic Bonding','approved','2025-07-05 10:46:26','2025-07-05 10:46:26','Dr. Tan'),(64,2,45,0,'2025-08-07 11:00:00',NULL,'Tooth Extraction','approved','2025-07-05 02:54:36',NULL,NULL),(65,1,46,0,'2025-07-05 12:49:00',NULL,'Consultation','approved','2025-07-05 04:49:48',NULL,NULL),(66,1,46,1,'2025-07-06 01:00:00',NULL,'Brace Adjustment','approved','2025-07-05 05:05:56',NULL,NULL),(67,1,47,0,'2025-07-17 13:30:00','2025-07-24 15:30:00','consultation','pending','2025-07-14 05:21:39',NULL,NULL),(68,1,1,1,'2025-07-23 17:00:00',NULL,'Consultation','pending','2025-07-14 06:17:24',NULL,NULL),(69,1,1,1,'2025-07-21 16:00:00',NULL,'Consultation','pending','2025-07-14 06:38:17',NULL,NULL),(70,1,1,1,'2025-07-14 17:00:00',NULL,'Consultation','pending','2025-07-14 06:40:56',NULL,NULL);
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `branch`
--

DROP TABLE IF EXISTS `branch`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `branch` (
  `branch_id` int NOT NULL AUTO_INCREMENT,
  `branch_name` varchar(100) NOT NULL,
  `full_address` varchar(255) NOT NULL,
  `clinic_description` text NOT NULL,
  `chief_dentist` varchar(255) NOT NULL,
  `contact_number` varchar(15) NOT NULL,
  `clinic_open_hour` time NOT NULL,
  `clinic_close_hour` time NOT NULL,
  `services` text NOT NULL,
  PRIMARY KEY (`branch_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branch`
--

LOCK TABLES `branch` WRITE;
/*!40000 ALTER TABLE `branch` DISABLE KEYS */;
INSERT INTO `branch` VALUES (1,'JCS Manila branch','123 Main St, Manila City','A modern dental clinic offering general and cosmetic services.','Dr. Elsa Cruz','09171234567','07:00:00','17:00:00','Preventive Dentistry,Intervention Dentistry,Orthodontics'),(2,'JCS Quezon City Branch','123 Main St, Quezon City','A modern dental clinic offering general and cosmetic services.','Dr. Juan Cruz','09181334435','08:00:00','18:00:00','Preventive Dentistry,Intervention Dentistry,Orthodontics');
/*!40000 ALTER TABLE `branch` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `chart_legend`
--

DROP TABLE IF EXISTS `chart_legend`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `chart_legend` (
  `condition_code` varchar(10) NOT NULL,
  `description` text,
  PRIMARY KEY (`condition_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `chart_legend`
--

LOCK TABLES `chart_legend` WRITE;
/*!40000 ALTER TABLE `chart_legend` DISABLE KEYS */;
INSERT INTO `chart_legend` VALUES ('/','Present Teeth'),('A','Amalgam Filling'),('AB','Abutment'),('Cm','Congenitally Missing'),('D','Decayed (Caries Indicated for Filling)'),('F','Filled'),('Fx','Fixed Cure Composite'),('I','Caries Indicated for Extraction'),('Im','Impacted Tooth'),('In','Inlay'),('J','Jacket Crown'),('M','Missing'),('MO','Missing due to Other Causes'),('P','Pontic'),('RF','Root Fragment'),('Rm','Removable Denture'),('S','Sealants'),('Sp','Supernumerary'),('X','Extraction due to Caries'),('XO','Extraction due to Other Causes');
/*!40000 ALTER TABLE `chart_legend` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clinic_branch_images`
--

DROP TABLE IF EXISTS `clinic_branch_images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clinic_branch_images` (
  `image_id` int NOT NULL AUTO_INCREMENT,
  `image_link` text NOT NULL,
  `branch_id` int NOT NULL,
  PRIMARY KEY (`image_id`),
  KEY `branch_id` (`branch_id`),
  CONSTRAINT `clinic_branch_images_ibfk_1` FOREIGN KEY (`branch_id`) REFERENCES `branch` (`branch_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clinic_branch_images`
--

LOCK TABLES `clinic_branch_images` WRITE;
/*!40000 ALTER TABLE `clinic_branch_images` DISABLE KEYS */;
INSERT INTO `clinic_branch_images` VALUES (1,'uploads/branches/manila1.jpg',1),(2,'uploads/branches/quezoncity1.jpg',2),(5,'uploads/branches/494361512_1898900354194506_7671129708134362962_n.jpg',1);
/*!40000 ALTER TABLE `clinic_branch_images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dental_chart_teeth`
--

DROP TABLE IF EXISTS `dental_chart_teeth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dental_chart_teeth` (
  `teeth_id` int NOT NULL AUTO_INCREMENT,
  `dental_chart_id` int NOT NULL,
  `tooth_number` varchar(10) NOT NULL,
  `teeth_condition` enum('D','M','F','I','RF','MO','Im','J','A','AB','P','In','Fx','S','Rm','X','XO','/','Cm','Sp','') DEFAULT '',
  `notes` text,
  PRIMARY KEY (`teeth_id`),
  KEY `dental_chart_id` (`dental_chart_id`),
  CONSTRAINT `dental_chart_teeth_ibfk_1` FOREIGN KEY (`dental_chart_id`) REFERENCES `dental_charting` (`dental_chart_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dental_chart_teeth`
--

LOCK TABLES `dental_chart_teeth` WRITE;
/*!40000 ALTER TABLE `dental_chart_teeth` DISABLE KEYS */;
/*!40000 ALTER TABLE `dental_chart_teeth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dental_charting`
--

DROP TABLE IF EXISTS `dental_charting`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dental_charting` (
  `dental_chart_id` int NOT NULL AUTO_INCREMENT,
  `dental_record_id` int NOT NULL,
  `date_taken` date NOT NULL,
  `chart_notes` text,
  `dental_chart_image_link` text,
  PRIMARY KEY (`dental_chart_id`),
  KEY `dental_record_id` (`dental_record_id`),
  CONSTRAINT `dental_charting_ibfk_1` FOREIGN KEY (`dental_record_id`) REFERENCES `dental_record` (`dental_record_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dental_charting`
--

LOCK TABLES `dental_charting` WRITE;
/*!40000 ALTER TABLE `dental_charting` DISABLE KEYS */;
/*!40000 ALTER TABLE `dental_charting` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dental_record`
--

DROP TABLE IF EXISTS `dental_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dental_record` (
  `dental_record_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `dental_record_image_link` text,
  `periodontal_screening` text,
  `occlusion` text,
  `appliances` text,
  `TMD` text,
  PRIMARY KEY (`dental_record_id`),
  KEY `patient_id` (`patient_id`),
  CONSTRAINT `dental_record_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient_info` (`patient_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dental_record`
--

LOCK TABLES `dental_record` WRITE;
/*!40000 ALTER TABLE `dental_record` DISABLE KEYS */;
INSERT INTO `dental_record` VALUES (6,1,'uploads/patients_record/11.png','Gingivitis, Early Periodontitis','Class (Molar), Overjet Overbite','Orthodontic','Clicking, Clenching'),(7,2,'uploads/patients_record/21.png','Moderate Periodontitis','Midline Deviation, Crossbite','Stayplate','None'),(8,3,'uploads/patients_record/31.png','Advanced Periodontitis','Class (Molar), Midline Deviation, Overjet Overbite','Orthodontic, Stayplate','Trismus, Muscle Spasm'),(9,4,'uploads/patients_record/41.png','Gingivitis','None','None','None'),(13,26,NULL,'Mild gingivitis','Class II','Retainers','Mild clicking'),(14,27,NULL,'Healthy','Class I','Night guard','None'),(15,28,NULL,'Moderate gingivitis','Class II','Braces (past)','No symptoms'),(16,29,NULL,'Healthy','Class I','None','None'),(17,30,NULL,'Slight inflammation','Class II','None','None'),(18,31,NULL,'Healthy','Edge-to-edge','None','Jaw clicking during yawning'),(19,32,NULL,'Moderate inflammation','Class II Division 2','Clear aligners','Occasional locking'),(20,33,NULL,'Mild inflammation','Normal','None','None'),(21,34,NULL,'Localized gingivitis','Class I','None','None'),(22,35,NULL,'Mild gingival recession','Class I','None','None'),(23,35,NULL,'Mild gingival recession','Class I','None','None'),(24,36,NULL,'Healthy','Normal','None','None'),(25,37,NULL,'Healthy','Crossbite','Removable retainers','Mild TMJ discomfort'),(26,39,NULL,'Mild inflammation','Class I','None','None'),(27,40,NULL,'Mild bleeding','Class I','None','Jaw clicking'),(29,41,NULL,'Localized moderate inflammation','Class I','None','Clicking jaw sound'),(30,41,NULL,'Localized moderate inflammation','Class I','None','Clicking jaw sound'),(31,44,NULL,'Generalized mild gingivitis','Class II','Night guard','None');
/*!40000 ALTER TABLE `dental_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `employee_id` int NOT NULL AUTO_INCREMENT,
  `branch_id` int NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `middle_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `birthdate` date NOT NULL,
  `sex` enum('f','m') NOT NULL,
  `contact_number` varchar(15) NOT NULL,
  `email` varchar(255) NOT NULL,
  `employment_status` enum('active','inactive') DEFAULT 'active',
  `date_hired` date NOT NULL,
  `position` varchar(255) NOT NULL,
  `department` varchar(255) DEFAULT NULL,
  `license_number` varchar(255) DEFAULT NULL,
  `shift_days` text NOT NULL,
  `shift_hours` text NOT NULL,
  PRIMARY KEY (`employee_id`),
  KEY `branch_id` (`branch_id`),
  CONSTRAINT `employees_ibfk_1` FOREIGN KEY (`branch_id`) REFERENCES `branch` (`branch_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES (1,1,'John','A.','Doe','1990-05-15','m','09171234567','john.doe@example.com','active','2024-01-10','Owner','Dental','PRC1234567','Monday, Wednesday, Friday','08:00 AM - 05:00 PM'),(2,2,'Sammy','B.','Versoza','1990-06-15','f','09472834','sam.versoza@gmail.com','active','2024-01-10','Dentist','Dental','PRC1234568','Monday, Wednesday, Friday','08:00 AM - 06:00 PM');
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_website`
--

DROP TABLE IF EXISTS `main_website`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_website` (
  `main_website` bigint NOT NULL,
  `clinic_name` varchar(255) DEFAULT NULL,
  `about_us` text NOT NULL,
  `services` text NOT NULL,
  `main_email` text,
  `main_contact_number` text,
  PRIMARY KEY (`main_website`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_website`
--

LOCK TABLES `main_website` WRITE;
/*!40000 ALTER TABLE `main_website` DISABLE KEYS */;
INSERT INTO `main_website` VALUES (1,'JCS Dental Clinic','JCS Dental Clinic is committed to providing top-quality dental care with modern equipment and a caring team.','Preventive Dentistry,Intervention Dentistry,Coroneric Dentistry','JCSmilesclinic@gmail.com','+63 912 345 6789');
/*!40000 ALTER TABLE `main_website` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_info`
--

DROP TABLE IF EXISTS `patient_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient_info` (
  `patient_id` int NOT NULL AUTO_INCREMENT,
  `branch_id` int NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `middle_name` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `birthdate` date NOT NULL,
  `sex` char(1) NOT NULL,
  `contact_number` varchar(15) NOT NULL,
  `email` varchar(255) NOT NULL,
  `address_line1` varchar(255) NOT NULL,
  `baranggay` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `province` varchar(255) NOT NULL,
  `country` varchar(60) NOT NULL,
  `initial_consultation_reason` text NOT NULL,
  `occupation` varchar(255) DEFAULT NULL,
  `office_number` varchar(255) DEFAULT NULL,
  `guardian_first_name` varchar(255) DEFAULT NULL,
  `guardian_middle_name` varchar(255) DEFAULT NULL,
  `guardian_last_name` varchar(255) DEFAULT NULL,
  `guardian_occupation` varchar(255) DEFAULT NULL,
  `reffered_by` varchar(255) DEFAULT NULL,
  `previous_dentist` varchar(255) DEFAULT NULL,
  `last_dental_visit` date DEFAULT NULL,
  `image_link` text,
  PRIMARY KEY (`patient_id`),
  KEY `branch_id` (`branch_id`),
  CONSTRAINT `patient_info_ibfk_1` FOREIGN KEY (`branch_id`) REFERENCES `branch` (`branch_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_info`
--

LOCK TABLES `patient_info` WRITE;
/*!40000 ALTER TABLE `patient_info` DISABLE KEYS */;
INSERT INTO `patient_info` VALUES (1,1,'Juana','Santos','Dela Cruz','1990-05-15','M','09171234567','juan.dc@example.com','123 Mabuhay St.','Barangay Uno','Manila','Metro Manila','Philippines','Dentures','Engineer','02-1234567',NULL,NULL,NULL,'None','Friend','Dr. Reyes',NULL,NULL),(2,1,'Maria','Luisa','Reyes','1985-08-22','F','09179876543','maria.reyes@example.com','456 Maligaya Ave.','Barangay Dos','Manila','Metro Manila','Philippines','Braces','Teacher','02-7654321','Lola','Cruz','Reyes','Retired','','None',NULL,NULL),(3,2,'Carlos','David','Santos','1992-02-10','M','09172345678','carlos.santos@example.com','789 Payapa Blvd.','Barangay Tres','Quezon City','Metro Manila','Philippines','Tooth ache','Designer','02-5566778',NULL,NULL,NULL,NULL,'Online Ad','Dr. Tan','2022-12-15',NULL),(4,2,'Angela','Marie','Lopez','1996-11-05','F','09173456789','angela.lopez@example.com','321 Tahimik Lane','Barangay Cuatro','Quezon City','Metro Manila','Philippines','Tooth ache','Student',NULL,'Anna','Grace','Lopez','Nurse','School','None',NULL,NULL),(5,1,'Samantha','Reyes','Bautista','2004-02-09','F','09501055477','ejbautista0209@gmail.com','129 Hello lane','Baranggay 567','Pasay City','Metro Manila','Philippines','Tooth ache','','None',NULL,NULL,NULL,'None','None','None',NULL,NULL),(26,1,'Sofia','Luisa','Velasco','1990-04-12','F','09185551123','sofia.velasco@example.com','456 Peace St','Barangay Dos','Smile City','ProvinceY','Philippines','Routine cleaning and whitening','Bank Teller','5554321',NULL,NULL,NULL,'Nurse','TV Ad','Dr. Enriquez',NULL,NULL),(27,1,'Enrico','Dela','Cruz','1988-11-05','M','09189997777','enrico.cruz@example.com','789 Smile Ave','Barangay Tres','Bright City','ProvinceZ','Philippines','Tooth extraction pain','Software Developer','8800555','Carla','Reyes','Cruz','Accountant','Online Ad','Dr. Felix','2023-10-10',NULL),(28,1,'Carmela','Ramos','Flores','1992-02-18','F','09181230098','carmela.flores@example.com','123 Rosewood St','Barangay Cuatro','Toothville','ProvinceA','Philippines','Pain in upper molar','Marketing Specialist','4412345','Angela','Ramos','Flores','Businesswoman','Facebook Ad','Dr. Ignacio','2023-08-22',NULL),(29,1,'Lorenzo','Manuel','Santos','1987-09-01','M','09181231122','lorenzo.santos@example.com','88 Dental Blvd','Barangay Cinco','Whitesmile City','ProvinceB','Philippines','Chipped front tooth','Architect','2345098','Elena','Martinez','Santos','Civil Engineer','Billboard','Dr. Robles','2023-11-12',NULL),(30,1,'Bianca','Morales','Reyes','1993-12-25','F','09173445566','bianca.reyes@example.com','201 Bright Smile St','Barangay Seis','Tooth City','ProvinceC','Philippines','Large cavity with sensitivity','Pharmacist','0998822','Cristina','Morales','Reyes','Lab Technician','Sibling','Dr. Gomez','2023-07-05',NULL),(31,1,'Nathaniel','Jose','Del Rosario','1985-07-15','M','09179998888','nathaniel.delrosario@example.com','502 Mint Lane','Barangay Siete','Dentalia','ProvinceD','Philippines','Discoloration on front tooth','Sales Manager','1239876','Consuelo','Santos','Del Rosario','Entrepreneur','Friend','Dr. Abad','2022-10-01',NULL),(32,1,'Clarisse','Anne','Gonzales','1997-06-27','F','09181112233','clarisse.gonzales@example.com','701 Smile Heights','Barangay Ocho','Pearl City','ProvinceE','Philippines','Tooth pain while chewing','Law Student','0202044','Veronica','Ramos','Gonzales','Lawyer','TikTok Ad','Dr. Mercado','2024-01-10',NULL),(33,1,'Elijah','Cruz','Manalo','2000-03-22','M','09182224444','elijah.manalo@example.com','888 Smile Drive','Barangay Nueve','Molar City','ProvinceF','Philippines','Wisdom tooth pain','Software Engineer','09003456','Liza','Reyes','Manalo','Nurse','Colleague','Dr. Fabian','2023-06-01',NULL),(34,1,'Kerbi','Elaine','Reyes','1998-12-04','F','09179992233','bianca.reyes@example.com','102 Blossom St','Barangay Trece','Toothville','ProvinceJ','Philippines','Mild gum bleeding while brushing','Marketing Analyst','0312123','Angela','Domingo','Reyes','Accountant','Company Wellness Program','Dr. Yulo','2024-10-01',NULL),(35,1,'Rafael','Domingo','Bautista','1989-09-18','M','09181234567','rafael.bautista@example.com','45 Smile Ave','Barangay Catorce','Bright City','ProvinceK','Philippines','Cracked molar','Architect','0221122','Isabel','Dela Cruz','Bautista','Engineer','Workmate','Dr. Valencia','2023-03-15',NULL),(36,1,'Rafael','Domingo','Bautista','1989-09-18','M','09181234567','rafael.bautista@example.com','45 Smile Ave','Barangay Catorce','Bright City','ProvinceK','Philippines','Cracked molar','Architect','0221122','Isabel','Dela Cruz','Bautista','Engineer','Workmate','Dr. Valencia','2023-03-15',NULL),(37,1,'Andrea','Mae','Cruz','2001-03-07','F','09181239876','andrea.cruz@example.com','908 Dental St','Barangay Quince','Gumtown','ProvinceL','Philippines','Tooth sensitivity to cold','Medical Technologist','0321987','Luz','Navarro','Cruz','Pharmacist','Poster Ad','Dr. Santos','2024-04-20',NULL),(38,1,'Louie','Enrique','Navarro','1990-11-30','M','09189998888','louie.navarro@example.com','17 Ortho Street','Barangay Diecisiete','Crownsville','ProvinceM','Philippines','Bite misalignment','Chef','0456789','Victoria','Lopez','Navarro','Restaurateur','YouTube Ad','Dr. Lim','2023-08-05',NULL),(39,1,'Julian','Rey','Santos','1993-05-15','M','09187776655','julian.santos@example.com','87 Dental Way','Barangay Uno','Happyville','ProvinceN','Philippines','Cavity pain in upper molar','IT Consultant','0345567','Gloria','De Vera','Santos','Teacher','Company Ad','Dr. Beltran','2023-09-20',NULL),(40,1,'Mikaella','Dionne','Chua','1997-02-22','F','09182345678','mika.chua@example.com','55 Serenity Lane','Barangay Dos','Tooth City','ProvinceO','Philippines','Wisdom tooth discomfort','Copywriter','0332211','Lilian','Tan','Chua','Editor','Friend','Dr. Gomez','2023-12-01',NULL),(41,1,'Miguel','Antonio','Santos','1985-05-14','M','09178887766','miguel.santos@example.com','812 Healthy Smile Ave','Barangay Uno','Tooth City','ProvinceA','Philippines','Severe toothache and swelling','Engineer','09176543210','Jose','Ramos','Santos','Electrician','Friend','Dr. Tan','2022-11-30',NULL),(44,2,'Andrea','Lopez','Reyes','1992-09-21','F','09171234567','andrea.reyes@example.com','45 Smile Corner','Barangay Dos','Tooth City','ProvinceB','Philippines','Chipped front tooth due to accident','Teacher','09334567890','Maria','Santos','Lopez','Nurse','Online Ad','Dr. Chan','2024-06-15',NULL),(45,2,'Marielle','','Modesto','2004-06-25','F','9876543222','marielle.modesto@gmail.com','123 mariellehouse','Barangay Dos','Manila','Metro Manila','Philippines','Tooth Extraction',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(46,1,'Eddielyn','Calano','Bautista','2005-02-09','F','9501055477','ejbautista0209@gmail.com','123 Mabuhay St.','Balara','Quezon City','Metro Manila','Philippines','Consultation',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL),(47,1,'sadssadads','dasadsa','dsadsad','2025-06-11','M','777-888-9996','bautistaeddielynjoy0209@gmail.com','ds','sdads','dsasaddsa','sdasd','Philippines','consultation',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `patient_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_medical_info`
--

DROP TABLE IF EXISTS `patient_medical_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient_medical_info` (
  `patient_id` int NOT NULL,
  `medical_info_image_link` text,
  `physician_name` varchar(255) DEFAULT NULL,
  `physician_specialty` varchar(255) DEFAULT NULL,
  `physician_office_address` text,
  `physician_office_number` varchar(15) DEFAULT NULL,
  `in_good_health` tinyint(1) DEFAULT NULL,
  `medical_treatment_currently_undergoing` text,
  `recent_illness_or_surgical_operation` text,
  `when_illness_or_operation` text,
  `when_why_hospitalized` text,
  `medications_currently_taking` text,
  `using_tabacco` tinyint(1) DEFAULT NULL,
  `using_alcohol_cocaine_drugs` tinyint(1) DEFAULT NULL,
  `allergies` text,
  `bleeding_time` varchar(20) DEFAULT NULL,
  `is_pregnant` tinyint(1) DEFAULT NULL,
  `is_nursing` tinyint(1) DEFAULT NULL,
  `on_birth_control` tinyint(1) DEFAULT NULL,
  `blood_type` varchar(20) DEFAULT NULL,
  `blood_pressure` varchar(20) DEFAULT NULL,
  `illness_checklist` text,
  PRIMARY KEY (`patient_id`),
  CONSTRAINT `patient_medical_info_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient_info` (`patient_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_medical_info`
--

LOCK TABLES `patient_medical_info` WRITE;
/*!40000 ALTER TABLE `patient_medical_info` DISABLE KEYS */;
INSERT INTO `patient_medical_info` VALUES (1,'','Dr. Enrique Santos','General Practitioner',NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,0,0,'',NULL,0,0,0,NULL,NULL,''),(2,'','Dr. Clara Navarro','Cardiologist','4th Floor, HeartCare Center, Makati','02-8822-4455',1,'Calcium supplements','None',NULL,NULL,'Calcium, Multivitamins',0,0,'Penicillin Antibiotics','Normal',0,0,1,'A+','110/70','Anemia'),(3,'','',NULL,NULL,NULL,1,'None','None',NULL,NULL,'None',1,0,'Aspirin','Normal',0,0,0,'B+','130/85','None'),(4,'','Dr. Aileen Ramos','Pediatrician','3rd Floor, Dental Hub, Quezon Avenue','02-8312-9988',1,'Iron supplements','None',NULL,NULL,'Iron',0,0,'None','Normal',0,0,1,'AB+','115/75','Thalassemia minor'),(26,NULL,'Dr. Miranda','General Practitioner',NULL,NULL,0,NULL,NULL,NULL,NULL,NULL,0,0,'',NULL,0,0,1,NULL,NULL,''),(27,NULL,'Dr. Santos','ENT Specialist','123 Clinic Corner','028800123',1,'None','Nasal Surgery','2022','Deviated septum correction','Antibiotics',0,0,'Dust','2 minutes',0,0,0,'B+','110/70','Asthma'),(28,NULL,'Dr. Javier','Internal Medicine','456 Medway Lane','028801112',1,'None','Gallbladder Removal','2020','Laparoscopic surgery','None',0,0,'Aspirin','1.8 minutes',0,0,1,'AB+','117/75','Diabetes'),(29,NULL,'Dr. Rivera','Family Medicine','12 Health St','028888456',1,'None','None','N/A','N/A','None',0,0,'Pollen','1.2 minutes',0,0,0,'B-','115/74','None'),(30,NULL,'Dr. Salazar','General Medicine','505 Clinic Park','028889999',1,'None','None','N/A','N/A','Vitamin B complex',0,0,'Shellfish','2.1 minutes',0,0,1,'O-','119/78','None'),(31,NULL,'Dr. Manalo','Cardiologist','99 Heartbeat Rd','028886123',1,'None','Bypass surgery','2019','Heart condition','Atenolol',0,0,'Latex','1.9 minutes',0,0,0,'A-','122/80','Hypertension'),(32,NULL,'Dr. Perez','Dermatologist','12 Skin Clinic Rd','028883456',1,'None','None','N/A','N/A','None',0,0,'Peanuts','1.4 minutes',0,0,1,'O+','116/72','None'),(33,NULL,'Dr. Rivera','Family Medicine','12 Health St','028888456',1,'None','None','N/A','N/A','None',0,0,'Pollen','1.2 minutes',0,0,0,'B-','115/74','None'),(34,NULL,'Dr. Austria','General Practitioner','456 Wellness Blvd','021223344',1,'None','None','N/A','N/A','Multivitamins',0,0,'None','1.8 minutes',0,0,0,'B+','117/79','None'),(35,NULL,'Dr. Sarmiento','Internist','23 Clinic Lane','029999123',1,'None','Appendectomy','2020','Appendix rupture','Pain relievers',0,0,'None','1.6 minutes',0,0,0,'A+','120/76','None'),(36,NULL,'Dr. Reyes','General Practitioner','101 Checkup Rd','021234567',1,'None','None','N/A','N/A','Calcium supplements',0,0,'Strawberries','1.5 minutes',0,0,1,'AB+','115/70','None'),(37,NULL,'Dr. Go','Orthopedist','9 Balance Clinic','029334455',1,'None','Knee surgery','2022','Accident recovery','Pain relievers',0,0,'None','2.0 minutes',0,0,0,'B-','118/75','None'),(39,NULL,'Dr. Rivera','Cardiologist','102 Wellness Blvd','029887766',1,'None','None','N/A','N/A','None',0,0,'Penicillin','1.7 minutes',0,0,0,'O-','119/75','None'),(40,NULL,'Dr. Yu','ENT Specialist','5 Health St','028765432',1,'None','None','N/A','N/A','Vitamin C',0,0,'None','1.3 minutes',0,0,0,'B+','112/70','None'),(41,NULL,'Dr. Manuel Reyes','Internal Medicine','75 General Health St.','028880001',1,'Hypertension management','Appendectomy','2023-03','Appendix removal','Amlodipine',0,0,'None','2.5 minutes',0,0,0,'A+','125/82','Hypertension'),(44,NULL,'Dr. Anna Cruz','Family Medicine','88 Care Street','028812345',1,'None','Gallbladder removal','2022-10','Cholecystectomy','Multivitamins',0,0,'Amoxicillin','2 minutes',0,0,1,'B+','118/76','None');
/*!40000 ALTER TABLE `patient_medical_info` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `procedure_history`
--

DROP TABLE IF EXISTS `procedure_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `procedure_history` (
  `procedure_id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `appointment_id` int DEFAULT NULL,
  `Procedure_date` date NOT NULL,
  `treatment_procedure` varchar(255) NOT NULL,
  `tooth_area` varchar(10) NOT NULL,
  `provider` varchar(255) NOT NULL,
  `treatment_plan` text,
  `fee` int NOT NULL,
  `procedure_status` varchar(255) DEFAULT NULL,
  `notes` text,
  PRIMARY KEY (`procedure_id`),
  KEY `patient_id` (`patient_id`),
  KEY `fk_procedure_appointment` (`appointment_id`),
  CONSTRAINT `fk_procedure_appointment` FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`appointment_id`) ON DELETE SET NULL,
  CONSTRAINT `procedure_history_appointment_id_fkey` FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`appointment_id`) ON DELETE CASCADE,
  CONSTRAINT `procedure_history_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient_info` (`patient_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `procedure_history`
--

LOCK TABLES `procedure_history` WRITE;
/*!40000 ALTER TABLE `procedure_history` DISABLE KEYS */;
INSERT INTO `procedure_history` VALUES (1,1,1,'2024-01-15','Tooth Extraction','28','Dr. Reyes','Remove decayed upper right wisdom tooth',1500,'Completed','Procedure completed without complications'),(2,1,2,'2024-03-10','Oral Prophylaxis','Full','Dr. Reyes','Routine cleaning and polish',800,'Completed','Advised 6-month follow-up'),(3,2,3,'2024-02-25','Dental Filling','14','Dr. Santos','Composite filling due to cavity',1200,'Completed','Patient felt sensitivity post-procedure'),(4,3,4,'2024-04-12','Root Canal Therapy','36','Dr. Tan','RCT due to pulp infection, 3-session plan',4500,'Ongoing','Session 1 completed; next in 2 weeks'),(5,3,5,'2024-05-05','Temporary Crown Placement','36','Dr. Tan','Placed temporary crown after RCT',2000,'Completed','Permanent crown scheduled next month'),(6,4,6,'2024-01-10','Orthodontic Consultation','Full','Dr. Garcia','Assessment for braces. Took impressions and X-rays.',0,'Completed','Braces recommended; patient agreed to start treatment'),(7,4,7,'2024-02-05','Braces Installation','Full','Dr. Garcia','Installed metal braces. Discussed oral care and monthly visits.',45000,'Ongoing','Patient tolerated procedure well'),(8,4,8,'2024-03-05','Braces Adjustment','Full','Dr. Garcia','Tightened brackets, replaced elastic bands.',0,'Completed','Minor discomfort reported'),(9,4,9,'2024-04-05','Braces Adjustment','Full','Dr. Garcia','Adjusted archwire, checked teeth movement progress.',0,'Completed','Slight improvement in alignment observed'),(10,4,10,'2024-05-04','Braces Adjustment','Full','Dr. Garcia','Replaced wires and elastics, minor repositioning done.',0,'Completed','Patient doing well with hygiene'),(11,4,11,'2024-06-05','Braces Adjustment','Full','Dr. Garcia','Final monthly adjustment for phase 1. Scheduled retainer fitting.',0,'Completed','Brackets to be removed next session'),(40,26,44,'2024-07-10','Scaling and Polishing','Upper Arch','Dr. Ortega','Review in 6 months',1200,'Completed','Tartar buildup removed successfully'),(41,27,45,'2025-03-15','Wisdom Tooth Extraction','32','Dr. Mendoza','Soft diet 3 days, pain meds prescribed',2500,'Completed','Extraction successful with minimal bleeding'),(42,28,46,'2025-05-22','Tooth Filling Replacement','14','Dr. Tan','Monitor sensitivity, avoid sweets for 2 weeks',1800,'Completed','Silver filling replaced with composite resin'),(43,29,47,'2025-04-12','Composite Bonding','11','Dr. Cruz','Avoid hard food for 1 week',2000,'Completed','Small chip repaired with bonding resin'),(44,30,48,'2025-06-18','Tooth Filling - Composite Resin','30','Dr. Velasquez','Re-evaluate in 1 month',1700,'Completed','Deep cavity restored successfully'),(54,39,58,'2025-01-18','Composite Filling','26','Dr. Beltran','Observe for any post-op sensitivity',1500,'Completed','Cavity cleaned and filled with composite resin'),(56,40,60,'2025-07-05','Tooth Filling','36','Dr. Garcia','Monitor sensitivity, avoid sweets for 2 weeks',1800,'completed','Recorded via modal'),(60,41,61,'2025-07-04','Root Canal Therapy','14','Dr. Lopez','Crown placement in next visit',5500,'Completed','Cleaned and sealed root canals'),(61,45,64,'2025-07-05','Tooth Extraction','12','Dr. Garcia','Tooth Extracted at 12',1000,'completed','Recorded via modal'),(62,46,65,'2025-07-05','Brace ','Full','Dr. Garcia','Braces',45000,'completed','Recorded via modal');
/*!40000 ALTER TABLE `procedure_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transactions`
--

DROP TABLE IF EXISTS `transactions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transactions` (
  `transaction_id` int NOT NULL AUTO_INCREMENT,
  `procedure_id` int DEFAULT NULL,
  `receipt_number` varchar(100) NOT NULL,
  `payment_method` enum('Cash','Card','GCash','Maya','Insurance','Other') NOT NULL,
  `transaction_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dentist_name` varchar(255) NOT NULL,
  `service_detail` text NOT NULL,
  `total_amount_paid` decimal(10,2) NOT NULL,
  `transaction_image_link` text,
  PRIMARY KEY (`transaction_id`),
  KEY `procedure_id` (`procedure_id`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`procedure_id`) REFERENCES `procedure_history` (`procedure_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,1,'RCPT-1001','Cash','2024-01-15 00:00:00','Dr. Reyes','Tooth Extraction',1500.00,NULL),(2,2,'RCPT-1002','Cash','2024-03-10 00:00:00','Dr. Reyes','Oral Prophylaxis',800.00,NULL),(3,3,'RCPT-1003','Cash','2025-07-01 00:00:00','Dr. Santos','Dental Filling',1209.00,NULL),(4,4,'RCPT-1004','Cash','2024-04-12 00:00:00','Dr. Tan','Root Canal Therapy (Session 1)',4500.00,NULL),(5,5,'RCPT-1005','Cash','2024-05-05 00:00:00','Dr. Tan','Temporary Crown Placement',2000.00,NULL),(6,6,'RCPT-1006','Cash','2024-01-10 00:00:00','Dr. Garcia','Orthodontic Consultation',0.00,NULL),(7,7,'RCPT-1007','Cash','2024-02-05 00:00:00','Dr. Garcia','Braces Installation',10000.00,NULL),(8,8,'RCPT-1008','Cash','2024-03-05 00:00:00','Dr. Garcia','Braces Adjustment (Month 1)',1500.00,NULL),(9,9,'RCPT-1009','Cash','2024-04-05 00:00:00','Dr. Garcia','Braces Adjustment (Month 2)',1500.00,NULL),(10,10,'RCPT-1010','Cash','2024-05-05 00:00:00','Dr. Garcia','Braces Adjustment (Month 3)',1500.00,NULL),(11,11,'RCPT-1011','Cash','2025-07-01 00:00:00','Dr. Garcia','Braces Adjustment (Month 4)',1500.00,NULL),(18,40,'RCPT-000012','Card','2024-07-10 09:30:00','Dr. Ortega','Scaling and Polishing - Upper Arch',1200.00,NULL),(20,41,'RCPT-000013','GCash','2025-03-15 14:45:00','Dr. Mendoza','Wisdom Tooth Extraction - Tooth 32',2500.00,NULL),(21,42,'RCPT-000014','Cash','2025-05-22 14:15:00','Dr. Tan','Tooth Filling Replacement - Tooth 14',1800.00,NULL),(22,43,'RCPT-000015','Card','2025-04-12 15:30:00','Dr. Cruz','Composite Bonding - Tooth 11',2000.00,NULL),(23,44,'RCPT-000016','Cash','2025-06-18 10:40:00','Dr. Velasquez','Tooth Filling - Tooth 30',1700.00,NULL),(33,54,'RCPT-000026','Cash','2025-01-18 14:10:00','Dr. Beltran','Composite Filling - Tooth 26',1500.00,NULL),(34,56,'AUTO-20250705015519','Card','2025-02-14 11:00:00','Dr. Garcia','Tooth Filling',1800.00,NULL),(36,60,'RCPT-000017','GCash','2025-07-04 12:15:00','Dr. Lopez','Root Canal Therapy - Tooth 14',5500.00,NULL),(37,60,'RCPT-000018','Cash','2025-07-05 11:00:00','Dr. Tan','Cosmetic Bonding - Tooth 11',3000.00,NULL),(38,61,'AUTO-20250705105657','Cash','2025-07-05 10:56:57','Dr. Garcia','Tooth Extraction',1000.00,NULL),(39,62,'AUTO-20250705130248','Cash','2025-07-05 13:02:48','Dr. Garcia','Brace ',1000.00,NULL);
/*!40000 ALTER TABLE `transactions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-07-14 15:39:08
