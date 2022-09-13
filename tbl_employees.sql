-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Sep 13, 2022 at 05:52 PM
-- Server version: 5.7.36
-- PHP Version: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `employees`
--

-- --------------------------------------------------------

--
-- Table structure for table `tbl_employees`
--

DROP TABLE IF EXISTS `tbl_employees`;
CREATE TABLE IF NOT EXISTS `tbl_employees` (
  `ID` smallint(6) NOT NULL AUTO_INCREMENT,
  `First_Name` varchar(50) NOT NULL,
  `Family_Name` varchar(50) NOT NULL,
  `Job_Title` varchar(20) NOT NULL,
  `Photo` varchar(20) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tbl_employees`
--

INSERT INTO `tbl_employees` (`ID`, `First_Name`, `Family_Name`, `Job_Title`, `Photo`) VALUES
(1, 'David', 'Khan', 'Programmer', '1.png'),
(7, 'Davina', 'Hope', 'Programmer', '3.png'),
(6, 'MIke', 'Singh', 'System Analyst', '2.png'),
(8, 'Anaya', 'Hanson', 'IT Manager', ''),
(11, 'Mary', 'Mary', 'Programmer', '');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
