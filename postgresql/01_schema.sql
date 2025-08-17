CREATE USER lab WITH PASSWORD 'lab';

CREATE DATABASE lab OWNER lab;

CREATE SCHEMA IF NOT EXISTS public;

CREATE TABLE IF NOT EXISTS usuario (
  User_ID BIGINT PRIMARY KEY,
  Nome TEXT
);

CREATE TABLE IF NOT EXISTS categoria (
  Product_Category INT PRIMARY KEY,
  Descricao TEXT
);

INSERT INTO usuario(user_id, Nome) VALUES (1001051, 'Pedro');

  
INSERT INTO categoria(Product_Category, Descricao) VALUES
  (6, 'Celular');