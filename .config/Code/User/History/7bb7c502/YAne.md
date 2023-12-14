## Prototypes & Classes 

Javascript permite programação orientada a objetos utilizando herança baseada em prototipos.

### Prototype Syntax

#### Constructor Function

Quando uma *function* é utilizada como *template* (*class*), ela é chamada *contructor function* (o nome da função deve seguir o padrão *CamelCase* para esse caso). As instâcias (objetos) derivados do template utilizam *new* para invocar o contrutor do template.

```javascript
function Car() {
   // ...
}

const car1 = new Car();
const car2 = new Car();
```

Os objetos criados possuem uma *property* interna denominada *prototype*. Essa *property* é uma relação com a *contructor functon*. Ela armazena uma referência para a chave *prototype* da *contructor function*.

#### Campos e métodos

Os campos de uma *contructor function* podem ser acessadas utilizando o *this*.

```javascript
function Car(color) {
	this.color = color;
}

const car = new Car('azul');
console.log(car.color);   // azul
```

Os métodos podém ser acessados usando a *property* **prototype** da *constructor function*.

```javascript
function Car(color) {
	this.color = color;
	this.engineRunning = false;
}

Car.prototype.start = function () {
	this.engineRunning = true;
}

const car = new Car('azul');
car.start();
```

### Class Syntax

Nas versões mais recentes, Javascript trouxe a palavra chave *class*, utilizada para criação de templates como o mesmo funcionamento de outras linguagens 
Orientadas a Objetos.

```javascript
class Car {

	contructor(color) {
		this.color = color;
		this.startEngine = false;
	}

	start() {
		this.startEngine = true;
	}

	addGas(litre) {
		// ...
	}
}

const car = new Car('red');
car.start();
```

Mesmo com a utilização de classes, Javascript ainda continua sendo uma linguagem baseadas em protótipos.

Os *get* e *set* de outras linguagens OO também estão presentes.

```javascript
class Car {

	contructor(color) {
		this._color = color; // atributos privados
		this._gas = 100;
	}

	// Consulta de atributo
	get gas() {
		return this._gas;
	}

	// Atribuicao de valor
	// podemos bloquear a atribuicao por aqui
	set gas(value) {
		this._gas = value;
	}
}

const car = new Car('red');

console.log(car.gas); // 100

car.gas = 0;
```

#### Herança de classes

Podemos também utilizar herança entre as classes utilizando a palavra chave *extends*.

```javascript

class Car {

	contructor(color) {
		this.color = color;
		this.gas = 100;
	}

	addGas(value) {
		this.gas = value;
	}
}

class Ferrari extends Car {

	contructor(color) {
		super(color);
	}

	addGas(value) {
		super.addGas();
		console.log('Add gas');
	}
}

const car = new Ferrari('red');
car.addGas(50);

```

## Referências

- https://www.w3schools.com/js/js_classes.asp




