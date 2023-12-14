# Manipulação de strings

Variável global `IFS` do Bash. Usada para separação de uma string a partir de um delimitador (padrão é `espace`)

O exemplo abaixo criar um array `ARRWORD` com cada uma das palavras de `TEXT` usando espaço em branco como delimitador.

```bash
IFS=" "; ARRWORD=($TEXT); unset IFS;
```

O comando `tr` também pode ser utilizado para realizar substituições ou remoção de caracteres de uma string.

```bash
# convert all string to uppercase
TEXT=$(echo $TEXT | tr [:lower:] [:upper:])

# delete ',' from string
TEXT=$(echo $TEXT | tr -d ",")

# delete '_' from string
TEXT=$(echo $TEXT | tr -d "_")

```