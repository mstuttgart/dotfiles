
# constantes para o modo de pagamento
DINHEIRO = '01'
CHEQUE = '02'
CARTAO_CREDITO = '03'
CARTAO_DEBITO = '04'
CREDITO_LOJA = '05'
VALE_ALIMENTACAO = '10'
VALE_REFEICAO = '11'
VALE_PRESENTE = '12'
VALE_COMBUSTIVEL = '13'
DEPOSITO_BANCARIO = '16'
PIX = '17'
TRANSFERENCIA_BANCARIA = '18'
PROGRAMA_DE_FIDELIDADE = '19'
SEM_PAGAMENTO = '90'
OUTROS = '99'

CODIGOS_PAGAMENTO = [
    DINHEIRO,
    CHEQUE,
    CARTAO_CREDITO,
    CARTAO_DEBITO,
    CREDITO_LOJA,
    VALE_ALIMENTACAO,
    VALE_REFEICAO,
    VALE_PRESENTE,
    VALE_COMBUSTIVEL,
    DEPOSITO_BANCARIO,
    PIX,
    TRANSFERENCIA_BANCARIA,
    PROGRAMA_DE_FIDELIDADE,
    SEM_PAGAMENTO,
    OUTROS,
]

FORMA_PAGAMENTO_SELECTION = [
    (DINHEIRO, 'Dinheiro'),
    (CHEQUE, 'Cheque'),
    (CARTAO_CREDITO, 'Cartão de Crédito'),
    (CARTAO_DEBITO, 'Cartão de Débito'),
    (CREDITO_LOJA, 'Crédito Loja'),
    (VALE_ALIMENTACAO, 'Vale Alimentação'),
    (VALE_REFEICAO, 'Vale Refeição'),
    (VALE_PRESENTE, 'Vale Presente'),
    (VALE_COMBUSTIVEL, 'Vale Combustível'),
    (DEPOSITO_BANCARIO, 'Depósito Bancário'),
    (PIX, 'Pagamento Instantâneo (PIX)'),
    (TRANSFERENCIA_BANCARIA, 'Transferência bancária, Carteira Digital'),
    (PROGRAMA_DE_FIDELIDADE, 'Programa de fidelidade, Cashback, Crédito Virtual'),
    (SEM_PAGAMENTO, 'Sem pagamento'),
    (OUTROS, 'Outros'),
]

STATE = [
    ('draft', 'Draft'),
    ('open', 'Open'),
    ('done', 'Done'),
    ('error', 'Error'),
    ('cancel', 'Cancel'),
]
