-- MySQL dump 10.13  Distrib 5.5.40, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: POS
-- ------------------------------------------------------
-- Server version	5.5.40-0ubuntu0.14.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Taxes`
--

DROP TABLE IF EXISTS `Taxes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Taxes` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `Taxe` varchar(100) DEFAULT NULL,
  `Description` varchar(100) DEFAULT NULL,
  `Rate` decimal(6,5) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Taxes`
--

LOCK TABLES `Taxes` WRITE;
/*!40000 ALTER TABLE `Taxes` DISABLE KEYS */;
INSERT INTO `Taxes` VALUES (2,'TVQ','9876543210',9.97500),(6,'TPS','0123456789',5.00000);
/*!40000 ALTER TABLE `Taxes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Technicien`
--

DROP TABLE IF EXISTS `Technicien`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Technicien` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `Prenom` varchar(100) NOT NULL,
  `Nom` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Username` varchar(100) NOT NULL,
  `Password` varchar(200) NOT NULL,
  `levelID` smallint(1) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Username` (`Username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Technicien`
--

LOCK TABLES `Technicien` WRITE;
/*!40000 ALTER TABLE `Technicien` DISABLE KEYS */;
INSERT INTO `Technicien` VALUES (1,'Martin','Verret','verret.martin@gmail.com','mverret','a92009999015bfc5b8aa4a4008dd846abbd9ca3331f31b0d50cf1aa81f8dbc2db5dd5f27b496423bd5dceabeae8f4df5aee1b2135bbe7bde69b120d909421a634c89da00bea87698ce4561116f6dc21fcbedcc9509',3);
/*!40000 ALTER TABLE `Technicien` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `adminLevel`
--

DROP TABLE IF EXISTS `adminLevel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `adminLevel` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `levelName` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `adminLevel`
--

LOCK TABLES `adminLevel` WRITE;
/*!40000 ALTER TABLE `adminLevel` DISABLE KEYS */;
INSERT INTO `adminLevel` VALUES (1,'user'),(2,'Manager'),(3,'Admin');
/*!40000 ALTER TABLE `adminLevel` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `groupTaxe`
--

DROP TABLE IF EXISTS `groupTaxe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `groupTaxe` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `groupName` varchar(100) DEFAULT NULL,
  `cascadeBOOL` int(10) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `groupTaxe`
--

LOCK TABLES `groupTaxe` WRITE;
/*!40000 ALTER TABLE `groupTaxe` DISABLE KEYS */;
INSERT INTO `groupTaxe` VALUES (3,'Quebec',1);
/*!40000 ALTER TABLE `groupTaxe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `shopInfo`
--

DROP TABLE IF EXISTS `shopInfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `shopInfo` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `buisnessName` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `postalCode` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `prov` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `shopInfo`
--

LOCK TABLES `shopInfo` WRITE;
/*!40000 ALTER TABLE `shopInfo` DISABLE KEYS */;
/*!40000 ALTER TABLE `shopInfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `storeData`
--

DROP TABLE IF EXISTS `storeData`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `storeData` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `storeName` varchar(100) DEFAULT NULL,
  `storeAddress` varchar(100) DEFAULT NULL,
  `storePostalCode` varchar(100) DEFAULT NULL,
  `storeCity` varchar(100) DEFAULT NULL,
  `storeProvince` varchar(100) DEFAULT NULL,
  `storePhone` varchar(100) DEFAULT NULL,
  `storeEmail` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `storeData`
--

LOCK TABLES `storeData` WRITE;
/*!40000 ALTER TABLE `storeData` DISABLE KEYS */;
INSERT INTO `storeData` VALUES (1,'Martin-Formatique','PRIVATE','PRIVATE','PRIVATE','PRIVATE','PRIVATE','PRIVATE');
/*!40000 ALTER TABLE `storeData` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sysConfig`
--

DROP TABLE IF EXISTS `sysConfig`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sysConfig` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `language` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sysConfig`
--

LOCK TABLES `sysConfig` WRITE;
/*!40000 ALTER TABLE `sysConfig` DISABLE KEYS */;
INSERT INTO `sysConfig` VALUES (1,'frCA');
/*!40000 ALTER TABLE `sysConfig` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `taxesGroupTaxe`
--

DROP TABLE IF EXISTS `taxesGroupTaxe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `taxesGroupTaxe` (
  `ID` int(10) NOT NULL AUTO_INCREMENT,
  `TaxesID` int(10) DEFAULT NULL,
  `groupTaxeID` int(10) DEFAULT NULL,
  `priority` int(10) DEFAULT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `taxesGroupTaxe`
--

LOCK TABLES `taxesGroupTaxe` WRITE;
/*!40000 ALTER TABLE `taxesGroupTaxe` DISABLE KEYS */;
INSERT INTO `taxesGroupTaxe` VALUES (1,2,3,2),(2,6,3,1);
/*!40000 ALTER TABLE `taxesGroupTaxe` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'POS'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-02-05 16:02:10
