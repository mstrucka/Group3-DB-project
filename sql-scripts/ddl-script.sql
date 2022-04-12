-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 ;
USE `mydb` ;

-- -----------------------------------------------------
-- Table `mydb`.`Users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `firstName` VARCHAR(45) NOT NULL,
  `lastName` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password_hash` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NULL DEFAULT NULL,
  `headline` VARCHAR(45) NULL DEFAULT NULL,
  `school` VARCHAR(45) NULL DEFAULT NULL,
  `education` VARCHAR(45) NULL DEFAULT NULL,
  `is_student` BIT(1) NOT NULL,
  `dob` DATE NOT NULL,
  PRIMARY KEY (`id`, `firstName`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`Courses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Courses` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `description` VARCHAR(500) NULL DEFAULT NULL,
  `level` INT NOT NULL,
  `price` DECIMAL(10,0) NOT NULL,
  `platform_sale` TINYINT(1) NULL DEFAULT NULL,
  `category` VARCHAR(45) NOT NULL,
  `lecturer` INT NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  INDEX `lecturer_id_idx` (`lecturer` ASC) VISIBLE,
  INDEX `course_title_price_idx` (`title` DESC, `price` DESC) VISIBLE,
  INDEX `course_category_idx` (`category` ASC) VISIBLE,
  CONSTRAINT `lecturer_id`
    FOREIGN KEY (`lecturer`)
    REFERENCES `mydb`.`Users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`Lectures`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Lectures` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NOT NULL,
  `description` VARCHAR(45) NULL DEFAULT NULL,
  `index` TINYINT(1) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`Course_lectures`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Course_lectures` (
  `course_id` INT NOT NULL,
  `lecture_id` INT NOT NULL,
  PRIMARY KEY (`course_id`, `lecture_id`),
  INDEX `lecture_id_idx` (`lecture_id` ASC) VISIBLE,
  INDEX `course_id_idx` (`course_id` ASC) VISIBLE,
  CONSTRAINT `course_id`
    FOREIGN KEY (`course_id`)
    REFERENCES `mydb`.`Courses` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `course_lecture_id`
    FOREIGN KEY (`lecture_id`)
    REFERENCES `mydb`.`Lectures` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`Courses_of_the_day`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Courses_of_the_day` (
  `course_id` INT NOT NULL,
  `date` DATE NOT NULL,
  PRIMARY KEY (`course_id`, `date`),
  CONSTRAINT `course_course_of_day`
    FOREIGN KEY (`course_id`)
    REFERENCES `mydb`.`Courses` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`Payments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Payments` (
  `id` INT NOT NULL,
  `date` DATETIME NULL DEFAULT NULL,
  `is_refund` BIT(1) NULL DEFAULT NULL,
  `total` DECIMAL(10,0) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`Enrollments`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Enrollments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `student_id` INT NOT NULL,
  `course_id` INT NOT NULL,
  `payment_id` INT NULL,
  `finished` BIT(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  INDEX `enrollment_course_idx` (`course_id` ASC) VISIBLE,
  INDEX `enrollment_payment_idx` (`payment_id` ASC) VISIBLE,
  CONSTRAINT `enrollment_course`
    FOREIGN KEY (`course_id`)
    REFERENCES `mydb`.`Courses` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `enrollment_student`
    FOREIGN KEY (`student_id`)
    REFERENCES `mydb`.`Users` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `enrollment_payment`
    FOREIGN KEY (`payment_id`)
    REFERENCES `mydb`.`Payments` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`Resources`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Resources` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `type` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `uri` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`Lecture_resources`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Lecture_resources` (
  `resource_id` INT NOT NULL,
  `lecture_id` INT NOT NULL,
  PRIMARY KEY (`resource_id`, `lecture_id`),
  INDEX `lecture_id_idx` (`lecture_id` ASC) VISIBLE,
  INDEX `resource_id_idx` (`resource_id` ASC) VISIBLE,
  CONSTRAINT `resource_id`
    FOREIGN KEY (`resource_id`)
    REFERENCES `mydb`.`Resources` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `resource_lecture_id`
    FOREIGN KEY (`lecture_id`)
    REFERENCES `mydb`.`Lectures` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `mydb`.`Course_progresses`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `mydb`.`Course_progresses` (
  `enrollment_id` INT NOT NULL,
  `finished_lecture_id` INT NOT NULL,
  PRIMARY KEY (`enrollment_id`, `finished_lecture_id`),
  INDEX `progress_lecture_idx` (`finished_lecture_id` ASC) VISIBLE,
  CONSTRAINT `progress_enrollment`
    FOREIGN KEY (`enrollment_id`)
    REFERENCES `mydb`.`Enrollments` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `progress_lecture`
    FOREIGN KEY (`finished_lecture_id`)
    REFERENCES `mydb`.`Lectures` (`id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
