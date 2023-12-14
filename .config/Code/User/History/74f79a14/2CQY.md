# Promises

Um objeto *promise* representa o eventual sucesso ou falha de uma tarefa assincrona e o valor resultante. Os métodos `then()`, `catch()` e `finally()` são utilizados para associar futuras ações com um dada *promise*. Esses métodos funcionam como o conjunto *try* - *exception* para funções assincronas.

Exemplo:

```javascript

```

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

[^number]: https://www.w3schools.com/jsref/jsref_obj_number.asp
[^math]: https://www.w3schools.com/jsref/jsref_obj_math.asp
[^IEEE]: https://en.wikipedia.org/wiki/IEEE_754
[^string]: https://www.w3schools.com/jsref/jsref_obj_string.asp
[^boolean]: https://www.w3schools.com/jsref/jsref_obj_boolean.asp
[^array]: https://www.w3schools.com/jsref/jsref_obj_array.asp
[^obj]: https://www.w3schools.com/jsref/jsref_obj_object.asp
[^var]: https://www.w3schools.com/jsref/jsref_var.asp
[^let]: https://www.w3schools.com/js/js_let.asp
[^const]: https://www.w3schools.com/js/js_const.asp
[^hoisting]: https://www.w3schools.com/js/js_hoisting.asp
[^operators]: https://www.w3schools.com/js/js_operators.asp
[^coales]: https://developer.mozilla.org/pt-BR/docs/Web/JavaScript/Reference/Operators/Nullish_coalescing
[^errors]: https://www.w3schools.com/js/js_errors.asp 
[^ifelse]: https://www.w3schools.com/js/js_if_else.asp
[^switch]: https://www.w3schools.com/js/js_switch.asp
[^while]: https://www.w3schools.com/js/js_loop_while.asp
[^function]: https://www.w3schools.com/js/js_functions.asp
[^callback]: https://developer.mozilla.org/en-US/docs/Glossary/Callback_function
[^nested-function]: https://javascript.info/closure#nested-functions
[^closure]: https://javascript.info/closure
[^regex]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Regular_Expressions
[^promise]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise

