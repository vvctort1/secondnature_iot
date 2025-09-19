# Autenticação Facial com Dlib, OpenCV + HaarCascades

## Objetivo

Nosso objetivo é implementar um sistema de autenticação em duas etapas adicionando além das credenciais de email e senha, o reconhecimento facial para garantir maior segurança no acesso de usuários. O sistema busca combinar a biometria facial com a validação de login e senha, permitindo ao usuário entrar com suas credenciais somente depois que seu rosto foi validado. Reduzindo riscos de fraude e aumentando a segurança da aplicação.
  <br><br>
## Execução

1. Ao iniciar, o sistema disponibiliza 3 opções ao usuário:
   - "c" para cadastrar um novo usuário;
   - "l" para efetuar um login (onde inicia a validação)
   - "q" para encerrar o programa
  <br><br>
2. Ao utilizar o comando "c", o sistema armazena o rosto do usuário no arquivo db.pkl. E pede ao usuário que escolha endereço de e-mail e senha. Guardando os dados do usuário em um arquivo json;
     <br><br>
4. O comando "l", inicia a validação:
   - No caso do reconhecimento facial falhar, um retângulo vermelho aparece em volta do rosto, e é mostrado no terminal uma mensagem pedindo ao usuário que reinicie a tentativa de validação;
   - Caso o rosto seja reconhecido, um retângulo verde aparece em volta do rosto, com o e-mail atrelado à face mostrada. Além do reconhecimento facial, o sistema pede ao usuário para que ele sorria (garantindo que não está sendo utilizada uma foto estática na tentativa de burlar a verificação), validando a face + sorriso.
       <br><br>
5. No passo final (após a validação facial), o sistema pede ao usuário que digite as credenciais atreladas ao rosto no terminal. Mostrando uma mensagem de sucesso ou falha.
    <br><br>
  Observação: todas as tentativas de validação são registradas em logs.json.
  <br><br>
### Sobre a Segurança

- O sistema não permite que seja cadastrado mais de 1 endereço de email;
- A cada 3 tentativas mal sucedidas de login ou cadastro, o sistema mostra uma mensagem de bloqueio da aplicação, interrompendo a execução do programa;
- É utilizado o email único para atrelar a face às credenciais. Dessa forma, 2 pessoas com o mesmo nome, não podem acessar o sistema com as credenciais uma da outra.

