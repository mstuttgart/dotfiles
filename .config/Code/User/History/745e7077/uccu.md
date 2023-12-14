# Regex

Em Javascript tem duas formas de declar expressões regulares: *regex literal* e *regex com contrutor*.

Exemplo *Expressão Regular Literal*:

É recomendável utilizar esta forma quando o padrão do *regex* for estático.

```javascript
const regex = \[a-b]\
```

Exemplo *Expressão Regular com Construtor*:

É recomendável utilizar esta forma quando o padrão do *regex* for dinâmico.

```javascript
const regex = new RegExp('[a-b]')
```

## Flags

As principais *flags* utilizadas são:

- `/g`  - busca global
- `/i` - busca *case sensitive*
- `/m` - busca multi-linha

A *flag* `/g` nos permite  buscar todas as ocorrência de um padrão dentro de uma *string*. Sem esta *flag*, apenas a primeira ocorrência será retornada.

A *flag* `/i` permite buscar ocorrência ignorando se as mesmas são *Uppercase* ou *Lowercase*

## Metodos mais comuns

A seguir temos as funções mais comuns utilizadas com *regex*.

### Test

Realiza a busca de ocorrências de um determinado padrão em uma string e retorna *true* ou *false*.

```javascript
const str = 'Hello World! Javascript'

/Javascript$/.test(str) // true
```

### Match

Realiza a busca e a extração de ocorrência de um padrão em uma dad *string*.

```javascript
const str = 'Code python, code javascript, code go'
const rgx = /code/gi

str.match(rgx)  // ['Code', 'code', 'code']
```

### Replace

Permite busca um padão em uma *string* e substituis suas ocorrências com um novo valor.

```javascript
const str = 'Hello, world! Python'
const rgx = /Python/gi

str.replace(rgx, 'Javascript') // 'Hello, world! Javascript' 
```

### split

Permite dividirmos uma dada *string* baseado em um determinado padrão.

```javascript
const str = 'Hello, world! Javascript'
const rgx = /[.!/s]/

str.split(rgx)   // ['Hello', 'world', 'Javascript']
```

# Referências
- [https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions)







