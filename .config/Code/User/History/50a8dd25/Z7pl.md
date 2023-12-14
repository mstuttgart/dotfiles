
## Array

O _array_ é utilizado para armazenar multiplos valores em uma unica variável. Funciona como uma lista e apresenta os métodos mais conhecidos desse tipo de estrutura de dados.

Exemplo:

```javascript
const lista = [2, 4.5, 'abc', 0]

// Consulta por indice
console.log(lista[0])   // 2

// Consulta por indice quando o indice nao existe
console.log(lista[4])    // undefined

// Consulta do comprimento do array
console.log(lista.length)    // 4

// Inseri um novo elemento ao final do array e retorna o novo comprimento do mesmo
lista.push('js')    // [2, 4.5, 'abc', 0, 'js'] - retorna 5

// Remove o ultimo elementro do array, retornado-o
lista.pop()    // 'js'

// Remove o primeiro elementro do array, retornado-o
lista.shift()    // 2

// Adiciona um ou mais elementos ao inicio do Array, retornando o novo comprimeiro do mesmo
lista.unshift('Python')  // ['Python', 4.5, 'abc', 0]

// Remove ou substitui um ou mais elementos do array em um determinada posicao. Retorna um Array com os objetos removidos

//
// splice(start=0, deleteCount, item1, item2, itemN)
//
lista.splice(1, 2)  // [4.5, 'abc']
```

Quando atribuimos um valor a um indice que não existe no _array_, o Javascript irá estender o _array_, o preenchendo com _undefined_ até o indice desejado, que receberá o valor que foi fornecido.

Exemplo:

```javascript
const lista = [2, 'abc', 4]

// Atribimos um valor a um indice que nao existe na lista
lista[5] = true

console.log(lista[3])    // undefined
console.log(lista[4])    // undefined
console.log(lista[5])    // true
```

### Array Destructuring

É um modo prático de extrair valores de um _array_ e atribui-los a variáveis distintas.

Exemplo:

```javascript
var lista = ['x', 'y', 'z']

// destructuring padrao
var [a, b, c] = lista

console.log(a)    // 'x'
console.log(b)    // 'y'
console.log(c)    // 'y'

// Trocando valor entre variáveis
var [a, b] = [b, a]

console.log(a)    // 'y'
console.log(b)    // 'x'

```

## Rest e Spread

O Javascript possui o operador `...`, que facilita trabalhar com lista que não conhecemos a quantidade de elementos. Dependendo do contexto de uso (lado esquerdo ou direito da atribuição), é chamado de operador `rest` ou operador `spread`.

### Rest Elements

Quando o operador `...` aparece do lado esquerdo da atribuição, é denominado como operador `rest`. Este operador coleta zero ou mais valores, armazenando-os em um _array_.

```javascript
// Separando valores em particular
var [a, b, ...resto] = [1, 2, 3, 4, 5]

console.log(a)      // 1
console.log(b)      // 2
console.log(resto)  // [3, 4, 5]

```

O _array_ `resto` que aparece acompanhada do operador é denominado `rest elements`.

> O _elemento `rest`_ deve ser o último elemento do operação de _destructurig_.

```javascript
const [...resto, a, b] = [1, 2, 3, 4, 5]
```

O exemplo acima irá apresentar um `SyntaxError`, porque o _rest element_ não esta no final da operação de _destructuring_.

### Rest Properties

Também podemos aplicar o mesmo conceito do operador `rest` para propriedades de objetos.

Exemplo:

```javascript
const {nome, ...endereco} = {
    nome: 'Maria',
    rua: 'Rua 123',
    cidade: 'Sao Paulo',
}

console.log(home)       // Maria
console.log(endereco)   // {rua: 'Rua 123', cidade: 'Sao Paulo'}

```

### Rest Parameters

O operador `rest` também pode ser utilizado como parâmento de uma função, possibilitando que passemso um número variável de parametros durante a chamada da função.

```javascript
function printName(...name) {
    console.log(name.join(' '))
}

printName('Maria')       // Maria
printName('Joao', 'Paulo')  // Joao Paulo
```

## Spread

### Spread Elements

Quando o operador `...` aparece do lado direto do operador de atribuição, ele é denominado operador `spread`. Esse operador expande um _array_ em uma lista de elementos e, diferente do operador `rest`, pode ser usado mais de uma vez e em qualquer lugar da expressão.

```javascript
const resto = [3, 4, 5]

const a = [1, 2, ...resto]

console.log(a)   // [1, 2, 3, 4, 5]
```

### Spread Properties

Assim como o operador `rest`, também podemos utilizar o `spread` sobre propriedades de objetos.

```javascript
let endereco = {
    rua: 'Rua 123',
    cidade: 'Sao Paulo',
}

endereco = {...endereco, estado: 'SP'}

console.log(endereco)   // {rua: 'Rua 123', cidade: 'Sao Paulo', estado: 'SP'}
```

## Array Analysis

São método nativos para analisar o conteúdo de um array. A maioria desses métodos recebe uma _function_ como parâmetro (denominada _predicate_) e devolve _true_ ou _false_ como parâmetro. Normalmente são utilizadas no lugar de laços _for_.

**include**

Verifica se um array contem um determinado valor.

Exemplo:

```javascript
const lista = ['one', 2, 3, 'four', 5];

lista.include('one');  // true
lista.include(4);      // false
```

**every**

Verifica se todos os elementos do array cumprem o requisito analisado pela _function_, retornando _true_ ou _false_.

Exemplo:

```javascript
const pares = [2, 4, 6, 8];

pares.every((n) => n % 2 == 0)  // true (todos sao pares)
```

> Funcionamento semelhante ao _all()_ em Python.

**some**

Verifica se pelo menos um dos elementros do array cumpre o requisito analisado pela função, retornando _true_ ou _false_.

Exemplo:

```javascript
const lista = [1, 2, 4, 6];

lista.some((n) => n % 2 != 0); // true (o numero 1 é impar)
```

> Funcionamento semelhante ao _any()_ em Python.

**find**

Retorna o valor do primeiro elemento que satisfaça a condição analisada pela função.

Exemplo:

```javascript
const lista = [1, 2, 3, 4]

lista.find((n) => n % 3 == 0); // 3 (primeiro numero divisivel por 3)
```

**findIndex**

Funciona de forma semelhante ao _find()_, porém retorna o indice do elemento ao invés do elemento em si.

Exemplo:

```javascript
const lista = [1, 2, 3, 4];

lista.findIndex((n) => n % 3 == 0);  // 2 (indice do numero 3)
```

### Array Transformations

A classe Array possui muitos metodos para manipulação de valores. Esses métodos são denominados _puros_ quando não alteram o array original. Quando os valores do array original são alterados, a função é denominada _impura_.

Exemplo função _pura_:

```javascript
const lista = [1, 2, 3, 4];

lista.filter(n => n % 2 == 0);  // [2, 4]
```

Exemplo função _impura_:

```javascript
const lista =  [1, 2, 3, 4];

lista.reverse(); // [4, 3, 2, 1]
```

### Object[^7]

**Object** é uma _function_ do Javascript. É utilizado para armazenar coleços de _chave: valor_.

> Não confundir _object_ com o formato _JSON(Javascript Object Notation)_. Apesar de serem parecidos, o **JSON** é um formato textual e aceita apenas aspas duplas como delimitador de texto, enquanto **Object** é uma notação literal para objetos e aceita tanto aspas simples como aspas duplas para delimitar textos

O exemplo a seguir cria um _object_ com 2 propriedades _chave: valor_.

> O _object_ funciona de modo semelhante ao _dict_ do Python.

Exemplo:

```javascript
const aluno = {
    nome: 'João',
    idade: 15,
    curso: 'Engenharia',
}

// Acessando valores
console.log(aluno.nome)      // 'João'
console.log(aluno['idade'])  // 15

// Adicionando novas chaves ao object
aluno.turma = '2A'  // ou
aluno['turma'] = '2A'

// Deletando chaves do object
delete aluno.curso     // ou
delete aluno['curso']

// Verificando se uma chave existe no object
aluno.hasOwnProperty('idade') // true

// Nova versao
Object.prototype.hasOwnProperty.call(aluno, 'idade')
```

Podemos também utilizar um _object_ como base para a criaçãoi de outro _objeto_.

Exemplo:

```javascript
const objA = {
    a: 1,
    b: 2,
}

const objC = { ...objA, c: 3} // novo object {a: 1, b: 2, c:3}
```
