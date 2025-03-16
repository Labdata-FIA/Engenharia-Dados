# Tipos de UNION em SQL

No SQL, o operador `UNION` é utilizado para combinar os resultados de duas ou mais consultas em um único conjunto de resultados. Existem duas variantes principais: `UNION` e `UNION ALL`.

## 1. UNION
- **Descrição:** Combina os resultados de duas ou mais consultas e elimina quaisquer linhas duplicadas. Realiza uma operação de distinção automática nos resultados.
- **Exemplo de Uso:**
  ```sql
  SELECT email FROM Employees
  UNION
  SELECT email FROM Contractors;
  ```
  Este comando retorna todos os emails únicos de ambas as tabelas.

## 2. UNION ALL
- **Descrição:** Combina os resultados de duas ou mais consultas sem eliminar linhas duplicadas, sendo mais rápido do que o `UNION` por não necessitar de uma operação de distinção.
- **Exemplo de Uso:**
  ```sql
  SELECT email FROM Employees
  UNION ALL
  SELECT email FROM Contractors;
  ```
  Este comando retorna todos os emails, incluindo duplicatas, de ambas as tabelas.

### Considerações de Uso
- **Performance:** `UNION ALL` é mais rápido que `UNION` devido à ausência de necessidade de verificar e eliminar duplicatas.
- **Aplicação:** Use `UNION` para resultados sem duplicatas e `UNION ALL` quando duplicatas são aceitáveis ou desejadas, ou quando a performance é uma prioridade.

## Navegação
- [Anterior](12-exemplo-having.md)
- [Próximo](14-exemplo-union.md)
