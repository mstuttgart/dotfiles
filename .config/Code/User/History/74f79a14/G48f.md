# Promises

Um objeto *promise* representa o eventual sucesso ou falha de uma tarefa assincrona e o valor resultante. Os métodos `then()`, `catch()` e `finally()` são utilizados para associar futuras ações com um dada *promise*. Esses métodos funcionam como o conjunto *try* - *exception* para funções assincronas.

## then

O método *then* recebe dois argumentos; o primeiro argumento é uma função *callback* para o caso da promisse ter sucesso, e o segundo argumento também é uma função *callback* para o caso de falha da *promise*.

```javascript
const prom = new Promise((resolve, reject) => {
	resolve('Success!');
});

promise.then((value) => {
	console.log(value);  // 'Success!''
}); 
```

## catch

É similar ao *then*, porém possui apenas uma parâmetro para função *callback* ser recusada. É utilizada para tratar *promises* rejeitadas.

```javascript
const prom = new Promise((resolve, reject) => {
	throw new Error('Eita!');
});

prom.catch((error) => {
	console.error(error);  ;// 'Eita!'
})
```

## finally

Assim como o *finally* do tratamento de exceção. É utilizada para a finalização da operação tanto em casos de sucesso como em casos de falha da *promise*.

```javascript
function checkMail() {
	return new Promise((resolve, reject) => {

		if (Math.random() > 0.5) {
			resolve('Mail has arrived!');
		} else {
			reject(new Error('Failed to arrive'));
		}
	});
}

checkMail()
	.then((main) => {
		console.log(mail);
	})
	.catch((err) => {
		console.log(err);
	})
	.finally(() => {
		console.log('Experiment completed');
	});
```

# Referências

* [https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise)

