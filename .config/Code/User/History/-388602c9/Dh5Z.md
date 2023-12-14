# Manipulação de strings

Variável global `IFS` do Bash. Usada para separação de uma string a partir de um delimitador (padrão é `espace`)

O exemplo abaixo criar um array com cada uma das palavras de `TEXT` 
```bash
IFS=" "; ARRWORD=($TEXT); unset IFS;
```