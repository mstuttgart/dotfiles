# Fundamentals

Javascript é uma linguagem de auto nível que segue o padrão ECMAScript. Ela é fracamente tipada e possui tipagem dinâmica, Orientação Objetos baseada em Protótipos e funções como cidadão de primeira classe. Suporta os paradigmas de programação imperativo, funcional e orientada a eventos.

### Características

#### Fracamente Tipada

Uma linguagem **fracamente tipada** aceita que valores de tipos diferentes sejam atribuídos a uma mesma variável.

```javascript
var a = 'exemplo'

a = 10 // não causa erro
```

Em linguagens **fortemente tipadas** (como C, C++ e Java), ocorreria um erro no codigo acima. Pois um variável que foi declarada com _string_, seria permitido receber apenas valores do tipo _string_.

#### Tipagem Dinâmica

Uma linguagem pode possuir tipagem _Estática_ ou _Dinâmica_.

***

Na **Tipagem Estática**, quando o tipo da valores que a variável irá receber é determinado na declaração da variável (como ocorre no C, C++ e Java).

Na **Tipagem Dinâmica**, o tipo de valor da variável é determinado somente **no** momento que um valor é atribuído a ela.

Podemos **usar** o comando _typeof_ para determinar o tipo do valor contido na variável.

> typeof value

Exemplo:

```javascript
var a = 'exemplo'
typeof a    // string

a = 10
typeof a    // number
```

### Number[^1]

Em Javascript, o tipo **Number** é uma função e representa tanto números inteiros (Integer) como números de ponto flutuante (Float). Ele apresenta várias operações muito úteis, como no exemplo a seguir.

Exemplo:

```javascript
// Exemplo de Numbers
typeof -5    // number
typeof 10    // number
typeof 2.5   // number

// Determinar se um numero é ou não inteiro
Number.isInteger(2.6)   // true
Number.isInteger(15)    // false

// Delimitar o numero de casas decimais
(3.1415).toFixed(2)    // '3.14' 

// Converter valor numerico para string
(3.1415).toString()    // '3.1415'

// Converter valor numerico para string, mas para base binária (2)
(7).toString(2)    // '111'
```

#### Números especiais

Javascript possui alguns valores de números especiais que normalmente não encontramos em outra linguagem: `NaN` e `Infinity`.

**NaN**

O valor `Nan` (do inglês, _Not a Number_) é produzido quando o resultado de uma operação retorna um valor que não é um _Number_.

Exemplo:

```javascript
var Number('hello')   // NaN -> o número não pode ser parseado
var Number('12a')     

var Math.sqrt(-4)  // NaN -> operação falhou raiz de numero negativo)

var NaN + 4   // NaN
```

**Importante**:

> `NaN` é o único valor que não ígual a si mesmo.

```javascript
NaN === NaN   // false

typeof NaN  // Number
```

Essa peculiaridade vem da regra [IEEE](https://en.wikipedia.org/wiki/IEEE\_754) utilizada para operações com ponto flutuante. Isso ocorre devido a natureza dos valores que o `NaN` pode representar.

```javascript
var raizA = Math.sqrt(-4)   // NaN
var raizB = Math.sqrt(-25)  // NaN

raizA === raizB  // false
```

Para realizar a verificação se um determinado valor é `NaN`, ddevemos utilizar a função `isNaN`:

```javascript
isNaN('12a')  // true
isNan(4)      // false
```

**Infinity**

É considerado o maior "número" da linguagem, assim como `-Infinty` é considerado o menor, com exceção do `NaN`. De modo a verificar se um _Number_ assume um dos valores `Infinity`, utilizamos a função `isFinite`.

```javascript
isFinite(1000)      // true
isFinite(Infinity)  // false
isFinite(NaN)       // false
```

#### Operações aritméticas

O Javascript apresenta alguma excentricidades em relação ao _Number_ que devem ser observadas.

**Divisão por zero**

Diferente de outras linguagens, o Javascript não irá acusar erro ou disparar uma exceção quando ocorrer uma divisão por zero. Ao invés disso, a linguagem possui o tipo **Infinity**, um tipo especial para representar valores infinitos.

```javascript
a = 5/8   // Infinity
```

**Operações com tipos diferentes**

Por ser fracamente tipada, o Javascript permite alguns tipos de operações envolvendo valores de tipos diferentes.

```javascript
a = '10' / 2    // 5
b = '10' * 2    // 10

c = '10,2' * 2    // Nan (indefinido, por causa da virgula, o JS nao sabe que é um número)
```

**Chamando funções diretamente**

Quando desejado podemos chamar as funções diretamente pelo Number, sem precisar guardar o valor em uma variável primeiro.

```javascript
10.toString()    // Uncaught SyntaxError: Invalid or unexpected token

(10).toString()    // '10'
```

**Operações com números de ponto flutuante**

Em operações com números de ponto flutuante, o Javascript sempre irá retornar o número máximo de casas decimais, seguindo o padrão IEEE .

```javascript
var soma = 0.1 + 0.7    //0.7999999999999999
```

#### Math

O objeto **Math** nos permite executar tarefas matemáticas, como raiz quadrada, elevar um número a determinada potência, seno e cosseno de um determinado angulo e determinar o máximo e mínimo de um determinado conjunto de valores, entre outras funções.

**Math** não é um construtor, então todos os metodos do objeto podem ser chamados sem criá-lo (semelhante a funções estática de outras linguagens).

```javascript
Math.PI    // valor PI

Math.sqrt(4)    // raiz quadrada de 4.

Math.pow(2, 3)    // 2^3

Math.max(2, 1, 5, 4)    // 5 -> maior valor de um conjunto de valores

Math.floor(3.1415)    // 3 -> arredondamento para o inteiro anterior
Math.ceil(3.1415)     // 4 -> arredondamento para o inteiro superior
```

### String

Em Javascript, uma _string_ pode ser representada tanto por aspas duplas quanto por aspas simples. A _string_ é tratada como uma lista, isso nos permite realizar buscas e cortes na mesma, conforme a necessidade.

Exemplos:

```javascript
text = 'Javascript'

// Retorna o caracter de uma determinada posicao
text.charAt(0)    // 'J'
text.charAt(20)    // '' . string vazia quando o indice nao existir na string

// Retorna o indice de um determinado caracter
text.indexOf('c')    // 5 
text.indexOf('a')    // 1 retorna a primeira ocorrencia do caracter 'a'

// Retorna substring a partir de um intervalor de indices
text.substring(1)    // 'avascript' . Do indice 1 até o final da string
text.substring(0, 3)    // 'Java'. Do indice 0 ao 3

// Separa uma string a partir de um caracter delimitador
'Javascript, Python, Go'.split(',')    // ['Javascript', 'Python', 'Go']

// Busca dentro da string (pode ser utilizado Regex)
'Javascript, Python, Go'.search('Python')    // 12. Indice da primeira ocorrencia que coincide coma busca
```

#### Interpolação e Concatenação de strings

O Javascript, assim como outras linguagens, também apresenta recursos para _interpolação_ e _concatenação_ de strings. **Interpolação de Strings** seria utilizar uma string como _template_, onde essa string possui variaveis nas partes de texto que valores reais durante o processo de interpolação.

Exemplo _concatenação_:

```javascript
text = 'Javascript'

// Concatenacao utilizando a funcao 'cocat'
text.cocat(' é ', ' nota', ' 10!')    // 'Javascript é nota 10!'

// Concatenacao usando operador +
text = text + ' é ' + ' nota ' + ' 10!'
```

Exemplo _interpolação_:

```javascript
var nota = 10

// Transformamos a string em uma template string, onde a chave #{nota} recebe
// o valor da variavel 'nota'
text = `Javascript é nota ${nota}!`    // 'Javascript é nota 10!'
```

O Javascript tentará executar tudo o que esta dentro da chave `${}`. Desde a execução de funções até operações aritméticas.

```javascript
text = `2 + 3 = ${2 + 3}`    // '2 + 3 = 5'
```

### Boolean[^2]

Em Javascript, os valores booleanos são representados por _true_ e _false_. Como ocorre em algumas linguagens, alguns valores também podem representar _true_ ou _false_ quando utilizados em determinados contextos.

Os valores a seguir são considerados _true_:

* `true`,
* `1`: ou qualquer inteiro diferente de zero,
* `' '`: string com pelo menos um caracter (mesmo que seja espaço) ,
* `Infinity`: palavra reservada,
* `[]`: array vazio,
* `{}`: objeto literal.

Os valores a seguir são considerados _false_:

* `false`,
* `0`: valor inteiro,
* `null`: palavra reservada,
* `undefined`: palavra reservada,
*   `NaN`: palavra reservada (_Not a Number_).

    ### Declaração de variáveis

**let** e **const** são substitutos para **var**, introduzidos no [ECMAScript6](https://www.w3schools.com/js/js\_es6.asp) e proveem escopo de block para o Javascript. Antes do ES6 (2015), o JavaScript possuia apernas _escopo global_ e _escopo de função_.

#### var

As variáveis definidas com _var_ possuem as seguintes propriedades:

* Devem ser declaradas antes do uso
* Podem ser redeclaradas
* Possuem escopo global ou de função

ECMAScript6 (ES6 / JavaScript 2015) encoraja a declaração de varáveis com **let**, de modo a evitar alguns possíveis problemas. O primeiro diz respeito ao escopo.

Exemplo:

```javascript
var n = 5

{
    var n = 10
}

console.log(n)    // 10
```

No exemplo acima, vericamos que o valor impresso nas duas situações foi `10`. Isso ocorre porque _var_ permite a redeclaração de variáveis e redeclar uma variável dentro de um block iŕa redeclará-la fora do bloco. Sendo assim, o Javascript intepretou que as duas variáveis `n` eram na verdade, a mesma variável. Por isso o valor impresso foi o valor da última atribuição.

Outro inconveniente de `var` é o fato dele permitir o acesso externo de variáveis declaras dentro do bloco `{}`.

Exemplo:

```javascript
{
    var nome = 'Maria' 
}

console.log(nome)    // 'Maria'
```

Essa liberdade de acesso independente do escopo pode atrapalhar a legibilidade de código e causar erros de inconsistência no estado das variáveis (valor armazenado pela mesma), algo muito importante em linguagens de paradigma funcional.

#### let[^3]

As variáveis definidas com _let_ possuem as seguintes propriedades:

* Devem ser declaradas antes do uso
* Não podem ser redeclaradas
* Possuem escopo de bloco `{}`

O uso de _let_ resolve os incoveniêntes apresentado pelo uso do _var_.

Exemplo:

```javascript
let n = 5

{
    let n = 10
}

console.log(n)    // 5 (o valor foi mantido)
```

O _let_ não permite a redeclaração de variáveis em um mesmo escopo de bloco `{}`. Sendo assim, o Javascript entende que, salvo terem o mesmo nome, as varáveis `n` são variáveis diferentes.

```javascript
{
    let nome = 'Maria'
    let nome = 'Pedro' // SyntaxError: Identifier 'nome' has already been declared
}
```

O _let_ também não permite o acesso fora do escopo de bloco onde ele foi declarado.

Exemplo:

```javascript
{
    let nome = 'Maria' 
}

console.log(nome)    // ReferenceError: nome is not defined
```

A tentativa de acesso resultará em um `ReferenceError` indicando que a variável `nome` não foi definida.

#### const

As variáveis definidas com _const_ possuem as seguintes propriedades:

* Devem ser declaradas e inicializas com um valor antes do uso
* Não podem ser redeclaradas
* Não podem sofrer reatribuição
* Possuem escopo de bloco `{}`

Exemplo:

```javascript
const PI = 3.1414   // Declaramos a constante PI e a inicializamos
PI = 3.14           // TypeError: Assignment to constant variable.

const PI = 3.14     // SyntaxError: Identifier 'PI' has already been declared
```

Sempre declaramos uma variável com _const_ quando sabemos que a _referência_ ao qual ela aponta não deve mudar. Recomenda-se o uso de _const_ quando declaramos:

* Um novo _array_
* Um novo _object_
* Uma nova _Function_

O _const_ não define um uma valor constante. Ela define um referência constante a uma valor. Sendo assim, não podemos reatribuir outro _object_ a uma constante, mas podemos alterar os valores do mesmo.

Exemplo:

```javascript
const pessoa = {nome: 'Maria'}

pessoa.nome = 'Joao'       // conseguimos alterar o atributo do object

pessoa = {nome: 'Pedro'}  // TypeError: Assignment to constant variable.
```

#### Hoisting[^4]

**Hoisting** é um comportamento padrão do Javascript de mover todas as declaração para o topo do escopo atual (para o topo do _script_ ou da função). Isso permite que variáveis possam ser utilizadas antes de serem declaradas.

```javascript
n = 10

.
. // codigo qualquer
.

var n
```

É a mesma coisa que:

```javascript
n = 10
var n

.
.  // codigo qualquer
.
```

O Javascript somente executa o _hoisting_ para declarações, não inicializações:

```javascript
var a = 10
var b = 2

console.log(a + b)  // 12
```

É diferente de:

```javascript
var a = 10

console.log(a + b)  // b is undefined

var b = 2
```

O Javascript irá indicar que `b` esta `undefined`. Isso ocorre porque somente a declaração `var b`, e não atribuição `= 2`, sofreu _hoisting_ para o topo do _script_. Em outras palavras, ocorre o comportamento semelhante ao seguinte código:

```javascript
var a = 10    // inicializa 'a'
var b         // declara 'b'

console.log(a + b)  // 'b' is undefined

b = 2   // somente aqui atriuimos um valor a 'b'
```

**Comportamento para o **_**let**_** e **_**const**_

Variáveis declaradas com _let_ e _const_ sofrem _hoisting_ para o topo do bloco, mas não são inicializadas. Isso significa que o bloco sabe da existência das variáveis, mas não pode usá-las até que as mesmas sejam declaradas.

Exemplo:

```javascript
{
    nome = 'Maria'
    let nome   // ReferenceError: Cannot access 'nome' before
}

{
    PI = 3.14
    const PI  // SyntaxError: Missing initializer in const declaration
}
```

**Boas práticas**

O funcionamento do _hoisting_ pode causar erros dificeis de depurar caso não saibamos do seu funcionamento e resultar em estados inesperados nas variáveis. De modo a evitar o surgimento de bugs e melhorar a legibilidade do código, é uma boa prática _sempre_ declarar as variáveis no inicio de cada escopo e evitar usar variaveis que ainda não foram declaradas (o uso de _let_ e _const_ evita isso).

#### Null e Undefined

São valores denominados _**nullish**_.

**Undefined** é utilizado pelo Javascript quando temos uma variável que não foi inicializada com nenhum valor.

```javascript
var n
console.log(n)    // sera retornado o tipo undefined
```

**Null** é utilizado quando queremos evitar que uma variável fique como _undefined_ mas não desejamos atribui nenhum valor a ela.

```javascript
var n = null
console.log(n)    // sera retornado null
```

O Javascript utiliza _cópia por referência_ para atribuição de valores. O mesmo não ocorre para tipos primitivos, onde é utilizada a _cópia por valor_.

```Javascript
// Object simples
var a = {nome: 'João'}

// Na atribuicao de objetos, ocorre a copia por referencia.
var b = a

/* 
Como as variáveis 'a' e 'b' apontam para o mesmo endereco de memoria, se alterarmos uma propriedade de 'b', o conteúdo de 'a' tambem sera alterado
*/
b.nome = 'Pedro'

console.log(b.nome)    // 'Pedro'
console.log(a.nome)    // 'Pedro'
```

O **null** também é util quando desejamos reinicializar o valor de um objeto.

```javascript
var a = {nome: 'João'}

a = null
console.log(a)    // null
```

### Operadores

Existem diferentes tipos de operadores em Javascripts e esses são separados nas seguintes categorias:

* Operadores Aritméticos
* Operadores de Atribuição
* Operadores de Comparação
* Operadores Lógicos
* Operadores Condicionais
* Operadores de Tipo

#### Operadores Aritméticos

São utilizados para executar operações aritméticas de números.

| Operador | Descrição                                                           |
| -------- | ------------------------------------------------------------------- |
| +        | Adição                                                              |
| -        | Subtração                                                           |
| \*       | Multiplicação                                                       |
| \*\*     | Exponenciação ([ES2016](https://www.w3schools.com/js/js\_2016.asp)) |
| /        | Divisão                                                             |
| %        | Modulo (resto da divisão)                                           |
| ++       | incremento                                                          |
| --       | Decremento                                                          |

#### Operadores de Atribuição

São utilizados para atribuir valores as variáveis.

Exemplo:

```javascript
x += y    // x = x + y
x++       // x = x + 1

x -= y    // x = x - y
x--       // x = x - 1

x *= y    // x = x * y
x /= y    // x = x / y

x %= y    // x = x % y
x **= y   // x = x ** y
```

**Atribuição Via Desestruturação**

No Javascript, uma **atribuição via desestruturação** (do inglês, _destructuring assignment_), é uma expressão que permite extrair dados de _arrays_ ou _objects_ em variáveis distintas.

Exemplo com _object_:

```javascript
const pessoa = {
    nome: 'Maria',
    idade: '20'
}

// destructuring padrao
var {nome, idade} = pessoa

console.log(nome)    // 'Maria'
console.log(idade)   // 20

// pessoa nao possui o atributo 'curso', entao 'curso' recebe um valor padrao
var {nome, idade, curso='Enfermagem'} = pessoa

console.log(nome)    // 'Maria'
console.log(idade)   // 20
console.log(curso)   // 'Enfermagem'

// destructuring ignorando valores (no caso, a propriedade 'idade')
var {nome, , curso='Enfermagem'} = pessoa

console.log(nome)    // 'Maria'
console.log(curso)   // 'Enfermagem'
```

#### Operadores de Tipo

| Operador   | Descrição                                                     |
| ---------- | ------------------------------------------------------------- |
| typeof     | Retorna o tipo da variável                                    |
| instanceof | Retorma `true` se um objeto é uma instância de um tipo objeto |

Exemplo:

```javascript
const langs = ['Javascript', 'Python', 'Go', 'C']

console.log(langs instanceof Array)    // true
console.log(langs instanceof Object)   // true
console.log(langs instanceof Number)   // false
```

#### Operadores de Manipulação de Bits

São operadores de _bits_ utilizados para trabalhar com numeros de 32 bits. Qualquer valor númerico na operação é convertido em um número de 32 bits. O resultado é reconvertido para um `Number`.

| Operador | Descrição            |
| -------- | -------------------- |
| &        | AND                  |
| \|       | OR                   |
| \~       | NOT                  |
| ^        | XOR                  |
| <<       | left shift           |
| >>       | right shift          |
| >>>      | unsigned right shift |

### Estruturas de Controle

As estruturas de controle no Javascript são semelhantes ao encontrado em outras linguagens.

#### Estrutura IF/ELSE[^5]

Possui estrutura semelhante ao de outras linguagens com C e Java.

Exemplo:

```javascript
if (condicao_1) {  
    //  codigo qualquer 
  
} else if (condicao_2) {
    // codigo qualquer

} else {  
    // codigo quanlquer
}
```

Se o bloco de código do `IF` possuir apenas uma linha, podemos omitir as chaves `{}`.

```javascript
if (condicao)
    console.log('A')

    console.log('B')
```

No exemplo acima, como não utilizamos chaves `{}` para o `IF`, o Javascript interpreta que o bloco de código do `IF` contem apenas a linha com o comando `console.log('A')`. Sendo assim, a _string_ `'A'` será impressa apenas se `condicao` for verdadeira. Por outro lado, a _string_ `'B'` sempre será impressa, independente do valor.

#### Estrutura Switch

Funciona também de modo semelhate ao de outras linguagens.

Exemplo:

```javascript
switch(expressao) {  
  case x:  
    // codigo qualquer
    break;  
  case y:  
    // codigo qualquer
    break;  
  default:  
     // codigo qualquer
}
```

É uma boa prática sempre utilizar o `default`, de modo a garantir o tratamento para todos os possíveis resultados de `expressao`.

#### Estrutura While e Do While[^6]

Segue o mesmo funcionamento do _while_ e do _do while_ presente em outras linguagens.

Exemplo:

```javascript
while (condicao) {  
    // codigo qualquer
}
```

Exemplo:

```javascript
do {  
    // codigo qualquer
}  
while (condicao)
```

#### Estrutura FOR e FOR/IN

O Javascript nos fornece dois tipos de estrutura de repetição **for**.

* `for`: percorre um bloco de código, um determinado número de vezes.
* `for/in`: percorre as propriedades de um objeto.
* `for/of`: percorre os valores das propriedades um objeto .

A seguir, temos alguns exemplos do uso da estrutura **for** , **for/in** e **for/of** e suas descrições.

**FOR**

O **for** comum, encontrado em outras linguagens com `C` e `Java`. É utilizado para percorrer _arrays_.

Exemplo:

```javascript
const alunos = ['Maria', 'Joao', 'Pedro']

for (let i = 0; i < alunos.length; i++) {
    console.log(i, alunos[i])
}

// -> 0 'Maria'
// -> 1 'Joao'
// -> 2 'Pedro'
```

**FOR/IN**

É utilizado para percorrer as propriedades enumeradas de um objeto. No caso de _arrays_, temos o seguinte comportamento.

Exemplo:

```javascript
// Percorrendo um array
const alunos = ['Maria', 'Joao', 'Pedro']

for (let a in alunos) {
    console.log(a)
}

// 0
// 1
// 2
```

A variável `a` recebeu em cada interação, não o valor contido no _array_, mas o seu indice. O laço **for/in** interage sobre propriedades enumeradas de um objeto, na ordem original de inserção.

Para _objects_, o **for/in** funciona retornando as propriedades dos objetos, e não seus valores.

Exemplo:

```javascript
// Percorrendo um object
const pessoa = {
    nome: 'Maria', 
    idade: 20
}

for (let p in pessoa) {
    console.log(`${p} = ${pessoa[p]}`)
}

//  -> nome = Maria
//  -> idade = 20
```

**FOR/OF**

O **for/of** foi introduzido no [ECMAScript 6 (2015)](https://www.w3schools.com/js/js\_es6.asp) e é utilizado para interar através dos valores de objetos interaveis. Ele nos permite iterar através de estruturas de dados como _Arrays, Sets, Maps_ e _Strings_.

Exemplo:

```javascript
// Percorrendo um array
const alunos = ['Maria', 'Joao', 'Pedro']

for (let a of alunos) {
    console.log(a)
}

// Maria
// Joao
// Pedro
```

Se tentarmos utilizar o **for/of** com um _object_, como no código a seguir:

```javascript
// Percorrendo um object
const Pessoa = {
    nome: 'Maria', 
    idade: 20
}

for (let p of Pessoa) {
    console.log(p)
}

// TypeError: Pessoa is not iterable
```

Isso ocorre porque o objeto `Pessoa` não implementa a propriedade que permite a iteração.

#### Break e Continue

Ainda cobrindo a área de _loops_, temos dois comandos muito úteis:

* `break`: comando que "pula fora" do _loop_.
* `continue`: comando que "pula" uma iteração do _loop_.

Exemplo **break**:

```javascript
const alunos = ['Maria', 'Joao', 'Pedro', 'Mel']

for (let a of alunos) {

    // Se a primeira letra do nome for 'P',saimos do loop
    if (a.charAt(0) == 'P') {
        break
    } else {
        console.log(a)
    }

}

// Saida do script:
// Maria
// Joao
```

No exemplo acima, percorremos o _array_ de nomes, imprimindo cada um deles até encontrarmos um nome que começa com a leta `P`. Nesse caso, utilizamos o `break` para encerrar o _loop_ **for**.

Exemplo **continue**:

```javascript
const alunos = ['Maria', 'Joao', 'Pedro', 'Mel']

for (let a of alunos) {

    // Se a primeira letra do nome for 'P',pulamos para o proximo item
    if (a.charAt(0) == 'P') {
        continue
    } else {
        console.log(a)
    }

}

// Saida do script:
// Maria
// Joao
// Mel
```

No exemplo acima, também percorremos o _array_ de nomes, imprimindo cada um deles até encontrarmos um nome que começa com a leta `P`. Nesse caso, utilizamos o `continue` para pular para o próximo valor presente no _array_.

### Tratamento de Erros

O tratamento de erros em Javascript possui as seguintes palavras chaves:

* `try`: define o bloco de código a ser executado (_obrigatório_)
* `catch`: define o bloco de código que irá tratar o erro (_obrigatório_)
* `finally`: define um bloco de código que será executado indeferente do resultado (_opcional_)
* `throw`: utilizado para disparar um erro criado pelo usuário.

Exemplo:

```javascript
function foo () {
    throw TypeError
}

.
.
.

try {
    foo()   // pode disparar mais de um tipo de expection
} catch (e if e instanceof TypeError) {
    // tratar o erro do tipo TypeError
} catch (e) {
    // tratar o erro default
} finally {
    // executa outro codigo
}
```

### Funções

No Javascript, funções são consideradas **Objetos de Primeira Classe** (do inglês, _First Class Object_). Isso significa que as funções tem papel central na linguagem e que podemos tratá-la com um dado. Como consequência disso, tanto **object** como **class** também sao do tipo _function_ e cada função instânciada é portanto um objeto da classe **Function**.

```javascript
typeof Object            // function
typeof class Aluno {}    // function
```

Podemos armazenar uma **function** em uma variável e invocá-la posteriormente.

```javascript
const foo = function () {
    return 'Hello World!'
}

consolo.log(foo())    // 'Hello World'
```

#### Passagem de parâmetros

Assim como em outras linguagens, uma _function_ pode aceitar um conjunto de parâmetros de qualquer tipo de modo a executar seu código. Entretanto, em **Javascript**, passar mais ou menos argumentos do que a quantidade de parâmetros que a _function_ recebe não dispara nenhum erro.

> Parâmetros e retornos em Javascript são _opcionais_.

Exemplo:

```javascript
function imprimirSoma(a, b) {
    console.log(a + b)
}

imprimirSoma(2, 3)    // 5
imprimirSoma(2)       // NaN (o valor do parâmetro 'b' é undefined)
imprimirSoma(2, 3, 4, 5)   // 5 (os argumentos 4 e 5 são ignorados)
```

Podemos atribuir um valor _default_ para os parâmetros, de modo a evitar que os mesmo fiquem como _undefined_ se nenhum argumento correspondente não forem passados para a _function_.

Exemplo:

```javascript
function imprimirSoma(a, b=1) {
    console.log(a + b)
}

// Como não foi fornecido argumento para 'b', ele recebe o valor default de 1

imprimirSoma(2)   // 3 
```

O Javascript também nos permite passar **functions** como parâmetro.

Exemplo:

```javascript
function imprimir(foo){
    // aqui, invocamos a function
    foo()
}

// passamos a function como parametro
imprimir(function () {
    console.log('Hello World')
})

// Saida:
// 'Hello World!'
```

#### Retorno de função

Uma _function_ pode retornar valores de quaiquer tipos, porém pode retornar apenas um valor por vez. Uma _function_ que não retorna valor ou que possui o _return_ ausente, retorna _undefined_. No Javascript não existem _return_ implicitos.

Exemplo:

```javascript
function imprimirFoo(foo) {
    console.log(foo)
    return
}

imprimir('texto')  // retorna undefined

function imprimirFoo2(foo) {
    console.log(foo)
}

imprimitFoo2('texto')  // retorna undefined
```

#### Função Anônima

Como funções são membros de primeira classe\*, também podemos atribuí-las a variáveis. Esse recurso é muito util em diversas funções do Javascript que muitas das vezes, devido a sua natureza funcional, recebem outras funções como parâmetro.

Exemplo:

```javascript
const imprimirSoma = function (a, b) {
    console.log(a + b)
}

imprimirSoma(2, 3)    // 5
```

Também podemos atribuir uma função como uma _property_ de um objeto.

Exemplo:

```javascript
const aluno = {
    nome: 'João',
    idade: 15,
    curso () {
        return 'Engenharia'
    },
}

aluno.curso()  // Retorna 'Engenharia'
```

**Arrow Functions**

As funções anônimas também podem ser escritas usando _arrow functions_. Essa função foi introduzida no ES6 e possibilita uma notação mais exuta da função.

Exemplo:

```javascript
const imprimirSoma = (a, b) => {
    console.log(a + b)
}

imprimirSoma(2, 3)    // 5

// Outra notação
const imprimirSoma = (a, b) => console.log(a + b)

imprimirSoma(2, 3)    // 5
```

#### Função Callback[^8]

São funções passadas como argumento para outras funções e é executada dentro dessa função para completar algum tipo de rotina. Função de _callback_ são normalmente utilizadas em de assincrono.

Exemplo:

```javascript
function printHello() {
    console.log('Hello World!');
}

button.addEventListener(printHello);
```

No exemplo acima, quando o botão `button` for pressionado, a função `printHello` será invocada e mensagem `Hello World!` será impresso.

#### Função Nested (_nested function_) \[^nested-functio]

Uma função é denominada _nested_ (ou aninhada), quando é declara dentro de outra função. Normalmente é utilizada de modo a centralizar um código que ocorre repetidas vezes dentro do escopo da função ao qual ela foi inserida.

```javascript
function printHello(firstName, lastName) {

    function getName() {
        return `${firstName} ${lastName}`;
    }

    console.log('Hello, ' + getName());
    console.log('Bye ' + getName());
}
```


### Referências

1. https://www.w3schools.com/jsref/jsref\_obj\_math.asp
2. https://www.w3schools.com/jsref/jsref\_obj\_string.asp

[^1]: https://www.w3schools.com/jsref/jsref\_obj\_number.asp

[^2]: https://www.w3schools.com/jsref/jsref\_obj\_boolean.asp

[^3]: https://www.w3schools.com/js/js\_let.asp

[^4]: https://www.w3schools.com/js/js\_hoisting.asp

[^5]: https://www.w3schools.com/js/js\_if\_else.asp

[^6]: https://www.w3schools.com/js/js\_loop\_while.asp

[^7]: https://www.w3schools.com/jsref/jsref\_obj\_object.asp

[^8]: https://developer.mozilla.org/en-US/docs/Glossary/Callback\_function
