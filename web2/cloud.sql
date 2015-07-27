-- MySQL dump 10.13  Distrib 5.5.43, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: cloud
-- ------------------------------------------------------
-- Server version	5.5.43-0ubuntu0.14.04.2

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
-- Table structure for table `u_cluster`
--

DROP TABLE IF EXISTS `u_cluster`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `u_cluster` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `uid` int(20) NOT NULL,
  `name` char(255) NOT NULL,
  `type` char(255) NOT NULL,
  `desc` text NOT NULL,
  `status` char(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `u_cluster`
--

LOCK TABLES `u_cluster` WRITE;
/*!40000 ALTER TABLE `u_cluster` DISABLE KEYS */;
INSERT INTO `u_cluster` VALUES (11,1,'Unknown','HS','W3siaW5faXBhZGRyIjogIjEwLjAuOTguMTc2IiwgIm5hbWUiOiAiaGFkb29wMDYiLCAicm9sZXMiOiBudWxsLCAidW5hbWUiOiAidWJ1bnR1IiwgImtleXMiOiAiaGFkb29wX21hc3RlciIsICJob3N0bmFtZSI6ICJoYWRvb3AwNi52ZG9tYWluLmNvbSIsICJleF9pcGFkZHIiOiAiIiwgInBhc3N3ZCI6ICIxMjM0NTYiLCAib3MiOiAiVTE0MDQiLCAiaWQiOiAxMSwgInVpZCI6IDF9LCB7ImluX2lwYWRkciI6ICIxMC4wLjk4LjE3OCIsICJuYW1lIjogImhhZG9vcDA4IiwgInJvbGVzIjogbnVsbCwgInVuYW1lIjogInVidW50dSIsICJrZXlzIjogImhhZG9vcF9zbGF2ZSIsICJob3N0bmFtZSI6ICJoYWRvb3AwOC52ZG9tYWluLmNvbSIsICJleF9pcGFkZHIiOiAiIiwgInBhc3N3ZCI6ICIxMjM0NTYiLCAib3MiOiAiVTE0MDQiLCAiaWQiOiAxMywgInVpZCI6IDF9LCB7ImluX2lwYWRkciI6ICIxMC4wLjk4LjE3NyIsICJuYW1lIjogImhhZG9vcDA3IiwgInJvbGVzIjogbnVsbCwgInVuYW1lIjogInVidW50dSIsICJrZXlzIjogImhhZG9vcF9zbGF2ZSxzcGFya19jbGllbnQiLCAiaG9zdG5hbWUiOiAiaGFkb29wMDcudmRvbWFpbi5jb20iLCAiZXhfaXBhZGRyIjogIiIsICJwYXNzd2QiOiAiMTIzNDU2IiwgIm9zIjogIlUxNDA0IiwgImlkIjogMTIsICJ1aWQiOiAxfV0=','R');
/*!40000 ALTER TABLE `u_cluster` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `u_machine`
--

DROP TABLE IF EXISTS `u_machine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `u_machine` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `uid` int(20) NOT NULL,
  `name` char(255) NOT NULL,
  `in_ipaddr` char(15) NOT NULL,
  `ex_ipaddr` char(15) DEFAULT NULL,
  `hostname` char(255) NOT NULL,
  `os` char(255) NOT NULL,
  `uname` char(255) NOT NULL,
  `passwd` char(255) NOT NULL,
  `roles` char(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `u_machine`
--

LOCK TABLES `u_machine` WRITE;
/*!40000 ALTER TABLE `u_machine` DISABLE KEYS */;
INSERT INTO `u_machine` VALUES (11,1,'hadoop06','10.0.98.176','','hadoop06.vdomain.com','U1404','ubuntu','123456',NULL),(12,1,'hadoop07','10.0.98.177','','hadoop07.vdomain.com','U1404','ubuntu','123456',NULL),(13,1,'hadoop08','10.0.98.178','','hadoop08.vdomain.com','U1404','ubuntu','123456',NULL);
/*!40000 ALTER TABLE `u_machine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `u_tasks`
--

DROP TABLE IF EXISTS `u_tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `u_tasks` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `uid` int(20) NOT NULL,
  `status` int(20) NOT NULL,
  `command` char(255) NOT NULL,
  `date` datetime NOT NULL,
  `logfile` char(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `u_tasks`
--

LOCK TABLES `u_tasks` WRITE;
/*!40000 ALTER TABLE `u_tasks` DISABLE KEYS */;
/*!40000 ALTER TABLE `u_tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `u_user`
--

DROP TABLE IF EXISTS `u_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `u_user` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `name` char(255) NOT NULL,
  `uname` char(255) NOT NULL,
  `passwd` char(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `u_user`
--

LOCK TABLES `u_user` WRITE;
/*!40000 ALTER TABLE `u_user` DISABLE KEYS */;
INSERT INTO `u_user` VALUES (1,'admin','admin','123456');
/*!40000 ALTER TABLE `u_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-07-24  5:31:47
