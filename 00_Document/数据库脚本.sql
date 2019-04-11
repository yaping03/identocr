/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 100213
 Source Host           : localhost:3306
 Source Schema         : kpi

 Target Server Type    : MySQL
 Target Server Version : 100213
 File Encoding         : 65001

 Date: 08/07/2018 22:20:40
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for T_ADMIN
-- ----------------------------
DROP TABLE IF EXISTS `T_ADMIN`;
CREATE TABLE `T_ADMIN` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `USERNAME` varchar(0) DEFAULT NULL COMMENT '用户名',
  `PASSWORD` varchar(0) DEFAULT NULL COMMENT '密码',
  `UPDATE_AT` varchar(0) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='管理员表';

-- ----------------------------
-- Table structure for T_DICTIONARY
-- ----------------------------
DROP TABLE IF EXISTS `T_DICTIONARY`;
CREATE TABLE `T_DICTIONARY` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `TYPE` varchar(0) DEFAULT NULL COMMENT '类型',
  `NAME` varchar(0) DEFAULT NULL COMMENT '名称',
  `VALUE` varchar(0) DEFAULT NULL COMMENT '值',
  `DESCRIPTION` varchar(0) DEFAULT NULL COMMENT '描述',
  `UPDATE_AT` varchar(0) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='字典表';

-- ----------------------------
-- Table structure for T_EXAM_ENTITY
-- ----------------------------
DROP TABLE IF EXISTS `T_EXAM_ENTITY`;
CREATE TABLE `T_EXAM_ENTITY` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(0) DEFAULT NULL COMMENT '测评体系',
  `SORT` int(11) DEFAULT NULL COMMENT '显示顺序',
  `UPDATE_AT` varchar(0) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='测评主体主表';

-- ----------------------------
-- Table structure for T_EXAM_ENTITY_DETAIL
-- ----------------------------
DROP TABLE IF EXISTS `T_EXAM_ENTITY_DETAIL`;
CREATE TABLE `T_EXAM_ENTITY_DETAIL` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ENTITY_ID` int(11) DEFAULT NULL COMMENT '主体表ID',
  `ALIAS` varchar(0) DEFAULT NULL COMMENT '简称',
  `WEIGHT` float DEFAULT NULL COMMENT '权重',
  `PAPER` varchar(0) DEFAULT NULL COMMENT '包含的票',
  `SORT` int(11) DEFAULT NULL COMMENT '显示顺序',
  `UPDATE_AT` varchar(0) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='测评主体明细表';

-- ----------------------------
-- Table structure for T_EXAM_INFO
-- ----------------------------
DROP TABLE IF EXISTS `T_EXAM_INFO`;
CREATE TABLE `T_EXAM_INFO` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ORG_ID` int(11) DEFAULT NULL COMMENT '单位ID',
  `YEAR` int(11) DEFAULT NULL COMMENT '年度',
  `BATCH` int(11) DEFAULT NULL COMMENT '批次',
  `NAME` varchar(0) DEFAULT NULL COMMENT '测评名称',
  `DATE` varchar(0) DEFAULT NULL COMMENT '测评时间',
  `UPDATE_AT` varchar(0) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='测评信息表';

-- ----------------------------
-- Table structure for T_EXAM_MEASURE
-- ----------------------------
DROP TABLE IF EXISTS `T_EXAM_MEASURE`;
CREATE TABLE `T_EXAM_MEASURE` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(0) DEFAULT NULL COMMENT '名称',
  `SORT` int(11) DEFAULT NULL COMMENT '排序',
  `UPDATE_AT` varchar(0) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评价指标主表';

-- ----------------------------
-- Table structure for T_EXAM_MEASURE_DETAIL
-- ----------------------------
DROP TABLE IF EXISTS `T_EXAM_MEASURE_DETAIL`;
CREATE TABLE `T_EXAM_MEASURE_DETAIL` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `MEASURE_ID` int(11) DEFAULT NULL COMMENT '主表ID',
  `COTENT` varchar(0) DEFAULT NULL COMMENT '考评内容',
  `NAME` varchar(0) DEFAULT NULL COMMENT '指标名称',
  `WEIGHT` float DEFAULT NULL COMMENT '权重',
  `SORT` int(11) DEFAULT NULL COMMENT '显示顺序',
  `UPDATE_AT` varchar(0) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='评价指标明细表';

-- ----------------------------
-- Table structure for T_EXAM_RESULT_MANAGER
-- ----------------------------
DROP TABLE IF EXISTS `T_EXAM_RESULT_MANAGER`;
CREATE TABLE `T_EXAM_RESULT_MANAGER` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ORG_ID` int(11) DEFAULT NULL COMMENT '单位ID',
  `YEAR` int(11) DEFAULT NULL COMMENT '年度',
  `MANAGER_ID` int(11) DEFAULT NULL COMMENT '中层干部ID',
  `ENTITY_ID` int(11) DEFAULT NULL COMMENT '测评主体ID',
  `PAPER` varchar(0) DEFAULT NULL COMMENT '票类型',
  `MEASURE_DETAIL_ID` int(11) DEFAULT NULL COMMENT '评价指标ID',
  `SCORE` int(11) DEFAULT NULL COMMENT '分数',
  `UPDATE_AT` varchar(0) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='中层干部投票数据';

-- ----------------------------
-- Table structure for T_EXAM_RESULT_TEAM
-- ----------------------------
DROP TABLE IF EXISTS `T_EXAM_RESULT_TEAM`;
CREATE TABLE `T_EXAM_RESULT_TEAM` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ORG_ID` int(11) DEFAULT NULL COMMENT '单位ID',
  `YEAR` int(11) DEFAULT NULL COMMENT '年度',
  `ENTITY_ID` int(11) DEFAULT NULL COMMENT '测评主体ID',
  `PAPER` varchar(0) DEFAULT NULL COMMENT '票类型',
  `MEASURE_DETAIL_ID` int(11) DEFAULT NULL COMMENT '评价指标ID',
  `SCORE` int(11) DEFAULT NULL COMMENT '得分',
  `UPDATE_AT` varchar(0) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='领导班子投票数据';

-- ----------------------------
-- Table structure for T_MANAGER
-- ----------------------------
DROP TABLE IF EXISTS `T_MANAGER`;
CREATE TABLE `T_MANAGER` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `YEAR` int(11) DEFAULT NULL COMMENT '年度',
  `ORG_ID` int(11) DEFAULT NULL COMMENT '所属单位ID',
  `MANAGER_NAME` varchar(0) DEFAULT NULL COMMENT '姓名',
  `MANAGER_TYPE` int(11) DEFAULT NULL COMMENT '人员类型',
  `MANAGER_TITLE` varchar(0) DEFAULT NULL COMMENT '职务',
  `WEIGHT` float DEFAULT NULL COMMENT '权重',
  `UPDATE_AT` varchar(0) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='中层干部表';

-- ----------------------------
-- Table structure for T_ORGANIZATION
-- ----------------------------
DROP TABLE IF EXISTS `T_ORGANIZATION`;
CREATE TABLE `T_ORGANIZATION` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `TYPE` int(11) DEFAULT NULL COMMENT '单位类型',
  `SHORT_NAME` varchar(0) DEFAULT NULL COMMENT '单位简称',
  `FULL_NAME` varchar(0) DEFAULT NULL COMMENT '单位全称',
  `PARENT_ID` int(11) DEFAULT NULL COMMENT '上级单位',
  `SORT` int(11) DEFAULT NULL COMMENT '显示顺序',
  `UPDATE_AT` varchar(0) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='单位表';

-- ----------------------------
-- Table structure for T_TEAM_RESULT
-- ----------------------------
DROP TABLE IF EXISTS `T_TEAM_RESULT`;
CREATE TABLE `T_TEAM_RESULT` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `YEAR` int(11) DEFAULT NULL COMMENT '年度',
  `ORG_ID` int(11) DEFAULT NULL COMMENT '单位ID',
  `TEAM_SCORE` float DEFAULT NULL COMMENT '班子业绩',
  `PARTY_BUILDING_SCORE` float DEFAULT NULL COMMENT '企业党建',
  `EXAM_SCORE` float DEFAULT NULL COMMENT '绩效成果',
  `UPDATE_AT` varchar(0) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='班子业绩表';

SET FOREIGN_KEY_CHECKS = 1;
