# Manipulação de strings

Variável global `IFS` do Bash. Usada para separação de uma string a partir de um delimitador (padrão é `espace`)

```bash
IFS=" "; ARRWORD=($TEXT); unset IFS;
```