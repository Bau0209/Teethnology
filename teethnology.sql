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
  KEY `employee_id` (`employee_id`),
  CONSTRAINT `accounts_ibfk_1` FOREIGN KEY (`employee_id`) REFERENCES `employees` (`employee_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts`
--

LOCK TABLES `accounts` WRITE;
/*!40000 ALTER TABLE `accounts` DISABLE KEYS */;
INSERT INTO `accounts` VALUES (1,1,'john.doe@example.com','securepassword123','owner','active');
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
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (1,1,1,0,'2024-01-15 09:00:00',NULL,'Tooth Extraction','approved','2024-01-10 08:00:00','2024-01-12 14:00:00','Dr. Reyes'),(2,1,1,1,'2024-03-10 10:30:00',NULL,'Oral Prophylaxis','approved','2024-03-05 11:00:00','2024-03-07 09:00:00','Dr. Reyes'),(3,1,2,0,'2024-02-25 11:00:00',NULL,'Dental Filling','approved','2024-02-20 13:00:00','2024-02-22 10:00:00','Dr. Santos'),(4,2,3,0,'2024-04-12 14:00:00',NULL,'Root Canal Therapy (Session 1)','approved','2024-04-07 09:30:00','2024-04-10 16:00:00','Dr. Tan'),(5,2,3,1,'2024-05-05 10:00:00',NULL,'Temporary Crown Placement','approved','2024-05-01 12:00:00','2024-05-03 14:00:00','Dr. Tan'),(6,2,4,0,'2024-01-10 09:00:00',NULL,'Orthodontic Consultation','approved','2024-01-05 08:00:00','2024-01-08 12:00:00','Dr. Garcia'),(7,2,4,1,'2024-02-05 10:00:00',NULL,'Braces Installation','approved','2024-01-30 13:00:00','2024-02-02 15:00:00','Dr. Garcia'),(8,2,4,1,'2024-03-05 10:00:00',NULL,'Braces Adjustment (Month 1)','approved','2024-03-01 09:30:00','2024-03-03 16:00:00','Dr. Garcia'),(9,2,4,1,'2024-04-05 10:00:00',NULL,'Braces Adjustment (Month 2)','approved','2024-04-01 11:00:00','2024-04-03 13:00:00','Dr. Garcia'),(10,2,4,1,'2024-05-05 10:00:00',NULL,'Braces Adjustment (Month 3)','approved','2024-05-01 11:00:00','2024-05-03 13:00:00','Dr. Garcia'),(11,2,4,1,'2024-06-05 10:00:00',NULL,'Braces Adjustment (Month 4)','approved','2024-06-01 11:00:00','2024-06-03 13:00:00','Dr. Garcia'),(12,1,5,0,'2025-07-30 16:00:00','2025-07-30 18:00:00','Tooth Extraction','pending','2025-07-01 14:28:01',NULL,NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `branch`
--

LOCK TABLES `branch` WRITE;
/*!40000 ALTER TABLE `branch` DISABLE KEYS */;
INSERT INTO `branch` VALUES (1,'Manila','123 Main St, Manila City','A modern dental clinic offering general and cosmetic services.','Dr. Anna Cruz','09171234567','08:00:00','17:00:00','Cleaning, Whitening, Braces'),(2,'Quezon City','123 Main St, Quezon City','A modern dental clinic offering general and cosmetic services.','Dr. Juan Cruz','09181334435','08:00:00','18:00:00','Cleaning, Whitening, Braces');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clinic_branch_images`
--

LOCK TABLES `clinic_branch_images` WRITE;
/*!40000 ALTER TABLE `clinic_branch_images` DISABLE KEYS */;
INSERT INTO `clinic_branch_images` VALUES (1,'uploads/branches/manila1.jpg',1),(2,'uploads/branches/quezoncity1.jpg',2);
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dental_record`
--

LOCK TABLES `dental_record` WRITE;
/*!40000 ALTER TABLE `dental_record` DISABLE KEYS */;
INSERT INTO `dental_record` VALUES (6,1,'uploads/patients_record/11.png','Gingivitis, Early Periodontitis','Class (Molar), Overjet Overbite','Orthodontic','Clicking, Clenching'),(7,2,'uploads/patients_record/21.png','Moderate Periodontitis','Midline Deviation, Crossbite','Stayplate','None'),(8,3,'uploads/patients_record/31.png','Advanced Periodontitis','Class (Molar), Midline Deviation, Overjet Overbite','Orthodontic, Stayplate','Trismus, Muscle Spasm'),(9,4,'uploads/patients_record/41.png','Gingivitis','None','None','None');
/*!40000 ALTER TABLE `dental_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employees`
--

DROP TABLE IF EXISTS `employees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employees` (
  `employee_id` int NOT NULL,
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employees`
--

LOCK TABLES `employees` WRITE;
/*!40000 ALTER TABLE `employees` DISABLE KEYS */;
INSERT INTO `employees` VALUES (1,1,'John','A.','Doe','1990-05-15','m','09171234567','john.doe@example.com','active','2024-01-10','Owner','Dental','PRC1234567','Monday, Wednesday, Friday','08:00 AM - 05:00 PM'),(2,2,'Sam','B.','Versoza','1990-06-15','f','09472834','sam.versoza@gmail.com','active','2024-01-10','Dentist','Dental','PRC1234568','Monday, Wednesday, Friday','08:00 AM - 06:00 PM');
/*!40000 ALTER TABLE `employees` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_info`
--

LOCK TABLES `patient_info` WRITE;
/*!40000 ALTER TABLE `patient_info` DISABLE KEYS */;
INSERT INTO `patient_info` VALUES (1,1,'Juan','Santos','Dela Cruz','1990-05-15','M','09171234567','juan.dc@example.com','123 Mabuhay St.','Barangay Uno','Manila','Metro Manila','Philippines','Dentures','Engineer','02-1234567',NULL,NULL,NULL,NULL,'Friend','Dr. Reyes','2023-07-01',NULL),(2,1,'Maria','Luisa','Reyes','1985-08-22','F','09179876543','maria.reyes@example.com','456 Maligaya Ave.','Barangay Dos','Manila','Metro Manila','Philippines','Braces','Teacher','02-7654321','Lola','Cruz','Reyes','Retired','','None',NULL,NULL),(3,2,'Carlos','David','Santos','1992-02-10','M','09172345678','carlos.santos@example.com','789 Payapa Blvd.','Barangay Tres','Quezon City','Metro Manila','Philippines','Tooth ache','Designer','02-5566778',NULL,NULL,NULL,NULL,'Online Ad','Dr. Tan','2022-12-15',NULL),(4,2,'Angela','Marie','Lopez','1996-11-05','F','09173456789','angela.lopez@example.com','321 Tahimik Lane','Barangay Cuatro','Quezon City','Metro Manila','Philippines','Tooth ache','Student',NULL,'Anna','Grace','Lopez','Nurse','School','None',NULL,NULL),(5,1,'Eddielyn Joy','Calano','Bautista','2004-02-09','F','09501055477','ejbautista0209@gmail.com','129 Hello lane','Baranggay 567','Pasay City','Metro Manila','Philippines','Tooth ache','',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL);
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
  `when_illness_or_operation` date DEFAULT NULL,
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
INSERT INTO `patient_medical_info` VALUES (1,'','Dr. Enrique Santos','General Practitioner','Unit 5, HealthLink Building, Manila City','02-8991-2345',1,'None','Appendectomy','2019-08-12','Hospitalized for appendicitis','Vitamin D supplements',0,0,'None','Normal',0,0,0,'O+','120/80','Diabetes, Hypertension'),(2,'','Dr. Clara Navarro','Cardiologist','4th Floor, HeartCare Center, Makati','02-8822-4455',1,'Calcium supplements','None',NULL,NULL,'Calcium, Multivitamins',0,0,'Penicillin Antibiotics','Normal',0,0,1,'A+','110/70','Anemia'),(3,'','',NULL,NULL,NULL,1,'None','None',NULL,NULL,'None',1,0,'Aspirin','Normal',0,0,0,'B+','130/85','None'),(4,'','Dr. Aileen Ramos','Pediatrician','3rd Floor, Dental Hub, Quezon Avenue','02-8312-9988',1,'Iron supplements','None',NULL,NULL,'Iron',0,0,'None','Normal',0,0,1,'AB+','115/75','Thalassemia minor');
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
  CONSTRAINT `procedure_history_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient_info` (`patient_id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `procedure_history`
--

LOCK TABLES `procedure_history` WRITE;
/*!40000 ALTER TABLE `procedure_history` DISABLE KEYS */;
INSERT INTO `procedure_history` VALUES (1,1,'2024-01-15','Tooth Extraction','28','Dr. Reyes','Remove decayed upper right wisdom tooth',1500,'Completed','Procedure completed without complications'),(2,1,'2024-03-10','Oral Prophylaxis','Full','Dr. Reyes','Routine cleaning and polish',800,'Completed','Advised 6-month follow-up'),(3,2,'2024-02-25','Dental Filling','14','Dr. Santos','Composite filling due to cavity',1200,'Completed','Patient felt sensitivity post-procedure'),(4,3,'2024-04-12','Root Canal Therapy','36','Dr. Tan','RCT due to pulp infection, 3-session plan',4500,'Ongoing','Session 1 completed; next in 2 weeks'),(5,3,'2024-05-05','Temporary Crown Placement','36','Dr. Tan','Placed temporary crown after RCT',2000,'Completed','Permanent crown scheduled next month'),(6,4,'2024-01-10','Orthodontic Consultation','Full','Dr. Garcia','Assessment for braces. Took impressions and X-rays.',0,'Completed','Braces recommended; patient agreed to start treatment'),(7,4,'2024-02-05','Braces Installation','Full','Dr. Garcia','Installed metal braces. Discussed oral care and monthly visits.',45000,'Ongoing','Patient tolerated procedure well'),(8,4,'2024-03-05','Braces Adjustment','Full','Dr. Garcia','Tightened brackets, replaced elastic bands.',0,'Completed','Minor discomfort reported'),(9,4,'2024-04-05','Braces Adjustment','Full','Dr. Garcia','Adjusted archwire, checked teeth movement progress.',0,'Completed','Slight improvement in alignment observed'),(10,4,'2024-05-05','Braces Adjustment','Full','Dr. Garcia','Replaced wires and elastics, minor repositioning done.',0,'Completed','Patient doing well with hygiene'),(11,4,'2024-06-05','Braces Adjustment','Full','Dr. Garcia','Final monthly adjustment for phase 1. Scheduled retainer fitting.',0,'Completed','Brackets to be removed next session');
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
  `receipt_number` varchar(100) NOT NULL,
  `payment_method` enum('Cash','Card','GCash','Maya','Insurance','Other') NOT NULL,
  `transaction_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `dentist_name` varchar(255) NOT NULL,
  `service_detail` text NOT NULL,
  `total_amount_paid` decimal(10,2) NOT NULL,
  `transaction_image_link` text,
  `procedure_id` int DEFAULT NULL,
  PRIMARY KEY (`transaction_id`),
  KEY `procedure_id` (`procedure_id`),
  CONSTRAINT `transactions_ibfk_1` FOREIGN KEY (`procedure_id`) REFERENCES `procedure_history` (`procedure_id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transactions`
--

LOCK TABLES `transactions` WRITE;
/*!40000 ALTER TABLE `transactions` DISABLE KEYS */;
INSERT INTO `transactions` VALUES (1,'RCPT-1001','Cash','2024-01-15 00:00:00','Dr. Reyes','Tooth Extraction',1500.00,NULL,1),(2,'RCPT-1002','Cash','2024-03-10 00:00:00','Dr. Reyes','Oral Prophylaxis',800.00,NULL,2),(3,'RCPT-1003','Cash','2025-07-01 00:00:00','Dr. Santos','Dental Filling',1200.00,NULL,3),(4,'RCPT-1004','Cash','2024-04-12 00:00:00','Dr. Tan','Root Canal Therapy (Session 1)',4500.00,NULL,4),(5,'RCPT-1005','Cash','2024-05-05 00:00:00','Dr. Tan','Temporary Crown Placement',2000.00,NULL,5),(6,'RCPT-1006','Cash','2024-01-10 00:00:00','Dr. Garcia','Orthodontic Consultation',0.00,NULL,6),(7,'RCPT-1007','Cash','2024-02-05 00:00:00','Dr. Garcia','Braces Installation',10000.00,NULL,7),(8,'RCPT-1008','Cash','2024-03-05 00:00:00','Dr. Garcia','Braces Adjustment (Month 1)',1500.00,NULL,8),(9,'RCPT-1009','Cash','2024-04-05 00:00:00','Dr. Garcia','Braces Adjustment (Month 2)',1500.00,NULL,9),(10,'RCPT-1010','Cash','2024-05-05 00:00:00','Dr. Garcia','Braces Adjustment (Month 3)',1500.00,NULL,10),(11,'RCPT-1011','Cash','2025-07-01 00:00:00','Dr. Garcia','Braces Adjustment (Month 4)',1500.00,NULL,11);
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

-- Dump completed on 2025-07-01 23:10:13
